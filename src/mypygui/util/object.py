from types import SimpleNamespace
from .functions import identity_function   
  
class Object(SimpleNamespace):
    '''Scuffed Object implementation'''
    __iterables__ = {'set', 'tuple', 'list'}
    '''All the recognized iterables'''
    __serializers__ = {
        'set' : lambda v:{'__objecttype__' : 'set', 'set' : list(v)},
        'tuple' : lambda v:{'__objecttype__' : 'tuple', 'tuple' : list(v)},
        'list' : lambda v:{'__objecttype__' : 'list', 'list' : list(v)},
    }
    '''A dict specifying serializers for a given type'''
    __deserializers__ = {
        'set' : lambda v:set(v),
        'tuple' : lambda v:tuple(v),
        'list' : lambda v:list(v)
    }
    '''A dict specifying deserializer for a given type'''
    __ignore__ = set()
    '''A set of keys to ignore while serializing'''

    __ignorenull__ = False
    '''Should we ignore null properties while serializing?'''
    __null__ = None
    '''If the value of a property is __null__ the property is ignored'''

    def __getattr__(self, name : str):
        return None

    def get(self, name : str):
        '''Gets an item'''
        return self.__getattribute__(name)

    def set(self, name : str, value : any):
        '''Sets an item'''
        self.__dict__[name] = value

    @classmethod
    def __register_deserializer__(cls, custom = None, deserializer = None):
        '''Registers a deserializer for a type'''
        cls = cls if custom is None else custom
        deserializer = cls.__from_json__ if deserializer is None else deserializer
        Object.__deserializers__[cls.__name__] = lambda d:deserializer(d) # Idk why this is anonumous but ok

    @classmethod
    def __register_serializer__(cls, custom : type = None, serializer = None):
        '''Registers a serializer for a type'''
        cls = cls if custom is None else custom
        serializer = cls.__serialize__ if serializer is None else serializer
        Object.__serializers__[cls.__name__] = serializer

    @staticmethod
    def __register_iterable__(iterableName : str):
        '''Marks the object as an iterable object'''
        Object.__iterables__.add(iterableName)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __serialize__(self):
        '''Returns a dictionary of all the properties on the object (use this when keeping track of class is important)'''
        def getVal(value):
            if issubclass(value.__class__, Object):
                return Object.__serializers__.get(value.__class__.__name__, Object.__serialize__)(value)
            elif value.__class__.__name__ in Object.__iterables__:
                return Object.__serializers__.get(value.__class__.__name__, Object.__serialize__)(
                    getVal(i) for i in value
                )
            else:
                return Object.__serializers__.get(value.__class__.__name__, identity_function)(value)
        serialized = {}
        for key,value in self.__dict__.items():
            if key in self.__ignore__:continue
            if self.__ignorenull__ and value == self.__null__:continue
            serialized[key] = getVal(value)
        return {
            '__objecttype__' : self.__class__.__name__,
            self.__class__.__name__ : serialized
        }

    @classmethod
    def __from_json__(cls, dictionary : dict):
        '''Parses the object from a dict (the root being unserialized)'''
        kwargs = {}
        def parseValue(value):
            if type(value) == dict and value.get('__objecttype__'):
                if value['__objecttype__'] in Object.__iterables__:
                    return Object.__deserializers__.get(value['__objecttype__'], list)(
                        parseValue(i) for i in value.get(value['__objecttype__'], [])
                    )
                else:
                    return Object.__deserializers__.get(value['__objecttype__'], Object.__from_json__)(value.get(value['__objecttype__'], {}))

            else:
                return Object.__deserializers__.get(type(value).__name__, identity_function)(value)
        for key, value in dictionary.items():
            kwargs[key] = parseValue(value)

        return cls(**kwargs)

    @classmethod
    def __deserialize__(cls, dictionary : dict, guessType = True):
        '''Constructs an Object out of a serialized object'''
        kwargs = {}
        clsname = dictionary['__objecttype__']
        deserializer = Object.__deserializers__.get(clsname, cls.__deserialize__) if guessType else cls.__deserialize__

        return deserializer(dictionary[clsname])

# Registering Object
Object.__register_serializer__()
Object.__register_deserializer__()

