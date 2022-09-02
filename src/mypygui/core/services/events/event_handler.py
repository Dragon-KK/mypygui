from __future__ import annotations
from ..service_provider import ServiceProvider
from ....core.asynchronous import Promise
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .event_emitter import EventEmitter
    from .event import Event

class EventHandler(ServiceProvider):
    '''Handles dom events'''

    def _on_idle(self):
        self.acknowledged_requests.clear()
        self.next_request_key = 0

    def request_dispatch(self, event_emitter : EventEmitter, event : Event):
        '''
        Requests for an event to be dispatched
        Parameters:
            event_emitter : EventEmitter
                The event emitter that requested dispatch
            event : Event
                The event
        '''
        self.request_service(event_emitter, event)

    def _provide_service(self, request_key, args : tuple, promise : Promise):
        try:
            result = args[0]._dispatch(args[1])
            if promise.state != Promise.ONGOING:return
            promise.resolve(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            # promise.cancel(e)