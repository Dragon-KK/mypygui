from __future__ import annotations
from ..service_provider import ServiceProvider
from ....page.objects.render_tree.render_node.layouting import layouter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...asynchronous import Promise
    from ..rendering import WindowProvider

class LayoutHandler(ServiceProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_provider : WindowProvider = None

    def _get_request_key(self, args):
        return id(args[0])

    def _provide_service(self, request_key, args : tuple, promise : Promise):
        del self.acknowledged_requests[request_key]
        try:
            to_be_painted_element = layouter.reflow_node(args[0])
            self.window_provider.call(to_be_painted_element.repaint)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)