from .crawler import Crawler

def main():
    crawler =  Crawler()
    crawler.initial_url = input('Input started Wikipedia URL: ')
    # crawler.initial_url = 'https://en.wikipedia.org/wiki/Luca_Brecel'
    # crawler.initial_url = 'https://en.wikipedia.org/wiki/Karl_Larenz'
    print(crawler.hitler_finder())


if __name__ == '__main__':
    main()
