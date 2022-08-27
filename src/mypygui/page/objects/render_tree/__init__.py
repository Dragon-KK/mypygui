from .render_node import RenderNode, RootRenderNode, ImageRenderNode, TextRenderNode
from ....util import Object

class RenderTree(Object):
    def __init__(self, root_render_node : RootRenderNode):
        self.root_render_node = root_render_node

    def layout(self):
        '''Does the initial layouting of the page'''
        self.root_render_node.layout()

    def paint(self):
        '''Does the initial pain of the page'''
        self.root_render_node.paint()
