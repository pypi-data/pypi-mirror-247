import asyncio

import aiohttp
import logging

from gulf_id_scanner import Client, ServiceError


async def main() -> None:
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    session = aiohttp.ClientSession()
    client = Client(host="192.168.3.45", web_session=session)
    try:
        await client.connect()
        print(client.support_card_detect)
        card_data = await client.async_read_card()
        print(card_data)
    except ServiceError as err:
        print(str(err))
    try:
        async for detected_card in client.async_detect_card():
            print(detected_card)
    except ServiceError as err:
        print(str(err))
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
