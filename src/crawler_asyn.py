from utils import *
from wikiapi import wikiapi
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


    async def get_links(self, session:aiohttp.ClientSession, url: str, stage:int):
            async with session.get(url) as resp:
                logging.info(f'stage: {stage}; url: {url}')

                soup = BeautifulSoup(await resp.text(), 'xml')
                articles = [pl.get_text() for pl in soup.find_all('pl')]

                # product_divs = soup.find('div', {'id': 'mw-content-text'})
                # links = product_divs.find_all(
                #     lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/wiki/')
                # )
                # articles = list([link.get('href') for link in links])
                print(f'{url:<150}', end='\r')
                self.check_links(articles)
                await asyncio.sleep(1)

                return articles
            

    def check_links(self, articles: list):
        if any(article == "Adolf_Hitler" for article in articles):
            logging.info('Hitler found.')
            print('\nHITLER FOUND!!!!!')
            quit()


    async def set_to_queue(self, queue: Queue, stage:int, articles: list):
        for article in articles:
            queue.put((article, stage + 1))

    async def manager(self, queue: Queue, session:aiohttp.ClientSession, article:str, stage:int):
        wiki_api = wikiapi.WikiApi()
        wiki_api_url = wiki_api.get_request(article)
        articles = list()

        try:
            articles = await self.get_links(session, wiki_api_url, stage)
        except asyncio.TimeoutError:
            logging.info('Timed out')
        except Exception as error:
            logging.info(error)
            return list()
        
        await self.set_to_queue(queue, stage, articles)

    async def gather_data(self, queue:Queue, current_stage: int):
        tasks = []

        async with aiohttp.ClientSession() as session:
            while not queue.empty():
                article, stage = queue.get()

                if current_stage != stage:
                    break
                #     async with asyncio.TaskGroup() as group:
                #         group.create_task(self.manager(queue, session, article, stage))

                task = asyncio.create_task(self.manager(queue, session, article, stage))
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def get_hitler_page(self):
        queue = Queue()
        queue.put((get_article(self._initial_url), 0))
        
        for stage in range(7):
            logging.info(f'current stage: {stage}'.upper())
            await self.gather_data(queue, stage)
            print('')

        print('HITLER NOT FOUND(((((')
