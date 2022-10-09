from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...src.mypygui.page.py_component import PyComponent

class PySVG(PyComponent):
    def on_paint(self):
        pass
        

def register_component(handler):
    handler['svg'] = PySVG