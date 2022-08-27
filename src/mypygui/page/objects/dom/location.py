from ....util import Object
from ....core import fs

class Location(Object):
    '''Wrapper around `fs.URI` to allow for serialization'''
    __ignore__ = {'_uri'}
    def __init__(self, uri : fs.URI):
        self._uri = uri
        
    @property
    def uri(self):
        '''Stringified uri'''
        return self._uri.to_string()

    def __serialize__(self):
        return {
            '__objecttype__' : self.__class__.__name__,
            self.__class__.__name__ : self.uri
        }

    @classmethod
    def __from_json__(cls, obj : any):
        '''Parses the object from a dict (the root being unserialized)'''
        return cls(
            fs.URI.from_uri_string(obj)
        )

Location.__register_serializer__()
Location.__register_deserializer__()