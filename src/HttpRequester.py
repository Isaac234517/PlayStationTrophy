import requests
from requests.models import Response
class HttpRequester:
    def __init__(self, base_address:str, use_proxy:bool):
        self.base_address = base_address
        self.use_proxy = use_proxy

    
    def get(self, api, params:dict = None, header:dict= None, cookie:dict = None, allow_redirects:bool = False) -> Response:
        endpoint = f'{self.base_address}{api}'
        resp = requests.get(endpoint, params = params, headers = header, cookies = cookie, allow_redirects= allow_redirects)
        return resp


    def post(self, api, params:dict, header:dict= None) -> Response:
        endpoint = f'{self.base_address}{api}'
        resp = requests.post(endpoint, data = params,headers= header)
        return resp
    
    def patch(self, api, params:dict, header:dict = None) -> Response:
        endpoint = f'{self.base_address}{api}'
        resp = requests.patch(endpoint, headers= header, json = params)
        return resp
