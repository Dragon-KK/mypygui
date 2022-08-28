from ..logging import console
from ..core.asynchronous import asyncify, Promise
from .objects import DOM, CSSOM, RenderTree, DOMNode, RenderNode
from .objects.dom.dom_node import ClassList
from ..core.services.events import Event
from ..page.objects.image_container import Image
from ..core import fs

def get_globals(page):
    return {
        'document' : page.dom,
        'DOMNode' : DOMNode,
        'Promise' : Promise,
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
        'clipboard' : page.clipboard
    }