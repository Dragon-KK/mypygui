'''Some common functionality'''

from . import exceptions

#region general
identity_function = lambda n:n
'''Returns exactly what has been given (expects only a single element)'''

null_function = lambda *args,**kwargs:None
'''Does nothing takes in as many arguments'''
#endregion

#regions checksums
def assert_keys(
    dictionary : dict, # the object to check (must have a `get` function that returns none if the property doesnt exists)
    required_keys : list,  # a list of the required properties on the object
    exception = exceptions.MissingKeyException, # the exception that is raised if the key doesnt exist
    raise_exception = True,  # set to false if an exeption shouldnt be raised
    on_exeption = null_function, # a callback called before raising the exception (ideally to only be used when raise_exception is set to false)
    object_name = 'dict' # the name of the object being checked
):
    '''checks if the given keys exist on the given object'''
    for key in required_keys:
        if dictionary.get(key) is none:
            on_exeption(key)
            if raise_exception:raise exception(object_name=object_name, property_name=key)
    return True
#endregion

#region typecasting
def try_float(n : str, default = None):
    try:
        return float(n)
    except:
        return default

# def camel_case(s):
#     #https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-96.php
#     s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
#     return ''.join([s[0].lower(), s[1:]])

def snake_case(s : str):
    '''
    Converts a hiphen case string to its snake case form
    eg : `background-color` -> `background_color`
    '''
    return s.lower().replace('-', '_')
#endregion

#region misc
def traverse_tree(node : 'TreeLike', func : callable, args = None, parent = None):
    '''
    Allows for traversal on a tree like structure
    NOTE: func should take in three arguments : (node, parent, args). 
        `parent` being the parent of the `node`
        `args` being the result of the parent's call
    NOTE: Return None to skip children
    '''
    res = func(node, parent, args)
    if res is None or not node.children:
        return res
    for i in node.children:
        traverse_tree(i, func, args, node)
#endregion