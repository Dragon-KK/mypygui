from .uri import URI
from enum import Enum, auto
import requests

class FileType(Enum):
    text = auto()
    bytes = auto()

def load_local(uri : URI, file_type : FileType = FileType.text) -> 'Resource':
    '''
    Loads a file located locally given the uri
    NOTE: This process is synchronous
    '''
    if file_type == FileType.text:
        return uri.path.read_text()
    elif file_type == FileType.bytes:
        return uri.path.read_bytes()
    else:
        raise NotImplementedError(f'Reading `{file_type}` files has not been implemeneted yet')

def load_web(uri : URI, file_type : FileType = FileType.text) -> 'Resource':
    '''
    Loads a file located on the web given the uri
    NOTE: This process is synchronous
    '''
    response = requests.get(uri.to_string())
    if file_type == FileType.text:
        return str(response.content)
    elif file_type == FileType.bytes:
        return response.content
    else:
        raise NotImplementedError(f'Reading `{file_type}` files has not been implemeneted yet')

def load(uri : URI, file_type : FileType = FileType.text) -> 'Resource':
    '''
    Loads a file given a uri
    NOTE: This process is synchronous
    '''
    if uri.schema == URI.Schema.file:
        return load_local(uri, file_type)

    elif uri.schema == URI.Schema.http or uri.schema == URI.Schema.https:
        return load_web(uri, file_type)

    else:
        raise NotImplementedError(f'Loading files has not been implemented for `{uri.schema}`')