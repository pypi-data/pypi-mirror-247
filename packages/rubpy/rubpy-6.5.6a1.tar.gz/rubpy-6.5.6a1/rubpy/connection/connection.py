from ..crypto import Crypto
from .. import exceptions
from ..types import SocketResults, Results
import os
import aiohttp
import aiofiles
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

                return (await response.json()).get('data_enc')

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
    
    async def upload_file(self, file, mime: str = None, file_name: str = None, chunk: int = 1048576 * 2,
                          callback=None, *args, **kwargs):
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('file not found in the given path')

            if file_name is None:
                file_name = os.path.basename(file)

            async with aiofiles.open(file, 'rb') as file:
                file = await file.read()

        elif not isinstance(file, bytes):
            raise TypeError('file arg value must be file path or bytes')

        if file_name is None:
            raise ValueError('the file_name is not set')

        if mime is None:
            mime = file_name.split('.')[-1]

        result = await self.client.request_send_file(file_name, len(file), mime)

        id = result.id
        index = 0
        dc_id = result.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        while index < total:
            data = file[index * chunk: index * chunk + chunk]
            try:
                result = await self.session.post(
                    upload_url,
                    headers={
                        'auth': self.client.auth,
                        'file-id': id,
                        'total-part': str(total),
                        'part-number': str(index + 1),
                        'chunk-size': str(len(data)),
                        'access-hash-send': access_hash_send
                    },
                    data=data
                )
                result = await result.json()
                if callable(callback):
                    try:
                        await callback(len(file), index * chunk)

                    except exceptions.CancelledError:
                        return None

                    except Exception:
                        pass

                index += 1
            except Exception:
                pass

        status = result['status']
        status_det = result['status_det']

        if status == 'OK' and status_det == 'OK':
            result = {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            }

            return Results(result)

        #self._client._logger.debug('upload failed', extra={'data': result})
        raise exceptions(status_det)(result, request=result)