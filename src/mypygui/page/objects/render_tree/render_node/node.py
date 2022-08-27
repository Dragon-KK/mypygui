from __future__ import annotations
from .information_containers import LayoutInformationContainer, RenderInformationContainer
from .....util import Object
from .... import css
from tkinter import UNITS, ALL

from .layouting import layouter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...dom import DOMNode
    from .....core.services.rendering import Composite, WindowProvider

from .....core.services.events import Event
BORDER_RADIUS_CORRECTION_FACTOR = 3.1459
BORDER_RADIUS_MAX_MULTIPLIER = 1.25

SHIFT_BITMASK = 0x0001

class RenderNode(Object):
    '''Deals with the layouting and painting of elements'''
    __ignore__ = {'dom_node', 'slaves', 'master'}
    def __init__(self, dom_node : DOMNode):
        # domnode
        self.dom_node = dom_node
        '''The domnode this rendernode is representing'''

        self.closest_relative : RenderNode = None
        '''Closest relative of the element'''

        # Information containers
        self.layout_information = LayoutInformationContainer()
        '''
        Stores information about the layout of the element
        NOTE: The values are in absolute values (px)
        '''
        self.render_information = RenderInformationContainer()
        '''
        Stores information on how the element is to be rendered
        NOTE: The values are in absolute values (px)
        '''
        self._units : dict[css.Unit, float] = {
            css.Unit.px : 1,
            css.Unit.em : 21,
            css.Unit.rem : 21, # For now both em and rem will mean the same thing
            css.Unit.viewport_width : self.layout_information.width,
            css.Unit.viewport_height : self.layout_information.height,
            css.Unit.master_height : 0,
            css.Unit.master_width : 0,
            css.Unit.self_height : self.layout_information.height,
            css.Unit.self_width : self.layout_information.width,
        }
        '''Contains the multipliers for each css Unit'''

        # Heirarchy
        self.master = None
        '''
        The element with respect to which the origin is set
        NOTE: Units like %, em etc. are also calculated wrt to this element
        '''
        self.slaves : dict[int, list[RenderNode]] = {}
        '''
        All elements this element is the master to
        Stored in a dictionary that maps zIndex to lists of renderNodes (stored in the order they are to be rendered)
        NOTE: Removal and addition of foreign slaves must be done by their parents and will not be done by their master
        '''

        # Tendering
        self.needs_composite = False
        '''
        Whether the given element needs to form a composite
        NOTE: This is done in the set_heirarchy step
        '''
        self.master_composite : Composite = None
        '''Reference to the composite that rendered the element'''
        self.own_composite : Composite = None
        '''References own composite if the node needs a composite'''

        self._window_provider : WindowProvider = None

        self.current_scroll_x = 0
        self.current_scroll_y = 0
        self._scroll_listener_is_set = False
        # NOTE The scroll region can be determined using contenet size and normal size



    def set_units(self):
        '''Sets the multipliers of css units'''
        # LIMIT: em and self size not implemented (em is same as rem here)
        self._units[css.Unit.em] = self.master._units.get(css.Unit.em, 0)
        self._units[css.Unit.rem] = self.master._units.get(css.Unit.rem, 0)
        self._units[css.Unit.viewport_height] = self.master._units.get(css.Unit.viewport_height, 0)
        self._units[css.Unit.viewport_width] = self.master._units.get(css.Unit.viewport_width, 0)
        self._units[css.Unit.self_height] = self.layout_information.height
        self._units[css.Unit.self_width] = self.layout_information.width
        self._units[css.Unit.master_height] = self.master.layout_information.height
        self._units[css.Unit.master_width] = self.master.layout_information.width
        
    def get_value(self, value : css.DimensionalValue, default = 0):
        '''Gets the value of a css property'''
        try:
            return value[0] * self._units.get(value[1])
        except:
            return default

    def add_slave(self, slave, z_index):
        '''Registers a slave'''
        if self.slaves.get(z_index) is None:
            self.slaves[z_index] = list()
        self.slaves[z_index].append(slave)
        slave.master = self

    def remove_slave(self, slave, z_index):
        '''Removes a registered slave on the element'''
        if self.slaves.get(z_index) is None:
            return
        try:self.slaves[z_index].remove(slave)
        except:pass

    def set_heirarchy(
        self,
        closest_relative,
        root
    ):
        self.closest_relative = closest_relative
        '''Sets the heirarchy of all elems'''

        if self.dom_node.styles.overflow_x is not None or self.dom_node.styles.overflow_y is not None: # or self.dom_node.styles.opacity != 1:
            self.needs_composite = True # NOTE: Now overflow hidden is implicitly enforced
        if self.dom_node.styles.position == css.Position.absolute:
            # Absolute elements are slaves to the closest element with `position: relative`
            closest_relative.add_slave(self, self.dom_node.styles.z_index if self.dom_node.styles.z_index is not None else 1)
            self.master = closest_relative
        elif self.dom_node.styles.position == css.Position.fixed:
            # Fixed elements are slaves to the root
            root.add_slave(self, self.dom_node.styles.z_index if self.dom_node.styles.z_index is not None else 1)
            self.master = root
            closest_relative = root
        elif self.dom_node.styles.position == css.Position.relative:
            # Relative elements register themselves as the closest relative element for their children
            self.dom_node.parent.render_node.add_slave(self, self.dom_node.styles.z_index if self.dom_node.styles.z_index is not None else 1)
            self.master = self.dom_node.parent.render_node
            closest_relative = self
        elif self.dom_node.styles.position == css.Position.static:
            # Static elements follow the normal flow of the document
            self.dom_node.parent.render_node.add_slave(self, self.dom_node.styles.z_index if self.dom_node.styles.z_index is not None else 1)
            self.master = self.dom_node.parent.render_node
        else:
            raise Exception('Invalid postition')
        for child in self.dom_node.children:
            child.render_node.set_heirarchy(closest_relative, root)

    def _set_render_information(self):
        self.render_information.background_color = self.dom_node.styles.background_color if self.dom_node.styles.background_color is not None else ''
        self.render_information.border_color = self.dom_node.styles.border_color if self.dom_node.styles.border_color is not None else ''
        self.render_information.border_stroke =  self.get_value(self.dom_node.styles.border_width) if self.dom_node.styles.border_width is not None else 0
        self.render_information.height = self.layout_information.height
        self.render_information.width = self.layout_information.width
        self.render_information.border_bottom_left_radius = min(self.get_value(self.dom_node.styles.border_bottom_left_radius) * BORDER_RADIUS_CORRECTION_FACTOR, self.render_information.width * BORDER_RADIUS_MAX_MULTIPLIER, self.render_information.height * BORDER_RADIUS_MAX_MULTIPLIER)
        self.render_information.border_bottom_right_radius = min(self.get_value(self.dom_node.styles.border_bottom_right_radius) * BORDER_RADIUS_CORRECTION_FACTOR, self.render_information.width * BORDER_RADIUS_MAX_MULTIPLIER, self.render_information.height * BORDER_RADIUS_MAX_MULTIPLIER)
        self.render_information.border_top_left_radius = min(self.get_value(self.dom_node.styles.border_top_left_radius) * BORDER_RADIUS_CORRECTION_FACTOR, self.render_information.width * BORDER_RADIUS_MAX_MULTIPLIER, self.render_information.height * BORDER_RADIUS_MAX_MULTIPLIER)
        self.render_information.border_top_right_radius = min(self.get_value(self.dom_node.styles.border_top_right_radius) * BORDER_RADIUS_CORRECTION_FACTOR, self.render_information.width * BORDER_RADIUS_MAX_MULTIPLIER, self.render_information.height * BORDER_RADIUS_MAX_MULTIPLIER)
        self.render_information.x = (self.master.render_information.x if not self.master.needs_composite else 0) + self.layout_information.offset_x + self.master.layout_information.border_width + (self.master.layout_information.padding_left if self.master.dom_node is self.dom_node.parent else 0) + self.layout_information.x
        self.render_information.y = (self.master.render_information.y if not self.master.needs_composite else 0) + self.layout_information.offset_y + self.master.layout_information.border_width + (self.master.layout_information.padding_top if self.master.dom_node is self.dom_node.parent else 0) + self.layout_information.y
    
    def paint(self, composite : Composite):
        '''Paints the thing onto the thingy'''
        if self.dom_node is None:return
        if not self._scroll_listener_is_set:
            self.dom_node.event_emitter.subscribe(Event.Types.scroll, lambda e:self._scroll_event_handler(e))
            self._scroll_listener_is_set = True
        if not self.dom_node._visible:return
        
        self._set_render_information()
        
        self.master_composite = composite
        if self.needs_composite:
            self.own_composite, self.render_information.context = composite.create_composite(self)
            
            # TODO: Hover event doesnt work well with composites
            # On easy way is to make the composite draw a box that fills then everything will easily work with what we already have
            composite = self.own_composite
            composite.canvas.bind('<Button-1>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<Button-2>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<Button-3>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<ButtonRelease>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_up, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<Motion>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_over, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<Enter>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.enter, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<Leave>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.leave, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.bind('<MouseWheel>', lambda e:self.dom_node.event_emitter.dispatch(Event(Event.Types.scroll, self.dom_node, False, _e = e)) if self.dom_node is not None else None)

        else:
            self.render_information.context = composite.create_box_element(self.render_information)

            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-1>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-2>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-3>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<ButtonRelease>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_up, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Motion>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_over, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Enter>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.enter, self.dom_node, True, _e = e)) if self.dom_node is not None else None)
            composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Leave>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.leave, self.dom_node, True, _e = e)) if self.dom_node is not None else None)

        for z_index in self.slaves:
            for slave in self.slaves[z_index]:
                slave.paint(composite if not self.needs_composite else self.own_composite)

    def _scroll_event_handler(self, e):
        # TODO: For some reason tkinter isnt like following scroll region
        # but in the night it works properly 
        # wth
        if e.info._e.state & SHIFT_BITMASK and self.dom_node.styles.overflow_x == css.Overflow.scroll:
            self.own_composite.scroll_x(-e.info._e.delta // 5)
        elif self.dom_node.styles.overflow_y == css.Overflow.scroll:
            self.own_composite.scroll_y(-e.info._e.delta // 5)  
        else:
            if self.master_composite is None:return
            self.master_composite.composited_element._scroll_event_handler(e)
        # Over here we can always check if the scroll must really be done or not depenin

    def __eq__(self, other):
        return other is self      

    def remove(self):
        '''Removes the element from the render tree and removes the element visually'''
        if self.own_composite is not None:
            self.own_composite.canvas.unbind_all(ALL)
            self.own_composite.composited_element = None
            self.own_composite.canvas.forget()
        if self.master is not None:
            self.master.remove_slave(self, self.dom_node.styles.z_index if self.dom_node.styles.z_index is not None else 1)
        if self.render_information.context is not None:
            self.master_composite.delete_element(self.render_information.context)


        self.dom_node = None
        self.closest_relative = None
        self.master = None
        self.render_information.context = None
        self._units.clear()
        self.render_information = None
        self.layout_information = None
        self._window_provider = None
        
        self.master_composite = None
        self.own_composite = None

    def repaint(self):
        ''''
        Paints the element and its children again
        NOTE: This is different from paint (this simply updates whatever was already present on the screen)
        '''
        if self.dom_node is None:return
        if not self.dom_node._visible:return


        if self.render_information.context is None: # The subtree hasnt been painted yet
            self.paint(self.master.master_composite if not self.master.needs_composite else self.master.own_composite)
            return

        self._set_render_information()

        if self.needs_composite:
            self.master_composite.update_composite_element(self)
            
        else:
            if self.master_composite is None:return

            self.master_composite.update_box_element(self.render_information)


        for z_index in self.slaves:
            for slave in self.slaves[z_index]:
                slave.repaint()

    def request_reflow(self):
        '''
        Puts a reflow request to the layout manager
        '''
        self._window_provider.layout_handler.request_service(self)

    def after_layout(self):
        '''
        Function called after initial size has been set
        '''
        pass

RenderNode.__register_serializer__()
RenderNode.__register_deserializer__()