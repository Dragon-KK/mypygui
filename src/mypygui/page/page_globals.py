from ..logging import console
from ..core.asynchronous import asyncify, Promise
from .objects import DOM, CSSOM, RenderTree, DOMNode, RenderNode
from .objects.dom.dom_node import ClassList
from ..core.services.events import Event
from ..page.objects.image_container import Image
from ..core import fs
from ..util import Object
from ..tools import validate_text_input
def get_globals(page):
    return {
        'document' : page.dom,
        'validate_text_input' : validate_text_input,
        'DOMNode' : DOMNode,
        'Promise' : Promise,
        'Object' : Object,
        'Event' : Event,
        'ClassList' : ClassList,
        'console' : console,
        'URI' : fs.URI,
        'FileType' : fs.FileType,
        'resource_handler' : page.browser_window.resource_handler,
        'worker' : page.browser_window.worker,
        'reload_page' : page.reload_page,
        'Image' : Image,
        'redirect' : page.redirect,
        'end_application' : page.end_application,
        'page_closed' : Promise(),
        'clipboard' : page.clipboard,
        'tmp_store' : page.browser_window.tmp_store
    }