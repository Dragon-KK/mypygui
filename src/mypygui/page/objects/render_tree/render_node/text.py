from __future__ import annotations
from .node import RenderNode
from tkinter.font import Font
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .....core.services.rendering import Composite

from .....core.services.events import Event

class TextRenderNode(RenderNode):
    '''Deals with thte layouting and painting of text'''
    __ignore__ = {'dom_node', 'slaves', 'master'}
    def paint(self, composite : Composite):
        '''Paints the thing onto the thingy'''
        if self.dom_node is None or not self.dom_node._visible:return
        
        self._set_render_information()
        
        self.render_information.context = composite.create_txt_element(self.render_information, self.dom_node.content)
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-1>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-2>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-3>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<ButtonRelease>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_up, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Motion>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_over, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Enter>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.enter, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Leave>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.leave, self.dom_node, True, _e = e)))

        self.master_composite = composite
    def repaint(self):
        ''''
        Paints the element and its children again
        NOTE: This is different from paint (this simply updates whatever was already present on the screen)
        '''
        if self.dom_node is None or not self.dom_node._visible:return

        if self.render_information.context is None: # The subtree hasnt been painted yet
            self.paint(self.master.master_composite if not self.master.needs_composite else self.master.own_composite)
            return
        if self.render_information.context.txt_token == -1:
            self.master_composite.delete_element(self.render_information.context)
            self.paint(self.master_composite)
            return
        self._set_render_information()

        self.master_composite.update_txt_element(self.render_information, self.dom_node.content)


    def __init__(self, *args, **kwargs):
        # LIMIT: Figure out a way to auto detect line breaks
        super().__init__(*args, **kwargs)
        self.font = Font()