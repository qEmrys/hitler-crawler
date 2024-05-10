from utils import input_validator
from bs4 import BeautifulSoup
from queue import Queue
import asyncio
import aiohttp
import logging


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


    async def get_links(self, url: str, stage:int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                logging.info(f'stage: {stage}; url: {url}')
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                product_divs = soup.find('div', {'id': 'mw-content-text'})
                links = product_divs.find_all(
                    lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/wiki/')
                )
                articles = list([link.get('href') for link in links])
                print(f'{url:<150}', end='\r')
                self.check_links(articles)
                await asyncio.sleep(1)

                return articles
            

    def check_links(self, articles: list):
        if any(article == "/wiki/Adolf_Hitler" for article in articles):
            logging.info('Hitler found.')
            print('\nHITLER FOUND!!!!!')
            quit()


    async def set_to_queue(self, queue: Queue, stage:int, articles: list):
        for article in articles:
            queue.put(('https://en.wikipedia.org' + article, stage + 1))

    async def manager(self, queue: Queue, url:str, stage:int):
        articles = list()

        try:
            articles = await self.get_links(url, stage)
        except asyncio.TimeoutError:
            logging.info('Timed out')
        except Exception as error:
            logging.info(error)
            return list()
        
        await self.set_to_queue(queue, stage, articles)

    async def gather_data(self, queue:Queue, current_stage: int):
        tasks = []

        while not queue.empty():
            url, stage = queue.get()

            if current_stage != stage:
                break

            task = asyncio.create_task(self.manager(queue, url, stage))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def get_hitler_page(self):
        queue = Queue()
        queue.put((self._initial_url, 0))
        
        for stage in range(7):
            logging.info(f'current stage: {stage}'.upper())
            await self.gather_data(queue, stage)
            print('')

        print('HITLER NOT FOUND(((((')
