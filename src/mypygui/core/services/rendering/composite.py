from __future__ import annotations
from ....core.services.events import Event
from .context import Context
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....page.objects import Image
    from ....page.objects.render_tree.render_node.information_containers import RenderInformationContainer
    from ....page.objects.render_tree.render_node import RenderNode

class Composite:
    '''
    Deals with painting (and also allows for scrolling)
    NOTE: If overflow is stated in either x or y it is to be explicitly stated for the other too
    '''
    def __init__(self, canvas : tk.Canvas, composited_element : RenderNode, listen_keyboard = False):
        self.canvas = canvas
        self.composited_element = composited_element

        if listen_keyboard:
            self.canvas.focus_set()
            self.canvas.bind('<Key>', lambda e:self.composited_element.dom_node.event_emitter.dispatch(Event(Event.Types.key_press, self.composited_element.dom_node, True, opposite_direction =True, _e = e)))

    def scroll_y(self, amount):
        '''Scrolls in the y direction'''
        self.canvas.yview_scroll(amount, tk.UNITS)
        self.canvas.update_idletasks()

    def scroll_x(self, amount):
        '''Scrolls in the x direction'''
        self.canvas.xview_scroll(amount, tk.UNITS)
        self.canvas.update_idletasks()

    def create_box_element(self, render_information : RenderInformationContainer) -> Context:
        '''Creates a box type of element (box + bounds are drawn)'''
        ctx = Context()
        
        ctx.box_token = self.paint_box(render_information)
        ctx.bnd_token = self.paint_bounds(render_information)

        return ctx

    def update_box_element(self, render_information : RenderInformationContainer):
        '''Updates a box element'''
        self.update_box(render_information)
        self.update_bounds(render_information)

    def create_txt_element(self, render_information : RenderInformationContainer, text : str) -> Context:
        '''Creates a text type of element (text)'''
        ctx = Context()

        ctx.txt_token = self.canvas.create_text(render_information.x,render_information.y,text=text,fill=render_information.foregound_color,font=render_information.font, anchor=tk.NW)
        ctx.bnd_token = ctx.txt_token
        return ctx

    def update_txt_element(self, render_information : RenderInformationContainer, text : str):
        '''Updates a box element'''
        self.canvas.coords(
            render_information.context.txt_token,
            render_information.x, render_information.y
        )
        self.canvas.itemconfig(render_information.context.txt_token,text=text,fill=render_information.foreground_color,font=render_information.font, anchor=tk.NW)

        #self.update_text(render_information)

    def create_img_element(self, render_information : RenderInformationContainer, image : Image) -> Context:
        '''Creates an image type of element (box + image + bounds)'''
        ctx = Context() 
        ctx.img_token = self.paint_image(render_information, image)
        ctx.bnd_token = ctx.img_token # Image is a little spcl

        return ctx

    def update_img_element(self, render_information : RenderInformationContainer, image : Image):
        '''Updates a box element'''
        self.update_image(render_information, image)

    def create_composite(self, node : RenderNode) -> (Composite, Context):
        '''NOTE: Composited elements are treated as box elements but border radius is not applied'''
        ctx = Context()
        canvas = tk.Canvas(scrollregion=(0, 0, max(node.layout_information.content_size_width, 1), max(1, node.layout_information.content_size_height)),closeenough=0,highlightthickness=0, borderwidth=0, yscrollincrement=1, xscrollincrement=1, background=node.render_information.background_color if node.render_information.background_color else 'black')
        ctx.bnd_token = self.canvas.create_window(node.render_information.x, node.render_information.y, window = canvas, width = max(1, node.render_information.width), height = max(1, node.render_information.height), anchor=tk.NW)
        return Composite(canvas, node), ctx

    def update_composite_element(self, node : RenderNode):
        '''Updates the composite'''
        self.canvas.coords(
            node.render_information.context.bnd_token,
            node.render_information.x, node.render_information.y
        )
        self.canvas.itemconfig(node.render_information.context.bnd_token, width = max(1, node.render_information.width), height = max(1, node.render_information.height))
        node.own_composite.canvas.config(scrollregion=(0, 0, max(node.layout_information.content_size_width, 1), max(1, node.layout_information.content_size_height)), background=node.render_information.background_color if node.render_information.background_color else 'black')
    
    def paint_image(self, render_information : RenderInformationContainer, image : Image) -> int:
        return self.canvas.create_image(
            render_information.x, render_information.y, anchor=tk.NW, image = image.photo_image
        )

    def update_image(self, render_information : RenderInformationContainer, image : Image) -> int:
        self.canvas.coords(
            render_information.context.img_token,
            render_information.x, render_information.y
        )
        self.canvas.itemconfig(render_information.context.img_token,image=image.photo_image)


    def paint_box(self, render_information : RenderInformationContainer) -> int:
        return self.canvas.create_polygon(
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width, render_information.y,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y,
            smooth = True,
            width = render_information.border_stroke, fill = render_information.background_color,
            outline = render_information.border_color
        )

    def paint_bounds(self, render_information : RenderInformationContainer) -> int:
        return self.canvas.create_polygon(
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width, render_information.y,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y,
            smooth = True,
            # LIMIT: Dig into how to get the active state (activefill is like a thing)
            width = 0, fill = ''
        )

    def update_box(self, render_information : RenderInformationContainer):
        self.canvas.coords(render_information.context.box_token,
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width, render_information.y,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y            
        )

        self.canvas.itemconfig(
            render_information.context.box_token,
            width = render_information.border_stroke, fill = render_information.background_color,
            outline = render_information.border_color
        )

    def update_bounds(self, render_information : RenderInformationContainer):
        self.canvas.coords( render_information.context.bnd_token,
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.border_top_left_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width - render_information.border_top_right_radius, render_information.y,
            render_information.x + render_information.width, render_information.y,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.border_top_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height - render_information.border_bottom_right_radius,
            render_information.x + render_information.width, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.width- render_information.border_bottom_right_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x + render_information.border_bottom_left_radius, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.height - render_information.border_bottom_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y + render_information.border_top_left_radius,
            render_information.x, render_information.y
        )

    def delete_element(self, context : Context):
        self.canvas.delete(context.bnd_token, context.box_token, context.img_token, context.txt_token)
