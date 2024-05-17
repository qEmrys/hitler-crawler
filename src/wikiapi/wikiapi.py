from src.wikiapi.config import Config


class WikiApi():
    def __init__(self) -> None:
        self.config = Config()
        self.api_page = 'https://en.wikipedia.org/w/api.php?'

    def get_request(self, page:str):
        self.config.page = page
        request = self.api_page
        api_params = ['action', 'format', 'prop', 'page']
        
        for param in api_params:
            param_value = getattr(self.config, param)

            if param_value != None:
                request += f'{param}={param_value}'
                request += '&'
            
        return request
