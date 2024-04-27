from src.crawler_asyn import Crawler
import asyncio

async def main():
    crawler =  Crawler()
    # crawler.initial_url = input('Input started Wikipedia URL: ')
    # crawler.initial_url = 'https://en.wikipedia.org/wiki/Luca_Brecel'
    crawler.initial_url = 'https://en.wikipedia.org/wiki/Karl_Larenz'
    # crawler.initial_url = 'https://en.wikipedia.org/wiki/Nazism'
    
    await crawler.get_hitler_page()


if __name__ == '__main__':
    asyncio.run(main())
