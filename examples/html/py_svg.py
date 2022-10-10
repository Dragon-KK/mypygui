from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...src.mypygui.page.py_component import PyComponent
from mypygui.page.css.types import Unit

class PySVG(PyComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for child in self.children:
            child.non_abs_points = []
            for point in child.content.split(','):
                p1, p2 = point.split()
                tmp = p1.split(':')
                p1 = (float(tmp[0]), Unit.str_to_enum(tmp[1]))
                tmp = p2.split(':')
                p2 = (float(tmp[0]), Unit.str_to_enum(tmp[1]))
                child.non_abs_points.extend((p1, p2))

    def set_points(self, child):
        child.points = [self.dom_node.render_node.get_value(p) for p in child.non_abs_points]

    def on_paint(self):
        for child in self.children:
            child.canv_id = self.dom_node.render_node.own_composite.canvas.create_polygon(*child.points, fill='#0f0', splinesteps=32, smooth=True)

        
    def on_layout(self):
        for child in self.children:
            self.set_points(child)

    def on_repaint(self):
        for child in self.children:
            self.dom_node.render_node.own_composite.canvas.coords(child.canv_id, *child.points)

def register_component(handler):
    handler['svg'] = PySVG