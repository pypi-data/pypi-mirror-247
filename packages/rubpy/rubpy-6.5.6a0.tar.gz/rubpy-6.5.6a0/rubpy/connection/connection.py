from ..crypto import Crypto
from ..types import SocketResults
import aiohttp
import asyncio


class Connection:
    def __init__(self, client) -> None:
        self.client = client
        self.session = self.make_session()
        self.api_url = None
        self.wss_url = None

    def make_session(self):
        return aiohttp.ClientSession(
            headers={'user-agent': self.client.user_agent,
            	'origin': 'https://web.rubika.ir',
            	'referer': 'https://web.rubika.ir/'},
            timeout=aiohttp.ClientTimeout(total=self.client.timeout)
        )

    async def close(self):
        await self.session.close()

    async def get_dcs(self):
        while True:
            try:
                async with self.session.get('https://getdcmess.iranlms.ir/') as response:
                    if not response.ok:
                        continue

                    response = (await response.json()).get('data')
                    self.api_url = response.get('API').get(response.get('default_api'))
                    self.wss_url = response.get('socket').get(response.get('default_socket'))
                    return True

            except aiohttp.ServerTimeoutError:
                continue

    async def request(self, data: dict):
        while True:
            async with self.session.post(self.api_url, json=data) as response:
                if not response.ok:
                    continue

                response = await response.json()
                data_enc = response.get('data_enc')

                if data_enc:
                    return data_enc

    async def update_handler(self, update: dict):
        data_enc: str = update.get('data_enc')
        if data_enc is not None:
            result = Crypto.decrypt(update.get('data_enc'),
                                    key=self.client.key)
            handlers = self.client.handlers.copy()

            for func, handler in handlers.items():
                for update in result.get(handler):
                    update['client'] = self.client
                    await func(SocketResults(update))

    async def get_updates(self):
        async with self.session.ws_connect(self.wss_url) as wss:
            self.ws_connect = wss
            await self.send_json_to_ws()
            asyncio.create_task(self.send_json_to_ws(data=True))

            async for message in wss:
                message = message.json()

                if message.get('status'):
                    continue

                asyncio.create_task(self.update_handler(message))

    async def send_json_to_ws(self, data=False):
        if data:
            while True:
                await asyncio.sleep(10)
                return await self.ws_connect.send_json('{}')

        return await self.ws_connect.send_json(
            {
                'method': 'handShake',
                'auth': self.client.auth,
                'api_version': '5',
                'data': '',
            })