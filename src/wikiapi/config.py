from decouple import config

class Config():
    def __init__(self) -> None:
        self.action = config('WIKI_API_ACTION', default='parse')
        self.format = config('WIKI_API_FORMAT', default='xml')
        self.prop = config('WIKI_API_PARSE_PROP', default='links')
        self.page = config('WIKI_API_PAGE', default=None)