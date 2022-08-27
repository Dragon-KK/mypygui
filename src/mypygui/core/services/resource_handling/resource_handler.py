from ..service_provider import ServiceProvider
from ....util import functions
from ....core import fs
from ....core.asynchronous import Promise

class ResourceHandler(ServiceProvider):
    '''Handles loading and releasing of resources'''
    def __init__(self):
        super().__init__()
        self.persisted_keys = set()

    def request_resource(self, uri : fs.URI = None, file_type : fs.FileType = None, resource_key = None, data_resolver = functions.identity_function, persist = False) -> Promise:
        '''
        Requests a resource
        NOTE: Set persist to true to allow a resource to persist between page changes
        '''
        return self.request_service(uri, file_type, resource_key, data_resolver, persist)
        # We want resource manager to just store the loaded resource

    def _get_request_key(self, args):
        # args[0] -> uri
        # args[1] -> resource_key
        return (args[0].host + str(args[0].path)) if args[0] is not None else args[2]

    def _provide_service(self, request_key, args : tuple, promise : Promise):
        try:
            resource = args[3](
                # The uri, filetype
                fs.load(args[0], args[1])
            )
            if args[4]:
                self.persisted_keys.add(request_key)
            if promise.state != Promise.ONGOING:return
            promise.resolve(resource)
        except Exception as e:
            import traceback
            traceback.print_exc()
            # promise.cancel(e)

    def reset(self):
        '''
        Clears pending requests and resets any counters etc
        NOTE: Set cancel_pending to False if pending requests are to be ignored (otherwise they will be cancelled)
        '''
        self.requests.clear()
        self.requests_pending.clear()
        self.next_request_key = 0
        for key in list(self.acknowledged_requests.keys()):
            if key in self.persisted_keys:
                continue
            #if self.acknowledged_requests[key][1].state == Promise.ONGOING:self.acknowledged_requests[key][1].cancel('reset')
            del self.acknowledged_requests[key]
        

    def release_all_resources(self):
        '''Releases all persisted resources'''
        self.persisted_keys.clear()
        for key in self.acknowledged_requests:
            self.release_resource(key)
        

    def release_resource(self, request_key):
        '''Releases a persisted resource given the resource key'''
        if self.acknowledged_requests.get(request_key) is None:
            return
        if self.acknowledged_requests[request_key][1].state == Promise.ONGOING:
            self.acknowledged_requests[request_key].cancel('released')
        else:
            self.persisted_keys.remove(request_key)
            self.acknowledged_requests[request_key][1].result = None # This seems to help with garbage collection
            
            del self.acknowledged_requests[request_key]
