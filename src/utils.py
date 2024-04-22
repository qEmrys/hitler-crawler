import re

def input_validator(url:str):
    while not re.match(r'https?://[a-z]+.wikipedia.org/wiki/[^\s]+', url):
        url = input('Incorrect URL. Try again: ')
    return url
