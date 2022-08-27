class UnexpectedPromiseResolutionException(Exception):
    '''
    Exception raised when a fulfilled or cancelled promise was asked to resolve or cancle itself
    Parameters:
        promise : Promise
        workDone : 'resolved' | 'cancelled'
        workAsked : 'cancel' | 'resolve'
    '''
    def __init__(self, promise,  work_done, work_asked):
        super().__init__(f"Promise `{promise}` has already been {work_done} but was asked to {work_asked} itself ||| {promise.result}")

class InvalidURISchema(Exception):
    '''Exception raised when a given schema is invalid'''
    def __init__(self, schema):
        super().__init__(f"Invalid uri schema {schema}")