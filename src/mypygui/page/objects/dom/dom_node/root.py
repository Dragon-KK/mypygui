from __future__ import annotations
from .node import DOMNode
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from ...render_tree import RootRenderNode

class RootDOMNode(DOMNode):
    '''The root node of the html tree'''
    __ignore__ = {'parent'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        self.render_node : RootRenderNode
        self.event_emitter.never_propogate = True
    

RootDOMNode.__register_serializer__()
RootDOMNode.__register_deserializer__()