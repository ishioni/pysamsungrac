import asyncio
# import async_timeout
import aiohttp
import os
import ssl
import logging

from aiohttp import ClientSession

from pysamsungrac.exceptions import DeviceTimeoutError, DeviceCommuncationError

DEFAULT_TIMEOUT = 10
_LOGGER = logging.getLogger(__name__)


class SamsungRacToken:
    def __init__(self, address):
        pass

    # async def token_server(self):
    #     """Start webserver"""
    #     cert = os.path.join(os.path.dirname(__file__), 'ac14k_m.pem')
    #     ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cert)
    #     ssl_ctx.load_cert_chain(cert)
    #     server = aiohttp.web.Application()

    # async def request_token(self):
    #     """Create server listener here"""
    #
    #     resource = '/devicetoken/request'
    #     try:
    #         await self._session.post(self._url + resource)
    #     except asyncio.TimeoutError:
    #         _LOGGER.error('Timed out requesting command to SamsungRac')
    #     except aiohttp.ClientResponseError as error:
    #         _LOGGER.error('Error requesting token from SamsungRac: %s', error.message)
    #     _LOGGER.info('Turn on the unit now!')


class SamsungRacConnection:
    """Class to communicate with the device"""

    def __init__(self, address, token, timeout=DEFAULT_TIMEOUT, session=None) -> None:
        self._loop = asyncio.get_event_loop()
        if session is None:
            self._session = self._loop.run_until_complete(self._create_session())
        else:
            self._session = session
        self._url = f'https://{address}:8888'
        self._timeout = timeout
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

    def __del__(self):
        self._loop.run_until_complete(self._session.close())

    @staticmethod
    async def _create_session() -> ClientSession:
        cert = os.path.join(os.path.dirname(__file__), 'ac14k_m.pem')
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=cert)
        ssl_ctx.load_cert_chain(cert)
        return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_ctx), raise_for_status=True)

    async def get(self, resource):
        _LOGGER.debug('GET: %s', self._url + resource)
        try:
            resp = await self._session.get(self._url + resource, headers=self._headers)
        except aiohttp.ServerTimeoutError as e:
            raise DeviceTimeoutError(e)
        except aiohttp.ClientResponseError as e:
            raise DeviceCommuncationError(e)
        return await resp.text()

    async def put(self, resource, command):
        _LOGGER.debug('PUT: %s, %s', self._url + resource, command)
        try:
            await self._session.put(self._url + resource, json=command, headers=self._headers)
        except aiohttp.ServerTimeoutError as e:
            raise DeviceTimeoutError(e)
        except aiohttp.ClientResponseError as e:
            raise DeviceCommuncationError(e)
