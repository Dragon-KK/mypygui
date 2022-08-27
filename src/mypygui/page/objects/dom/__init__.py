from .dom_node import DOMNode, RootDOMNode
from ....util import Object
from .location import Location

class DOM(Object):
    def __init__(
        self,
        root : RootDOMNode = None,
        location : Location = None ,
        root_directory : Location = None,
        title : str = 'New Document'
    ):
        self.root = root
        '''The root html element'''
        self.location = location
        '''The location of the html file'''
        self.root_directory = root_directory
        '''The location relative to which all resources in the page are resolved'''

        self.title = title
        '''The title of the document'''

    def get_element_by_id(self, id):
        '''Gets an element given an id'''
        return self.root.get_element_by_id(id)

    def get_elements_by_class_name(self, *class_names):
        '''Get elements which have a given class name'''
        return self.root.get_elements_by_class_name(*class_names)

    def get_elements_by_tag_name(self, tag_name):
        '''Get elements which have a given tag name'''
        return self.root.get_elements_by_tag_name(tag_name)
        
DOM.__register_serializer__()
DOM.__register_deserializer__()