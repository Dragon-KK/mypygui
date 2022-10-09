from __future__ import annotations
from .node import RenderNode

from typing import TYPE_CHECKING
from ...image_container import Image
if TYPE_CHECKING:
    from .....core.services.resources import Resource
    from .....core.services.rendering import Composite

from .....core.services.events import Event

class PyComponentRenderNode(RenderNode):
    '''Deals with the layouting and painting of images'''
    __ignore__ = {'dom_node', 'slaves', 'master'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.needs_composite = True

    def remove(self):
        super().remove()

    def paint(self, composite : Composite):
        '''Paints the thing onto the thingy'''
        if self.dom_node is None:return
        if not self._scroll_listener_is_set:
            self.dom_node.event_emitter.subscribe(Event.Types.scroll, lambda e:self._scroll_event_handler(e))
            self._scroll_listener_is_set = True
        if not self.dom_node._visible:return
        
        self._set_render_information()
        
        self.master_composite = composite
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

        self.dom_node.component.on_paint()

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

        self.master_composite.update_composite_element(self)

        self.dom_node.component.on_repaint()
            

    def after_layout(self):
        self.dom_node.component.on_layout()

PyComponentRenderNode.__register_serializer__()
PyComponentRenderNode.__register_deserializer__()