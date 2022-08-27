from ..asynchronous import asyncify, Promise, Signal
from typing import Tuple
from collections import deque

InvalidRequestKeyPromise = Promise()
InvalidRequestKeyPromise.cancel('Invalid Request (key)')

class ServiceProvider:
    '''A model for objects that provide some essential service asynchronously'''
    def __init_subclass__(cls):
        cls.run = asyncify(cls.run, cls.__name__)

    def __init__(self):
        self.requests : deque[int] = deque()
        '''A deque of request_keys'''
        self.acknowledged_requests : dict[int, Tuple[any, Promise]] = {}
        '''A dectionary mapping request_keys to a tuple containing the request args and the promise'''

        self.next_request_key = 0
        '''The default internal counter for requests'''

        self.ended = Promise()
        '''Promise that is fulfilled when the SeviceProvider is ended'''
        self.requests_pending = Signal()
        '''Set to true to start working'''

    def reset(self, cancel_pending = True):
        '''
        Clears pending requests and resets any counters etc
        NOTE: Set cancel_pending to False if pending requests are to be ignored (otherwise they will be cancelled)
        '''
        self.requests.clear()
        self.requests_pending.clear()
        self.next_request_key = 0
        promises = list(self.acknowledged_requests.values()) if cancel_pending else []
        self.acknowledged_requests.clear()

        for args, promise in promises: # Cancel all pending requests
            if promise.state == Promise.ONGOING:promise.cancel('reset')

    def run(self):
        '''Runs the service provider'''
        def runner():
            while self.requests: # While we still have requests
                request_id = self.requests.popleft()
                args, promise = self.acknowledged_requests[request_id]
                if promise.state != Promise.ONGOING:
                    # Maybe the request was cancelled, then just continue
                    continue
                self._provide_service(request_id , args, promise) # Provide the service
                if self.ended.state != Promise.ONGOING:break # Check if we need to break

        while self.ended.state == Promise.ONGOING:        
            if self.ended.state != Promise.ONGOING:break # Check if we need to break
            self.requests_pending.clear() # Clear the signal
            runner() # Handle all requests
            if self.ended.state != Promise.ONGOING:break # Check if we need to break
            self._on_idle()
            self.requests_pending.wait() # Wait for requests to come

    def end(self):
        '''Stops execution of the service provider'''
        self.ended.resolve(True)
        self.requests_pending.set()

    def request_service(self, *args) -> Promise:
        '''Request a service'''
        request_key = self._get_request_key(args)
        if request_key is None:
            return InvalidRequestKeyPromise
        if self.acknowledged_requests.get(request_key) is not None: # If a similar request was already made, just return that promise
            return self.acknowledged_requests[request_key][1]
        promise = Promise()
        self.acknowledged_requests[request_key] = (args, promise) # Acknowledge the request
        self.requests.append(request_key) # Add our request to our queue
        if not self.requests_pending.is_set():self.requests_pending.set() # A new request was made
        return promise # Return the promise

    def _get_request_key(self, args) -> int:
        '''
        Returns a key unique to the request (to group same requests)
        NOTE: Return None if the request is to be rejected
        '''
        key = self.next_request_key
        self.next_request_key += 1
        return key

    def _on_idle(self):
        '''
        Function is called whenever the service provider goes idle
        '''
        return

    def _provide_service(self, request_id : int, args : any, promise : Promise):
        '''
        Handles a singular service request
        NOTE: The promise must be resolved / cancelled as needed in this function
        NOTE: The acknowledged request must manually be deleted if needed
        '''
        pass