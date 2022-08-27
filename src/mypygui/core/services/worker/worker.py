from __future__ import annotations
from ..service_provider import ServiceProvider

class Worker(ServiceProvider):

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

    def request_service(self, work : callable, args = (), kwargs = {}) -> Promise:
        '''Request a service'''
        request_key = self._get_request_key(args)
        if request_key is None:
            return InvalidRequestKeyPromise
        promise = Promise()
        self.acknowledged_requests[request_key] = ((work, args, kwargs), promise) # Acknowledge the request
        self.requests.append(request_key) # Add our request to our queue
        if not self.requests_pending.is_set():self.requests_pending.set() # A new request was made
        return promise # Return the promise

    def _on_idle(self):
        '''
        Function is called whenever the service provider goes idle
        '''
        self.reset()

    def _provide_service(self, request_id : int, args : any, promise : Promise):
        '''
        Handles a singular service request
        NOTE: The promise must be resolved / cancelled as needed in this function
        NOTE: The acknowledged request must manually be deleted if needed
        '''
        del self.acknowledged_requests[request_id]
        try:
            result = args[0](*args[1], **args[2])
            promise.resolve(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            promise.cancel(e)