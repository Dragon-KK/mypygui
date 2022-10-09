from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .objects import DOMNode, PyComponentRenderNode

class PyComponent:
    '''
    NOTE: For py component definitions the only thing given in scope is the `PyComponent` class
    '''
    def __init__(self, dom_node, children):
        self.dom_node : DOMNode = dom_node
        self.children : list[DOMNode] = children
        self.render_node : PyCompositeRenderNode = dom_node.render_node

    def on_remove(self):
        '''Called when the dom node is removed'''
        self.dom_node = None
        for child in self.children:
            child.remove(_reflow=False, _remove_from_parent=False)
        self.children = None

    def on_paint(self):
        '''Called when the render node is painted'''
        pass

    def on_repaint(self):
        '''Called when the render node is reapainted'''
        pass

    def on_layout(self):
        '''Called when the render node is layouted'''
        pass

    @classmethod
    def create(cls, dom_node, children):
        for child in children:
            child.parent = None
        return cls(dom_node, children)