from __future__ import annotations # to reference classes on each other
from abc import ABC, abstractmethod


# composite pattern
# for services

class Resource(ABC):
    @property
    def parent(self) -> Resource:
        return self._parent

    @parent.setter
    def parent(self, parent: Resource):
        self._parent = parent

    def add(self, component: Resource) -> None:
        pass

    def remove(self, component: Resource) -> None:
        pass

    def is_composite(self) -> bool:
        return False
    
    @property
    def endpoint(self) -> str:
        pass

# leaf
class Path(Resource):
    """ represents end object of composition, do real work
    """
    def __init__(self, endpoint) -> None:
        super().__init__()
        self._endpoint = endpoint
        self.parent = None
    @property
    def endpoint(self) -> str:
        return self._endpoint
    @property
    def fullurl(self) -> str:
        if self.parent != None:
            return self.parent.url + self._endpoint
        
    def nav(self, navid):
        return self.fullurl + f"/navigations({navid})"

# composite
class Service(Resource):
    """ represents node with children, delegate work to them"""
    def __init__(self, service_url) -> None:
        self._children: list[Resource] = []
        self.url = service_url
        self._paths = {}

    @property
    def paths_objs(self):
        return self._paths
    
    @property
    def paths(self):
        paths = {}
        for k in self._paths.keys():
            paths[k] = self._paths[k].fullurl
        return paths
    
    @property
    def pf(self) -> dict:
        """PATHS FULL"""
        paths = {}
        for k in self._paths.keys():
            paths[k] = self._paths[k].fullurl
        return paths
    
    def is_composite(self) -> bool:
        return True

    def add_path(self, path: Path):
        self._paths[path.endpoint.replace('/', '')] = path
        path.parent = self

    def remove(self, component: Resource) -> None:
        self._children.remove(component)
        component.parent = None

    def get_kids(self) -> str:
        
        results = []
        for child in self._children:
            results.append(child.fullurl)
        return f"Path('{'+'.join(results)}')"
    
    

# FACTORY pattern to create EndpointsCollection
class ServiceFactory(ABC):
    @abstractmethod
    def create() -> EndpointsCollection:
        pass

class EndpointsCollection(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.schema = {}

    def add_service(self, name: str, service: Service):
        self.schema[name] = service

    def list_services(self):
        for serv in self.schema:
            print(serv)

# IMPLEMENTATION INTERFACE LEVEL / PRIMITIVE OPERATIONS
class RestAPI(ABC):    
    def __init__(self):
        self._endpoints = None
    def request_handler(self, endpoint):
        pass
    @property
    def api(self)->RestAPI:
        return self._api
    @api.setter
    def api(self, val: RestAPI):
        self._api = val
    @property
    def endpoints(self)->EndpointsCollection:
        return self._endpoints
    @endpoints.setter
    def endpoints(self, val:EndpointsCollection):
        self._endpoints = val

    @property
    def post(self) -> PostAPI:
        pass
    @post.setter
    def post(self, val: PostAPI):
        pass
    @property
    def get(self) -> GetAPI:
        pass
    @get.setter
    def get(self, val: GetAPI):
        pass

class GetAPI(RestAPI):
    @abstractmethod
    def processes():
        pass
    @abstractmethod
    def entities():
        pass

class PostAPI(RestAPI):    
    def token(self):
        pass




