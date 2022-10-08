class SVGComponent(PyComponent):
    def __init__(self):
        self.render_node
        self.dom_node
        self.children

        # NOTE: The domnodes will not have children, instead children are passed as arguments (but parent property exists)

    def onpaint():
        pass

    def onrepaint():
        pass

    # The normal node and render node will be created for a pycomponent
    # Dont over complicate

    # The only difference is a new composite is always created for a component and the componenet can hook into 'onpaint', 'onrepaint' hooks inorder to do some extra rendering based on the content in it :)


    # (Could normal elements just become py componenets potentially? No the cost would be a lot)

    # PyComponenets are essentiall

def RegisterComponenet(PyComponenetHandler):
    PyComponenetHandler.register_pycomponent('svg', SVGComponent)