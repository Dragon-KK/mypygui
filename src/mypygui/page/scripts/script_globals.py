'''All the variables given in global scrope to scripts'''
from ...core.services.resource_handling import ResourceHandler
from ...page.objects.dom.dom_node import ClassList
from ...page.objects import DOM, DOMNode, Image
from ...core.services.events import Event
from ...core.asynchronous import Promise
from ...page.clipboard import ClipBoard
from ...core.fs import URI, FileType
from ...logging import console
from ...util import Object
from ...tools import validate_text_input
document : DOM
resource_handler : ResourceHandler
clipboard : ClipBoard
page_closed : Promise
tmp_store : Object
def reload_page():
    '''
    Basically closes the page and shows it again (after reloading it)
    '''    

def redirect(uri:fs.URI):
    '''
    Closes the current page and then loads and 
    '''    

def end_application(reason = "Closed by script"):
    '''
    Closes the window
    '''

def preload_page(uri) -> Promise:
    '''Loads a page onto memory asynchrounoulsy given a uri'''