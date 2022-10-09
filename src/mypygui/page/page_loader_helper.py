from ..util import functions
from ..logging import console
from .objects.render_tree import RootRenderNode, ImageRenderNode, TextRenderNode, RenderNode, PyComponentRenderNode

def link_dom(root, cssom, window_provider, event_handler = None, set_parent = False):
    '''
    Connects all dom elements to their respective styles and creates the renderNodes for each domNode
    '''
    # Setting reference for dom nodes and render nodes is to be done here
    def handle_node(node, parent, args):
        node.styles._set_reference(node, cssom)
        if set_parent and node.parent is None:
            node.parent = parent
        if event_handler is not None:
            node.event_emitter.disabled = False
            node.event_emitter.event_handler = event_handler
        node.styles.compute_true_styles(notify_element=False)
        if node.parent is None: # The element is the root node
            node.render_node = RootRenderNode(node)
            node.render_node._window_provider = window_provider
            return True
        if node.tag == 'img':
            node.render_node = ImageRenderNode(node)
            node.render_node._window_provider = window_provider
            if node.image is None:
                console.error('Image has not been parsed on dom node')
                return None
        elif node.tag == 'span':
            node.render_node = TextRenderNode(node)
            node.render_node._window_provider = window_provider
            return None # Span elements cannot have node children
        elif node.tag.startswith('py-') and window_provider.py_components.get(node.tag.removeprefix('py-')) is not None:
            children = node.children
            node.children = []
            node.render_node = PyComponentRenderNode(node)
            node.component = window_provider.py_components[node.tag.removeprefix('py-')].create(node, children)
            node.render_node._window_provider = window_provider
            return True
        else:
            node.render_node = RenderNode(node)
            node.render_node._window_provider = window_provider
            return True
    functions.traverse_tree(root, handle_node)