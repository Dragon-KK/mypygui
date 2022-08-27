'''A bunch of functions to provide simple debugging of Objects'''

import json
from .object import Object

def stringify(obj : dict, **kwargs) -> str:
    '''Converts a jsonifiable dictionary into a string'''
    return json.dumps(obj, **kwargs)

def parse(raw : str) -> dict:
    '''Converts a stringified string to a dictionary'''
    return json.loads(raw)

def deserialize_from_str(raw : str, **kwargs):
    '''Deserializes an object given a stringified serialized object'''
    return deserialize(parse(raw), **kwargs)

def serialize_to_str(obj : Object, **kwargs):
    '''Serializes and stringifies an object'''
    return stringify(serialize(obj), **kwargs)

def serialize(obj : Object) -> dict:
    '''Serializes an object'''
    return obj.__serialize__()

def deserialize(dictionary : dict, **kwargs) -> Object:
    '''Deserializes an object'''
    return Object.__deserialize__(dictionary, **kwargs)