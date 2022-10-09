from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...src.mypygui.page.py_component import PyComponent

class PySVG(PyComponent):
    def on_paint(self):
        for i in self.children:
            i.image = self.dom_node.render_node.own_composite.canvas.create_oval(10, 10, *(self.render_node.get_value(eval(j), 1) for j in i.content.split('|')))
        
    def on_repaint(self):
        for i in self.children:
            self.dom_node.render_node.own_composite.canvas.coords(i.image, 10, 10, *(self.render_node.get_value(eval(j), 1) for j in i.content.split('|')))

def register_component(handler):
    handler['svg'] = PySVG