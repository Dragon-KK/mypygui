from __future__ import annotations
from .....util import Object, functions
from .....core.asynchronous import Promise
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from ...render_tree import RenderNode
    from ....py_component import PyComponent
from .style_container import Styles, css
from .state_maintainers import ClassList, StateContainer
from .....core.services.events import EventEmitter, Event
from ....page_loader_helper import link_dom


class DOMNode(Object):
    '''
    The building block of the dom
    NOTE: Remember that the renderNode is created in the layouting step and so any element created after that must have its render node added
    NOTE: Remember that styles are computed and set after creation of the cssom, so any element created after this must have its styles calculated
    '''
    __ignore__ = {'parent'}
    # __slots__ = ( # Does this really help?
    #     'parent',
    #     'children',
    #     'tag',
    #     'id',
    #     'class_list',
    #     'state',
    #     'styles',
    #     'render_node',
    #     '_visible',
    #     'attrs',
    #     'content',
    #     'image',
    #     'event_emitter',
    # )

    def __init__(
        self,
        parent      : DOMNode        = None,
        children    : list[DOMNode]  = None,
        tag         : str            = None,
        class_list  : ClassList      = None,
        id          : Optional[str]  = None,
        attrs       : Object         = None,
        styles      : StyleContainer = None,
        render_node : RenderNode     = None,
        content     : str            = None,
        image       : Promise        = None,
        component   : PyComponent    = None
    ):
        super().__init__()
        # Heirarchy
        self.parent    = parent
        '''The heirarchichal parent of this element'''
        self.children  = children if children is not None else []
        '''List of elements which are children of me'''
        
        # Descriptors
        self.tag        = tag if tag is not None else 'div'
        '''The tag name of the element'''
        self.id         = id
        '''The id of this element (as specified in the html)'''
        self.class_list = class_list if class_list is not None else ClassList()
        '''A collection of classes associated with the element'''
        self.class_list.element = self

        self.state      = StateContainer('') # `''` implies default state
        '''The current state of the element'''
        self.state.element = self

        # View
        self.styles    = styles if styles is not None else Styles()
        '''The styles associated with the element'''
        self.render_node : RenderNode = render_node
        '''The object tasked with rendering me on the screen'''
        self._visible = False
        '''A property that is to be used in the render tree'''

        # Misc
        self.attrs     = attrs if attrs is not None else Object()
        '''An object that contains all properties defined in the html'''

        self.content = content if content is not None else ''
        '''
        The textual content in the element
        NOTE: Only the content of span elements is shown
        '''

        self.image = image
        '''
        The image content in the element
        NOTE: Only the image of an image element is shown
        '''

        self.component = component
        '''
        The component object
        NOTE: Only components have this property set
        '''

        self.event_emitter = EventEmitter(self)
        '''The entity tasked with emitting dom events'''

        self.event_emitter.subscribe(Event.Types.enter, lambda e: self.event_emitter.dispatch(Event(Event.Types.hover_start, self, True)) if e.target == self else None)
        self.event_emitter.subscribe(Event.Types.leave, lambda e: self.event_emitter.dispatch(Event(Event.Types.hover_end, self, True)) if e.target == self else None)

        self.event_emitter.subscribe(Event.Types.hover_start, lambda e: self.state.add('hover-top') if e.target == self else None)
        self.event_emitter.subscribe(Event.Types.hover_end, lambda e: self.state.remove('hover-top') if e.target == self else None)

        self.event_emitter.subscribe(Event.Types.hover_start, lambda e: self.state.add('hover'))
        self.event_emitter.subscribe(Event.Types.hover_end, lambda e: self.state.remove('hover'))

    def get_element_by_id(self, id) -> DOMNode | None:
        '''Gets an element given an id'''
        if self.id == id:return self
        for child in self.children:
            xs = child.get_element_by_id(id)
            if xs is not None:
                return xs
        return None

    def get_elements_by_class_name(self, class_name) -> list[DOMNode]:
        '''Get elements which have a given class name'''
        result = []
        if self.class_list.contains(class_name):result.append(self)
        for child in self.children:
            result.extend(child.get_elements_by_class_name(class_name))
        return result

    def get_elements_by_tag_name(self, tag_name) -> list[DOMNode]:
        '''Get elements which have a given tag name'''
        result = []
        if self.tag == tag_name:result.append(self)
        for child in self.children:
            result.extend(child.get_elements_by_tag_name(tag_name))
        return result

    def append_child(self, node : DOMNode):
        '''
        Adds an element to the dom 
        Sets its render nodes, calculates heirarchy and triggers a relayout
        '''
        
        # Ok So the render tree has to be like created before the subtree is linked
        # Create render nodes for subtree
        node.parent = self
        link_dom(node, self.styles._cssom, self.render_node._window_provider, event_handler=self.event_emitter.event_handler, set_parent = True)

        # Calculate heirarchy
        def get_root(dom_node : DOMNode):
            if dom_node.parent is None:return dom_node
            return get_root(dom_node.parent)
        
        closest_relative = self.render_node.closest_relative
        root = get_root(self)

        self.children.append(node)
        node.render_node.set_heirarchy(closest_relative, root.render_node)
        
        # Trigger layout
        root.render_node.request_reflow()  

    def __eq__(self, other):
        return other is self      

    def remove(self, _reflow=True, _remove_from_parent=True):
        '''
        Removes an element from the dom tree
        Triggers a layout recalculation
        '''
        # Remove from dom (from parents children and set parent to None also set visible to False)
        self._visible = False
        if _remove_from_parent:self.parent.children.remove(self)
        self.parent = None
        
        children = self.children.copy()
        self.children.clear()
        # Remove children
        for child in children:
            child.remove(_reflow=False, _remove_from_parent=False)

        # Remove from render tree
        if self.render_node is not None:
            master = self.render_node.master
            self.render_node.remove()
        if self.component is not None:
            self.component.on_remove()
            self.component = None
        self.image = None
        # Also remove references from style_container and disable event_emitter
        self.event_emitter.disabled = True
        self.event_emitter.subscribers.clear()
        self.event_emitter.target = None
        self.styles._cssom = None
        self.styles._element = None
        self.styles._clear()

        # Delete render node
        self.render_node = None
        
        # Trigger layout
        if _reflow:master.request_reflow()


    def __repr__(self):
        class_list = f' class="{" ".join(self.class_list)}"' if self.class_list else ''
        attrs = ' '.join(f'{key}="{value}"' for key, value in self.attrs.__dict__.items() if key not in ('class'))
        attrs = (' ' + attrs) if attrs else ''
        return f'<{self.tag}{class_list}{attrs}>{f"...({len(self.children)})..." if self.children else ""}</{self.tag}>'

    def _on_class_change(self, added = None, removed = None, update_styles = True):
        '''
        Callback called when the class_list of an element has changed
        NOTE: The element can request for a style change if asked for
        '''
        if update_styles:
            self.styles.compute_true_styles()

    def _on_state_change(self, added = None, removed = None, update_styles = True):
        '''
        Callback called when the state of an element has changed
        NOTE: The element can request for a style change if asked for
        '''
        if update_styles:
            self.styles.compute_true_styles()
    def _on_true_style_change(self):
        '''
        Callback called when the true styles of an element have changed
        NOTE: The element will request for a reflow over here
        '''
        
        # TODO: Detect any changes in style that can cause a reheirarchy calculatoin or repaint to be needed
        # eg: change in closest relative element or change in composite needingness
        self.render_node.request_reflow()
    

DOMNode.__register_serializer__()
DOMNode.__register_deserializer__()
DOMNode.__register_iterable__('ClassList')
DOMNode.__register_serializer__(custom=ClassList, serializer=lambda v:{'__objecttype__' : 'ClassList', 'ClassList' : list(v.keys())})
DOMNode.__register_deserializer__(custom=ClassList, deserializer=lambda v:ClassList(*v))
DOMNode.__register_iterable__('StateContainer')
DOMNode.__register_serializer__(custom=StateContainer, serializer=lambda v:{'__objecttype__' : 'StateContainer', 'StateContainer' : list(v.keys())})
DOMNode.__register_deserializer__(custom=StateContainer, deserializer=lambda v:StateContainer(*v))

# def on_true_style_change(self):
#     '''
#     Callback called when the true styles of an element have changed
#     NOTE: The element will request for a reflow over here
#     '''
#     self.render_node.request_reflow()

# def on_state_change(self, added = None, removed = None, update_styles = True):
#     '''
#     Callback called when the state of an element has changed
#     NOTE: The element can request for a style change if asked for
#     '''
#     if update_styles:self.styles.compute_true_styles()

# def on_class_change(self, added = None, removed = None, update_styles = True):
#     '''
#     Callback called when the class_list of an element has changed
#     NOTE: The element can request for a style change if asked for
#     '''
#     if update_styles:self.styles.compute_true_styles()
    