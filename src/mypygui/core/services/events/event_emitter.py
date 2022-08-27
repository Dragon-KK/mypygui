from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .event import Event
    from ....page.objects import DOMNode

class EventEmitter:
    def __init__(self, target : DOMNode, event_handler : EventHandler = None, never_propogate = False):
        self.target = target
        self.event_handler = event_handler

        self.never_propogate = never_propogate

        self.disabled = False

        self.subscribers : dict[Events, Tuple[callable, bool]] = {}
        '''the callback and whether child events should be notified too'''

    def subscribe(self, event : Events, callback : callable, notify_child_events = True):
        if self.subscribers.get(event) is None:
            self.subscribers[event] = []
        self.subscribers[event].append((callback, notify_child_events))

    def dispatch(self, event : Event):
        '''Dispatches an event'''
        self.event_handler.request_dispatch(self, event)

    def _dispatch(self, event : Event):
        '''Dispatches an event'''
        if self.disabled:return
        self.emit(event)
        self.propogate(event)

    def emit(self, event : Event):
        '''Emits the event to all that subscribed to it'''
        is_child_event = event.target != self.target
        for subscriber in self.subscribers.get(event.type, ()):
            if (not is_child_event) or subscriber[1]:subscriber[0](event)

    def propogate(self, event : Event):
        '''Propogates the event to parent event emitter'''
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