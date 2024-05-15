from decouple import config
import aiohttp

class Config:
    def __init__(self):
        self.timeout = int(config("HTTP_CLIENT_TIMEOUT", default=30))
        self.use_proxy = config("HTTP_CLIENT_USE_PROXY", default="false").lower() == "true"
        self.proxy_url = config("HTTP_CLIENT_PROXY_URL", default=None)
        self.log_req_res_enable = config("HTTP_CLIENT_LOG_REQ_RES_ENABLE", default="true").lower() == "true"
        self.log_req_res_body_enable = config("HTTP_CLIENT_LOG_REQ_RES_BODY_ENABLE", default="true").lower() == "true"
        # self.transport = aiohttp.ClientSession()
