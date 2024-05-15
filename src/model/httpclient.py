from src.model.config.config import Config
from bs4 import BeautifulSoup
import aiohttp
import logging
import json

class HttpClient:
    def __init__(self, config=None):
        self.config = config or Config()
        # self.session = self.config.transport

    async def request(self, url, headers=None, data=None):
        # session = self.session
        # session.headers = headers

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(BeautifulSoup(await resp.text(), 'html.parser'))
