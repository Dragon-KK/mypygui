from __future__ import annotations
from .node import RenderNode
from .layouting import layouter
from .....core.services.events import Event
from .... import css

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...dom import RootDOMNode
    from .....core.services.rendering import WindowProvider

class RootRenderNode(RenderNode):
    __ignore__ = {'dom_node', 'slaves', 'master'}
    def __init__(self, dom_node : RootDOMNode):
        super().__init__(dom_node)
        self.closest_relative = self
        self.dom_node : RootDOMNode
        self._window_provider : WindowProvider = None

        
    def set_units(self):
        '''Sets the multipliers of css units'''
        # LIMIT: rem and em are like useless rn
        self._units[css.Unit.em] = 21 # For now it is hardset
        self._units[css.Unit.rem] = 21
        self._units[css.Unit.viewport_height] = self.layout_information.height / 100
        self._units[css.Unit.viewport_width] = self.layout_information.width / 100
        self._units[css.Unit.self_height] = self.layout_information.height / 100
        self._units[css.Unit.self_width] = self.layout_information.width / 100

    def set_heirarchy(self):
        '''Sets the heirarchy of all elems'''
        for child in self.dom_node.children:
            child.render_node.set_heirarchy(self, self)

    def _set_layout_information(self):
        self.layout_information.reset()
        self._window_provider.update_info()
        self.layout_information.width = self._window_provider.info.width
        self.layout_information.height = self._window_provider.info.height
        self.layout_information.content_height = self._window_provider.info.height
        self.layout_information.content_width = self._window_provider.info.width
        self.layout_information.content_size_height = self._window_provider.info.height
        self.layout_information.content_size_width = self._window_provider.info.width

    def layout(self, skip_node = None):
        '''Does the initial layouting of the dom tree'''
        self._set_layout_information()
        self.set_units()
        width, height = layouter.layout_children(self, self.layout_information.content_width, skip_node=skip_node)
        self.layout_information.content_width = width
        self.layout_information.content_height = height
        self.layout_information.content_size_height = height
        self.layout_information.content_size_width = width

    def _set_render_informaiton(self):
        '''Sets the render information using the layout information and styles'''
        self.render_information.background_color = self.dom_node.styles.background_color
        self.render_information.height = self.layout_information.height
        self.render_information.width = self.layout_information.width

    def paint(self):
        '''Paints the thing onto the thingy'''
        self._set_render_informaiton()
        if self.dom_node is None:return
        self.dom_node.event_emitter.subscribe(Event.Types.scroll, lambda e:self._scroll_event_handler(e))
        self.own_composite = self._window_provider.main_composite
        self.own_composite.canvas.bind('<MouseWheel>', lambda e:self.dom_node.event_emitter.dispatch(Event(Event.Types.scroll, self.dom_node, False, _e = e)) if self.dom_node else 0)
        self._window_provider.main_composite.canvas.bind('<Configure>', lambda e:self.dom_node.event_emitter.dispatch(Event(Event.Types.resize, self.dom_node, False, _e = e)) if self.dom_node else 0)
        self.dom_node.event_emitter.subscribe(Event.Types.resize, lambda e:self.request_reflow())
        
        self._window_provider.main_composite.canvas.config(bg=self.render_information.background_color, scrollregion=(0, 0, self.layout_information.content_size_width, self.layout_information.content_size_height))
        for z_index in self.slaves:
            for slave in self.slaves[z_index]:
                slave.paint(self._window_provider.main_composite)

    def reflow(self, skip_element = None):
        '''The bane of my existence'''
        self.layout(skip_element)
        return self
        
    def repaint(self):
        ''''
        Paints the element and its children again
        NOTE: This is different from paint (this simply updates whatever was already present on the screen)
        '''
        self._set_render_informaiton()
        if self.dom_node is None:return
        self._window_provider.main_composite.canvas.config(bg=self.render_information.background_color, scrollregion=(0, 0, self.layout_information.content_size_width, self.layout_information.content_size_height))
        for z_index in self.slaves:
            for slave in self.slaves[z_index]:
                slave.repaint()
RootRenderNode.__register_serializer__()
RootRenderNode.__register_deserializer__()