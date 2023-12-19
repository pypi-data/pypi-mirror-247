from abc import abstractmethod
from typing import Callable

current_module = __name__

# #  Base extension pkg
class PackageTrackerMeta(type):
    _class_package_map = {}

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)
        package_name = dct.get('__module__')
        if package_name != current_module:
            if name in cls._class_package_map:
                raise Exception("Only one module is allowed.")
            cls._class_package_map[name] = package_name
        return new_class

    @classmethod
    def get_class_package(cls, class_name):
        return cls._class_package_map.get(class_name, None)

    @classmethod
    def package_imported(cls):
        return len(cls._class_package_map) > 0
    

class RequestTrackerMeta(type):
    _request_type_set = set()

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)

        # Retrieve request_type from dct, if it's defined
        request_type = dct.get('request_type')
        if request_type:
            cls._request_type_set.add(request_type)

        return new_class

    @classmethod
    def get_request_type_set(cls):
        return cls._request_type_set
    

class ResponseTrackerMeta(type):
    _response_type_set = set()

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)

        # Retrieve response_type from dct, if it's defined
        response_type = dct.get('response_type')
        if response_type:
            cls._response_type_set.add(response_type)

        return new_class

    @classmethod
    def get_response_type_set(cls):
        return cls._response_type_set
    

class WebApp(metaclass=PackageTrackerMeta):
    @abstractmethod
    def route(self, func: Callable):
        pass
    
    @abstractmethod
    def get_app():
        pass

class WebServer(metaclass=PackageTrackerMeta):
    def __init__(self, hostname, port, web_app: WebApp):
        self.hostname = hostname
        self.port = port
        self.web_app = web_app.get_app()

    @abstractmethod
    async def serve(self):
        pass

