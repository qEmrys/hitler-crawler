from .utils import input_validator
from queue import Queue
from lxml import html
import requests
import re

class Crawler():
    def __init__(self) -> None:
        self._initial_url = None

    @property
    def initial_url(self):
        return self._initial_url

    @initial_url.setter
    def initial_url(self, value):
        self._initial_url = input_validator(value)

    def check_hitler(self, url):
        articles = self.get_links(url)
        return any(article == "Adolf_Hitler" for article in articles)

    def get_links(self, url):
        response = requests.get(url)
        webpage = html.fromstring(response.content)
        links = webpage.xpath('//div[contains(@id, "bodyContent")]//a/@href').__str__()
        wiki_articles = []

        for link in set(re.findall(r'/wiki/([^\s]+)\'', links)):
            wiki_articles.append(link)
        
        return wiki_articles

    def hitler_finder(self):
        queue = Queue()
        queue.put((self._initial_url, 0))

        while not queue.empty():
            current_url, stage = queue.get()
            print(f"stage: {stage}; link: {current_url}")

            if stage > 6:
                return 'Hitler not found.'
            
            if self.check_hitler(current_url):
                return 'Hitler found.'
            
            for article in self.get_links(current_url):
                queue.put(('https://en.wikipedia.org/wiki/' + article, stage + 1))
        
        return None
