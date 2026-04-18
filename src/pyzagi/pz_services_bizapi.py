from .pz_services_abc import Service, Path, ServiceFactory, \
     EndpointsCollection, RestAPI, GetAPI, PostAPI
import requests, json
from typing import Union

# CONCRETE LEVEL
class BizagiAPI(RestAPI):
    """orchestrator class
    manages API requests at low level"""
    def __init__(self, endpoints: EndpointsCollection):
        super().__init__()
        self.endpoints = endpoints
        self._post = None
        self._get = None
        # self.get = BizGet(self) will not give results since there is no self obj yet
        
    @property 
    def post(self):
        return self._post
    @post.setter
    def post(self, postapi: PostAPI):
        self._post = postapi

    @property 
    def get(self):
        return self._get
    @get.setter
    def get(self, getapi: GetAPI):
        self._get = getapi

class BizPost(PostAPI):
    def __init__(self, api: BizagiAPI):
        super().__init__()
        self.api = api
        self.servicename = "BizPost"
    def request_handler(self, endpoint, body, headers = None, timeout = 30, auth = None):
        print(f"\n=> POST request: {endpoint} ...")
        try:
            if auth != None:
                r = requests.post(endpoint,
                        data=body,
                        auth=auth,
                        timeout=timeout) 
            else:
                r = requests.post(endpoint,
                            data=json.dumps(body),
                            headers=headers,
                            timeout=timeout)          
            print('Status:', r.status_code, "/ Details:\n", r.text)
            return r.json(), r.status_code
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def token(self, base, timeout, auth):
        body = {
            'grant_type':'client_credentials',
            'scope':'api'
        } 
        print("\tself.api", self.api.endpoints.schema['oauth2'].paths['token'])
        endpoint = base + self.api.endpoints.schema['oauth2'].paths['token']
        token_resp = self.request_handler(endpoint=endpoint, body=body, timeout=timeout, auth=auth)[0]
        bearer = f"Bearer {token_resp['access_token']}"
        return bearer
        
class BizGet(GetAPI):
    def __init__(self, api: BizagiAPI):
        super().__init__()
        self.api = api
        self.servicename = "BizGet"
    def request_handler(self, endpoint, body = None, headers = None, 
                        timeout = 30, details = False, vanilla = False):
        """Makes GET request
        
        Parameters
        details - to log response body 
        vanilla - to return response body as a string
            else RETURNS JSON body AND status code
        """
        print(f"\n=> GET request: {endpoint} ...")
        values = {
            "url":endpoint,
        }
        if body != None:
            values["body"] = json.dumps(body)
        if headers != None:
            values["headers"] = headers
        if timeout != None:
            values["timeout"] = timeout
        try:            
            r = requests.get(**values)   
            print('Status:', r.status_code)
            if details:
                print("/ Details:\n", r.text)
            if vanilla:
                return r.text
            else:
                return r.json(), r.status_code
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}") 

    def schema(self, baseURL, headers):                
        return self.request_handler(baseURL+self.api.endpoints.schema["data"].paths["$metadata"],
                                    headers=headers,
                                    vanilla=True)
             
    def cases(self, baseURL, headers, caseid: Union[str, int] = None):
        """ DATA/CASES
        Shows inbox for authenticated user
        or info from one case if caseid is specified
        """
        endpoint = baseURL + self.api.endpoints.schema['data'].paths['cases']
        if caseid != None:
            # caseid should be str or int, eg. 101 or "101"
            endpoint += f"({caseid})"             
            return self.request_handler(endpoint=endpoint, headers=headers)[0]
        else:            
            return self.request_handler(endpoint=endpoint, headers=headers)[0]
        
    def cases_workitems():
        pass
    
    def processes():
        pass
    def entities():
        pass
    def entities_values():
        pass
    



class BizagiServicesFactory(ServiceFactory):
    @staticmethod
    def create() -> BizagiAPI:
        """ Creates BizagiAPI orchestrator object
        """
        # ENDPOINT REFERENCE
        bizagiServices = EndpointsCollection()
        # OAUTH2
        oauth2 = Service("oauth2/server/") 
        oauth2.add_path(Path("token/"))
        bizagiServices.add_service('oauth2', oauth2)
        # METADATA
        metadata = Service("odata/metadata/")    
        metadata.add_path(Path("processes"))
        bizagiServices.add_service('metadata', metadata)
        # DATA
        data = Service("odata/data/")    
        data.add_path(Path("entities"))
        data.add_path(Path("cases"))
        data.add_path(Path("$metadata"))
        bizagiServices.add_service('data', data)
        # CREATE AND CONNECT BIZAGIAPI OBJ 
        bizapi = BizagiAPI(bizagiServices)
        bizapi.post = BizPost(bizapi)
        bizapi.get = BizGet(bizapi)
        
        return bizapi
    
# проверить денежный тип
# отдает как просто флоат "value": 199.0, берет так же
    
"""
/odata/data/cases([id_case])/navigations([id_navigation])
/values([id_value])/navigations([id_navigation])
/values([id_value])/navigations

cases(caseid).nav(navid).values(vlid)
"""



