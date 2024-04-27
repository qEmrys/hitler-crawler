from .utils import input_validator
from bs4 import BeautifulSoup
from queue import Queue
import asyncio
import aiohttp

class Crawler():
    def __init__(self) -> None:
        self._initial_url = None
        self._stage = 0

    @property
    def initial_url(self):
        return self._initial_url

    @initial_url.setter
    def initial_url(self, value):
        self._initial_url = input_validator(value)


    async def get_links(self, session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url, timeout=1) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                product_divs = soup.find('div', {'id': 'mw-content-text'})
                links = product_divs.find_all(
                    lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/wiki/')
                )

                return list([link.get('href') for link in links])
        except asyncio.TimeoutError:
            print('Timed out')
            return list()
            

    async def check_links(self, articles: list):
        if any(article == "/wiki/Adolf_Hitler" for article in articles):
            print('Hitler found.')


    async def set_to_queue(self, session: aiohttp.ClientSession, queue: Queue, url: str, current_stage: int):
        print(f'stage: {current_stage}; url: {url}')
        articles = await self.get_links(session, url)
        await self.check_links(articles)

        for article in articles:
            queue.put(('https://en.wikipedia.org' + article, current_stage + 1))


    async def gather_data(self, queue:Queue, stage: int):
        tasks = list()
        urls = list()

        while not queue.empty():
            current_stage = queue.queue[0][1]

            if current_stage != stage:
                break

            url = queue.get()[0]
            urls.append(url)

        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as group:
                for url in urls:
                    result = group.create_task(self.set_to_queue(session, queue, url, current_stage))


    async def get_hitler_page(self):
        queue = Queue()
        queue.put((self._initial_url, 0))
        
        for stage in range(7):
            await self.gather_data(queue, stage)
