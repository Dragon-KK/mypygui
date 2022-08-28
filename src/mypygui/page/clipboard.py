class ClipBoard:
    def __init__(self, root):
        self.__root = root

    def get(self):
        try:
            return self.__root.clipboard_get()
        except:
            return ''

    def set(self, text, additive = False):
        if not additive:self.__root.clipboard_clear()
        self.__root.clipboard_append(text)