import re

def valid_wiki_url(url:str):
    if re.match(r'https?://[a-z]+.wikipedia.org/wiki/[^\s]+', url):
        return url
    return None

def input_validator(url:str):
    while not valid_wiki_url(url):
        url = input('Incorrect Wiki URL. Try again: ')
    return url

def get_article(url:str):
    return url.rsplit('/', 1)[-1]
