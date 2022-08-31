import PIL.Image
import PIL.ImageTk
from math import ceil
from ...logging import console

class Image:
    '''Ye'''
    def __init__(self, image : PIL.Image.Image):
        self.true_image = image
        self.true_size = image.size

        self.photo_image = PIL.ImageTk.PhotoImage(image)
        self.size = self.true_size

    def resize(self, new_width, new_height):
        new_width = ceil(new_width)
        new_height = ceil(new_height)
        if self.size == (new_width, new_height):return
        if self.true_size == (new_width, new_height):
            self.photo_image = PIL.ImageTk.PhotoImage(self.true_image)
            self.size = self.true_size
            return
        
        self.photo_image = PIL.ImageTk.PhotoImage(self.true_image.resize((new_width, new_height)))
        self.size = (new_width, new_height)

    def __repr__(self):
        return f'<Image size = {self.size} true_size = {self.true_size}>'

    @staticmethod
    def handle_resource_request(data):
        from io import BytesIO
        try:
            return PIL.Image.open(BytesIO(data))
        except:
            console.warn('Image data did not come :(')
            return PIL.Image.new('RGB', (0, 0))