from __future__ import annotations
from ...asynchronous import asyncify, Promise
from .composite import Composite
from ....util import Object
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....page.objects import RenderNode, RootRenderNode
    from ..layout_managing import LayoutHandler

import ctypes 
ctypes.windll.shcore.SetProcessDpiAwareness(True)

class WindowProvider: # Does this need to be a service provider? 
    def __init__(self, layout_handler : LayoutHandler):
        self.ended = Promise()
        '''Promise that is fulfilled when the SeviceProvider is ended'''
        self.info = Object()
        '''Contains info about the window size and position etc'''
        self.layout_handler = layout_handler
        '''Reference to the layout handler'''
        self.layout_handler.window_provider = self # Give reference of the window provider to the layout handler

    def reset(self, root_render_node : RootRenderNode): # Resets the window provider
        '''Resets the window providers'''
        self.main_composite.canvas.forget()
        self.main_composite.canvas.destroy()
        del self.main_composite.canvas
        del self.main_composite

        canvas = tk.Canvas(self.root, highlightthickness=0, borderwidth=0, yscrollincrement=1)
        canvas.place(relx=0,rely=0,relheight=1,relwidth=1)

        self.main_composite = Composite(canvas, root_render_node, listen_keyboard=True)

    @lambda func:asyncify(func, 'WindowProvider')
    def run(self):
        '''Runs the mainloop'''
        self.root = tk.Tk()
        '''tkinter root'''
        self.root.geometry('915x400')
        # self.root.call('tk', 'scaling', 10.0)
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        
        canvas = tk.Canvas(self.root,closeenough=0, highlightthickness=0, borderwidth=0, yscrollincrement=1, xscrollincrement=1, background='#ffffff')
        canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.main_composite = Composite(canvas, None)

        self.root.mainloop()

    def end(self, reason = 'gui'):
        '''Ends the window provider'''
        self.ended.resolve(reason)
        self.root = None

    def update_info(self):
        '''Updates the info about the window'''
        self.root.update()
        self.info.width = self.root.winfo_width()
        self.info.height = self.root.winfo_height()
        self.info.x_pos = self.root.winfo_x()
        self.info.y_pos = self.root.winfo_y()

    def set_title(self, title : str):
        '''Sets the title to the window'''
        self.root.title(title)

    def call(self, func : callable, args = (), kwargs = {}):
        '''Runs a given function in the tkinter mainloop'''
        self.root.after(0, lambda:func(*args, **kwargs))
        self.root.update_idletasks() # This makes things smooooooooth ;)