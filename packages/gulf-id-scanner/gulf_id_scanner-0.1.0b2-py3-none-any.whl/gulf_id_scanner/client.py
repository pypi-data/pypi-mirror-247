"""Websocket client for Emirates ID."""

from collections.abc import Callable
import json
import logging
from enum import Enum
from typing import Any, AsyncIterator, cast

import aiohttp

from .exceptions import (
    ReadError,
    ReaderNotFound,
    ServiceDisconnected,
    ServiceUnavailable,
)
from .models import (
    CardData,
    EIDCardData,
    Request,
    GCCIDCardData,
)

_LOGGER = logging.getLogger(__name__)

PROTOCOLS = ["eida-toolkit"]


class ServiceState(Enum):
    """Card reader service state."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    READY = "ready"


class Client:
    """Class for reading EID data over websocket."""

    def __init__(
        self,
        *,
        host: str,
        web_session: aiohttp.ClientSession,
        eid_ws_port: int = 9004,
        gcc_ws_port: int = 5060,
        use_ssl: bool = False,
    ) -> None:
        """Initiate class."""
        self.host = host
        self.eid_url = f"ws{'s' if use_ssl else ''}://{host}:{eid_ws_port}"
        self.gcc_id_url = f"ws{'s' if use_ssl else ''}://{host}:{gcc_ws_port}/SCardRead"
        self.ssl = use_ssl
        self.web_session = web_session
        self.request = Request()
        self.eid_ws_state = ServiceState.DISCONNECTED
        self.gcc_ws_state = ServiceState.DISCONNECTED

    @staticmethod
    async def _list_readers(readers: list[str]) -> list[str]:
        """List connected ID card readers."""
        return [reader for reader in readers if "Windows Hello" not in reader]

    @property
    def support_card_detect(self) -> bool:
        """Return if card detect service is available."""
        return self.gcc_ws_state not in (ServiceState.DISCONNECTED,)

    @property
    def support_eid(self) -> bool:
        """Return if eid card service is available."""
        return self.eid_ws_state not in (ServiceState.DISCONNECTED,)

    async def _async_ws_request(
        self,
        url: str,
        request: str | dict[str, Any] | None = None,
        protocols: list[str] = [],
    ) -> dict[str, Any] | bool:
        """Send request over ws and return response."""
        async with self.web_session.ws_connect(url, protocols=protocols) as ws:
            if isinstance(request, dict):
                await ws.send_json(request)
            elif isinstance(request, str):
                await ws.send_str(request)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    _LOGGER.debug("Received %s", msg.data)
                    if msg.data == "Connected to WebSockets Server!":
                        if request is None:
                            return True
                        continue
                    else:
                        try:
                            return msg.json()
                        except json.JSONDecodeError:
                            raise ValueError(f"Data received is not json. {msg.data}")
        return False

    async def _async_eid_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Send a ws request to EID service and return the response."""
        try:
            return cast(
                dict[str, Any],
                await self._async_ws_request(self.eid_url, request, PROTOCOLS),
            )
        except aiohttp.ClientConnectionError as err:
            raise ServiceDisconnected("EID reader service is unavailable.") from err

    async def _async_gcc_id_request(
        self, request: str | None = None
    ) -> dict[str, Any] | bool:
        """Send a ws request to GCC ID service and return the response."""
        try:
            return await self._async_ws_request(self.gcc_id_url, request)
        except aiohttp.ClientConnectionError as err:
            raise ServiceDisconnected("GCC ID reader service is unavailale.") from err

    async def _connect_reader_with_eid(self) -> bool:
        """Connect to the card reading holding EID."""
        if self.eid_ws_state == ServiceState.DISCONNECTED:
            raise ServiceDisconnected("EID service is disconnected.")
        try:
            response = await self._async_eid_request(self.request.reader_with_eid)
        except ServiceDisconnected:
            return False
        if response["status"] != "success":
            return False
        self.request.context.card_reader_name = response["smartcard_reader"]
        response = await self._async_eid_request(self.request.connect_to_reader)
        if response["status"] != "success":
            return False
        self.request.context.eid_card_context = response["card_context"]
        self.eid_ws_state = ServiceState.READY
        return True

    async def _connect_reader_with_gccid(self) -> bool:
        """Get list of connected readers."""
        if self.gcc_ws_state == ServiceState.DISCONNECTED:
            raise ServiceDisconnected("GCC ID service is disconnected.")
        response = cast(
            dict[str, Any], await self._async_gcc_id_request("GetReaderNames")
        )
        if not (card_readers := await self._list_readers(response["ReaderNames"])):
            return False
        self.request.context.card_reader_name = card_readers[0]
        self.gcc_ws_state = ServiceState.READY
        return True

    async def connect(self) -> None:
        """Connect to the scanner services and set context."""
        if self.gcc_ws_state == ServiceState.DISCONNECTED:
            try:
                if await self._async_gcc_id_request():
                    self.gcc_ws_state = ServiceState.CONNECTED
            except ServiceDisconnected as err:
                _LOGGER.warning(str(err))

        if self.eid_ws_state == ServiceState.DISCONNECTED:
            try:
                response: dict[str, Any] = await self._async_eid_request(
                    Request.establish_context()
                )
                if response.get("status") == "success":
                    self.request.context.service_context = response["service_context"]
                    self.eid_ws_state = ServiceState.CONNECTED
            except ServiceDisconnected as err:
                _LOGGER.warning(str(err))
        if self.gcc_ws_state == self.eid_ws_state == ServiceState.DISCONNECTED:
            raise ServiceUnavailable(
                f"No smart card service detected on host {self.host}"
            )

    async def _read_eid_card_data(self) -> EIDCardData:
        """Read data from EID card."""
        if self.eid_ws_state != ServiceState.READY:
            if not await self._connect_reader_with_eid():
                raise ReadError("No EID smart card detected.")
        response = await self._async_eid_request(self.request.read_eid_card)
        if response["status"] != "success":
            raise ReadError("Failed to read EID card.")
        self.eid_ws_state = ServiceState.CONNECTED
        card_data = EIDCardData(xml_data=response["toolkit_response"])
        return card_data

    async def _read_gcc_card_data(self) -> GCCIDCardData:
        """Read data from other Gulf ID cards."""
        if self.gcc_ws_state != ServiceState.READY:
            if not await self._connect_reader_with_gccid():
                raise ReaderNotFound("No compatible reader detected.")

        response = cast(
            dict[str, Any], await self._async_gcc_id_request(self.request.read_gcc_card)
        )
        if response["MessageType"] == "Error":
            raise ReadError("Failed to read GCC card: %s", response["ErrorDescription"])
        return GCCIDCardData(**response["CardData"])

    async def async_read_card(self) -> CardData:
        """Return data from Gulf ID card."""
        try:
            if self.gcc_ws_state != ServiceState.DISCONNECTED and (
                card_data := await self._read_gcc_card_data()
            ):
                return CardData(card_data)
        except ReadError as err:
            _LOGGER.debug(str(err))
        if self.eid_ws_state != ServiceState.DISCONNECTED and (
            card_data := await self._read_eid_card_data()
        ):
            return CardData(card_data)
        raise ReadError("Card data could not be read")

    async def async_detect_card(
        self,
        *,
        inserted_callback: Callable[[], None] | None = None,
        removed_callback: Callable[[], None] | None = None,
        error_callback: Callable[[str], None] | None = None,
    ) -> AsyncIterator[CardData]:
        """List to card inserted events and read card data."""
        if self.gcc_ws_state == ServiceState.DISCONNECTED:
            raise ServiceDisconnected(
                "GCC ID service is not connectd. Can't listen to card insert events."
            )
        if self.gcc_ws_state != ServiceState.READY and not (
            await self._connect_reader_with_gccid()
        ):
            raise ReaderNotFound("No compatible reader detected.")
        async with self.web_session.ws_connect(
            self.gcc_id_url,
        ) as ws:
            await ws.send_str("RunCardDetection")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    _LOGGER.debug("Received %s", msg.data)
                    if msg.data == "Connected to WebSockets Server!":
                        continue
                    try:
                        response: dict[str, Any] = msg.json()
                    except json.JSONDecodeError:
                        return
                    if response.get("EventName") == "CardMonitorStarted":
                        self.request.context.card_reader_name = response["ReaderName"]
                        continue
                    if response.get("EventName") == "CardInserted":
                        _LOGGER.debug("Card inserted")
                        if inserted_callback is not None:
                            inserted_callback()
                        try:
                            yield await self.async_read_card()
                        except ReadError as err:
                            _LOGGER.error(str(err))
                            if error_callback is not None:
                                error_callback(str(err))
                        continue
                    if response.get("EventName") == "CardRemoved":
                        _LOGGER.debug("Card removed")
                        if removed_callback is not None:
                            removed_callback()
                        continue
        if ws.closed:
            self.gcc_ws_state = ServiceState.DISCONNECTED
            raise ServiceDisconnected("GCC service disconnected.")
