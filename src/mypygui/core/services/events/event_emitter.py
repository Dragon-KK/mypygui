from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .event import Event
    from ....page.objects import DOMNode

class EventEmitter:
    def __init__(self, target : DOMNode, event_handler : EventHandler = None, never_propogate = False):
        self.target = target
        '''The target of the event emitter (the one who emits the events)'''
        self.event_handler = event_handler
        '''Reference to the event_handler (in order to emit events)'''

        self.never_propogate = never_propogate
        '''Set to True in order to never propogate events that are in the normal direction'''

        self.disabled = False
        '''Set to True in order to stop emitting events'''

        self.subscribers : dict[Event.Types, Tuple[callable, bool]] = {}
        '''The callback and whether child events should be notified too'''

    def subscribe(self, event_type : Event.Types, callback : callable, notify_child_events = True):
        '''
        Subscribe to the events of a particular type
        Parameters:
            event_type : Event.Types
                The type of the event to subcribe to
            callback : (event) → None
                The function that should be called when the event is emitted
            notify_child_events : bool
                Set to True in order to get notified by events emitted by children also
        '''
        if self.subscribers.get(event) is None:
            self.subscribers[event] = []
        self.subscribers[event].append((callback, notify_child_events))

    def dispatch(self, event : Event):
        '''
        Dispatches an event (by requesting it to the event_handler)
        Parameters:
            event : Event
                The event
        '''
        self.event_handler.request_dispatch(self, event)

    def _dispatch(self, event : Event):
        '''
        Dispatches an event (by calling emit and propogate)
        Parameters:
            event : Event
                The event
        '''
        if self.disabled:return
        self.emit(event)
        self.propogate(event)

    def emit(self, event : Event):
        '''
        Emits the event to all that subscribed to it
        Parameters:
            event : Event
                The event
        '''
        is_child_event = event.target != self.target
        for subscriber in self.subscribers.get(event.type, ()):
            if (not is_child_event) or subscriber[1]:subscriber[0](event)

    def propogate(self, event : Event):
        '''
        Propogates the event to parent event emitter (or to children if opposite direction is set to true on the event)
        Parameters:
            event : Event
                The event
        '''
        if (self.never_propogate and not event.opposite_direction) or (not event.propogate) or self.target is None: # or (self.target.styles.position == css_literals.Position.absolute or self.target.styles.position == css_literals.Position.fixed)
            return

        if not event.opposite_direction:
            if self.target is None or self.target.parent is None:return
            self.target.parent.event_emitter.emit(event) # Emits the event
            if self.target is None or self.target.parent is None:return
            self.target.parent.event_emitter.propogate(event) # Propogates the event if needed
            return
        
        if self.target is None:return
        for child in self.target.children:
            child.event_emitter.emit(event)
            child.event_emitter.propogate(event)