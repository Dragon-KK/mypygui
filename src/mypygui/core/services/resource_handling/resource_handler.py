from ..service_provider import ServiceProvider
from ....util import functions
from ....core import fs
from ....core.asynchronous import Promise

class ResourceHandler(ServiceProvider):
    '''Handles loading and releasing of resources'''
    def __init__(self):
        super().__init__()
        self.persisted_keys = set()
        '''The set of all keys that were marked to persist between page loads'''

    def request_resource(self, uri : fs.URI = None, file_type : fs.FileType = None, resource_key = None, data_resolver = functions.identity_function, persist = False) -> Promise:
        '''
        Requests a resource
        Parameters:
            uri : fs.URI
                The uri that needs to be loaded
            file_type : fs.FileType
                The file type of the resource
            resource_key
                A backup resource_key just in case a resource key could not be made from the uri (will never happen)
            data_resolver : (data) → any
                A function that will modify the data to a more usable form
            persist : bool
                Set persist to true to allow a resource to persist between page loads
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
            promise.cancel(e)

    def reset(self):
        '''
        Clears pending requests and resets any counters etc
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
        '''Releases all resources (including persisted resources)'''
        self.persisted_keys.clear()
        for key in self.acknowledged_requests:
            self.release_resource(key)
        

    def release_resource(self, request_key):
        '''
        Releases a persisted resource given the resource key
        NOTE: It is not recommended to use this
        Parameters:
            resource_key (use ResourceHandler._get_request_key to get this)
        '''
        if self.acknowledged_requests.get(request_key) is None:
            return
        if self.acknowledged_requests[request_key][1].state == Promise.ONGOING:
            self.acknowledged_requests[request_key].cancel('released')
        else:
            self.persisted_keys.remove(request_key)
            self.acknowledged_requests[request_key][1].result = None # This seems to help with garbage collection
            
            del self.acknowledged_requests[request_key]
