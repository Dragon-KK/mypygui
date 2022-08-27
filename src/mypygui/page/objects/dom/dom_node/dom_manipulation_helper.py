

def append_child(parent, child):
    if element.tag == 'img':
        element.render_node = ImageRenderNode(element)
        element.render_node._window_provider = self.root.render_node._window_provider
        return True
    elif element.tag == 'span':
        element.render_node = TextRenderNode(element)
        element.render_node._window_provider = self.root.render_node._window_provider
        return None # Span elements cannot have node children
    else:
        element.render_node = RenderNode(element)
        element.render_node._window_provider = self.root.render_node._window_provider
        return True