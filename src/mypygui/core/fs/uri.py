from __future__ import annotations
from urllib.parse import urlparse
from urllib.request import url2pathname
from pathlib import Path
from os.path import normpath
from enum import Enum, auto
from .. import exceptions

class URI:
    class Schema(Enum):
        file  = auto()
        http  = auto()
        https = auto()

    def __init__(
        self,
        schema : Schema,
        host : str,
        path : Path,
        queries : list = [],
        fragment : str = ''
    ):
        self.schema = schema
        '''The schema of the uri'''
        self.host = host
        '''The host of the uri'''
        self.path = path
        '''The path pertaining to the uri'''
        
        self.queries = queries
        '''Queries asked in the uri'''
        self.fragment = fragment
        '''Fragments of the uri'''

    @property
    def parent(self) -> URI:
        '''The parent of the uri'''
        return URI(
            self.schema,
            self.host,
            self.path.parent,
            self.queries,
            self.fragment
        )

    def make(self, uri_string : str):
        # LIMIT Improve this
        if uri_string.strip()[:4] == 'http':
            return URI.from_uri_string(uri_string)

        return self.join(uri_string)

    def join(self, *parts) -> URI:
        '''Returns a new merged uri'''
        
        return URI(
            self.schema,
            self.host,
            self.path.joinpath(*parts).resolve(),
            self.queries,
            self.fragment
        )

    def to_string(self) -> str:
        '''Converts the uri to a string'''
        return f'{_str_from_schema(self.schema)}://{self.host}/{self.path}'.replace('/\\','/')

    @classmethod
    def from_uri_string(cls, uri : str, _resolve_path = False):
        '''Forms the uri using a string'''
        parsed = urlparse(uri)
        xs = cls(
            _schema_from_str(parsed.scheme),
            parsed.netloc,
            Path(parsed.path).resolve() if _resolve_path else Path(parsed.path),
            [i.strip() for i in parsed.query.split(';') if i.strip()],
            parsed.fragment
        )
        if xs.schema == URI.Schema.file:
            xs.path = Path(xs.host).resolve()
            xs.host = ''
        return xs

    @classmethod
    def from_local_path_string(cls, path : str):
        '''
        Forms a uri using a path to the given local resource
        NOTE: The paths must be absolute paths
        '''
        return URI.from_uri_string('file://' + normpath(path), _resolve_path = True)

    def __repr__(self):
        return repr({
            'schema' : self.schema,
            'host' : self.host,
            'path' : self.path,            
            'queries' : self.queries,
            'fragment' : self.fragment,
        })

def _schema_from_str(string) -> URI:
    '''Gets the schema from a string'''
    if string == 'file':
        return URI.Schema.file
    elif string == 'http':
        return URI.Schema.http
    elif string == 'https':
        return URI.Schema.https
    else:
        raise exceptions.InvalidURISchema(string)

def _str_from_schema(schema : URI.Schema) -> str:
    '''Converts a schema into its string representation'''
    if schema == URI.Schema.file:
        return 'file'
    elif schema == URI.Schema.http:
        return 'http'
    elif schema == URI.Schema.https:
        return 'https'
    else:
        raise exceptions.InvalidURISchema(schema)