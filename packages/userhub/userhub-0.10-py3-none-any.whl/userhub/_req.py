import aiohttp


async def fetch(url, payload=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            try:
                return await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                return await response.text()
