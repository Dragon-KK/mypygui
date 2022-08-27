class MissingKeyException(Exception):
    '''Exception raised when a required property is missing on an object'''
    def __init__(self, object_name = 'dict', property_name = 'unkown'):
        super().__init__(f"Missing key `{property_name}` on `{object_name}`")

class UnexpectedPropertyTypeException(Exception):
    '''Exception raised when a property isnt of the expected type'''
    def __init__(self, object_name = 'dict', property_name = 'unknown', expected_type = None, recieved_type = None):
        super().__init__(f"Expected type `{expected_type}` for `{property_name}` on `{object_name}`. Recieved `{recieved_type}` instead")