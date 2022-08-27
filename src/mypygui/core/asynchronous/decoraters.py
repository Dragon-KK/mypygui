from .async_tools import Promise, asynchronously_run

def thenify(func, name = None):
    '''
    Runs the function on a new thread and returns a promise
    NOTE: The promise will not be provided to the thenified function
    '''
    def thenable(*args, **kwargs) -> Promise:
        promise = Promise()
        def try_fulfill(*args, **kwargs):
            try:
                promise.resolve(func(*args, **kwargs))
            except Exception as e:
                promise.cancel(e)
        asynchronously_run(try_fulfill, args=args, kwargs=kwargs, name=func.__name__ if name is None else name)
        return promise
    return thenable

def promisify(func, name = None):
    '''
    Converts a function into a thenable
    NOTE: The function must take in a parameter called `_promise` which contains the promise that is given in place of the funciton
    NOTE: The function must resolve or cancel the promise on its own
    '''
    def promisable(*args, **kwargs) -> Promise:
        promise = Promise()
        kwargs['_promise'] = promise
        asynchronously_run(func, args=args, kwargs=kwargs, name=func.__name__ if name is None else name)
        return promise
    return promisable

def asyncify(func, name = None):
    '''
    Marks a function to be run asynchronously (does not create any promises)
    '''
    def asyncable(*args, **kwargs):
        asynchronously_run(func, args = args, kwargs = kwargs, name=name)
    return asyncable