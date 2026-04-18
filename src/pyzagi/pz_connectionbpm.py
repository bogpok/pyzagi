from __future__ import annotations
import requests
from typing import Union

from .pz_tools import *
from .pz_services_abc import RestAPI

# Using bridge design pattern

# ABSTRACTION LEVEL / WRAPPER
class ConnectionBPM:
    """
    Manages API at high level through BizagiAPI object

    baseURL : str
        Link to your Bizagi project
    client['id'], client['secret']
        Authentication details
    client['username']
        username of client of auth provided
    timeout : int
        timeout for requests in seconds
    """
    def __init__(self, baseURL: str, client: dict, ServiceAPI: RestAPI, timeout: int = 30):
        self.baseURL = baseURL
        self.username = client['username']
        self.auth = (client['id'], client['secret'])        
        self.timeout = timeout
        self.sAPI = ServiceAPI
        self.headers = {}
        
        self._connect()
        

    def _connect(self):
        print(f'\n=> Initiating connection to {self.baseURL}')
        try:
            self.set_token()  
        except:
            raise ConnectionError('\n\tSomething went wrong with the connection.\n\tCheck the baseURL and BIZAGI server availability') 
        else:
            self.headers = {
                "Authorization": self.BTOKEN
            }
            print('Successfully connected\n')

    def set_token(self):
        """ Receive token and put it into attribute of this class """        
        self.BTOKEN = self.sAPI.post.token(self.baseURL, self.timeout, auth = self.auth)
    def schema(self):
        return self.sAPI.get.schema(self.baseURL, self.headers)
    def cases(self, caseid: Union[str, int] = None):
        return self.sAPI.get.cases(self.baseURL, self.headers, caseid)
