from __future__ import annotations
from .node import RenderNode

from typing import TYPE_CHECKING
from ...image_container import Image
if TYPE_CHECKING:
    from .....core.services.resources import Resource
    from .....core.services.rendering import Composite

from .....core.services.events import Event

class ImageRenderNode(RenderNode):
    '''Deals with the layouting and painting of images'''
    __ignore__ = {'dom_node', 'slaves', 'master'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image : Image = None
        if self.dom_node.image is not None:
            def set_image(r):
                self.image = Image(r)
                if self.render_information is None:return
                if self.render_information.context is not None: # If the image was loaded after the initial paint we must update the image
                    self.after_layout() # LIMIT: Move this to the layouting stage cause this will cause slowdowns (will it tho? cause the promise is fulfilled in the resource request loop)
                    
                    self.repaint()
            self.dom_node.image.then(set_image)

    def remove(self):
        super().remove()
        self.image = None

    def paint(self, composite : Composite):
        '''Paints the thing onto the thingy'''
        if self.dom_node is None or not self.dom_node._visible:return
        
        self._set_render_information()
        
        if self.needs_composite:
            raise NotImplementedError('Composites not allowed currently for images')
        else:
            if self.image is None:
                self.render_information.context = composite.create_box_element(self.render_information)
            else:
                self.render_information.context = composite.create_img_element(self.render_information, self.image)

        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-1>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-2>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Button-3>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.click, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<ButtonRelease>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_up, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Motion>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.mouse_over, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Enter>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.enter, self.dom_node, True, _e = e)))
        composite.canvas.tag_bind(self.render_information.context.bnd_token, '<Leave>', lambda e: self.dom_node.event_emitter.dispatch(Event(Event.Types.leave, self.dom_node, True, _e = e)))

        self.master_composite = composite

        # img is not allowed to have slaves
        # for z_index in self.slaves:
        #     for slave in self.slaves[z_index]:
        #         slave.paint(composite)

    def repaint(self):
        ''''
        Paints the element and its children again
        NOTE: This is different from paint (this simply updates whatever was already present on the screen)
        '''
        if self.dom_node is None or not self.dom_node._visible:return

        if self.render_information.context is None: # The subtree hasnt been painted yet
            self.paint(self.master.master_composite if not self.master.needs_composite else self.master.own_composite)
            return
        if self.render_information.context.img_token == -1 and self.image is not None:
            self.master_composite.delete_element(self.render_information.context)
            self.paint(self.master_composite)
            return

        self._set_render_information()

        if self.needs_composite:
            raise NotImplementedError('Composites not allowed currently')
        else:
            if self.image is None:
                if self.master_composite is None:return
                self.master_composite.update_box_element(self.render_information)
            else:
                if self.master_composite is None:return
                self.master_composite.update_img_element(self.render_information, self.image)
        
        # img is not allowed to have slaves
        # for z_index in self.slaves:
        #     for slave in self.slaves[z_index]:
        #         slave.repaint()

    def after_layout(self):
        if self.image is None:return
        self.image.resize(self.layout_information.width, self.layout_information.height)