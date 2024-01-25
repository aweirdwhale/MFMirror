# spinning_image.py

from PIL import Image, ImageTk

class SpinningImage:
    def __init__(self, canvas):
        self.canvas = canvas
        self.image_label = None

    def update_thumbnail(self, thumbnail_path):
        img = Image.open(thumbnail_path).convert("RGBA")
        img = img.resize((80, 80), Image.ANTIALIAS)

        image_tk = ImageTk.PhotoImage(img)

        if self.image_label:
            self.canvas.delete(self.image_label)

        self.image_label = self.canvas.create_image(40, 40, image=image_tk)
        self.canvas.image = image_tk
