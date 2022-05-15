import os
import random

from PIL import Image, ImageFilter


class ImageChange:
    def __init__(self, date, file):
        self.date = date
        self.file = file
        self.image = Image.open(f'static/inner/{self.date}/{self.file}').convert('RGB')
        os.mkdir(f'static/images/{self.date}')
        self.size = None

    def pixelator(self):
        def pixelate(image, pixel_size=9, draw_margin=True):
            margin_color = (0, 0, 0)

            image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
            image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
            pixel = image.load()

            # Draw black margin between pixels
            if draw_margin:
                for i in range(0, image.size[0], pixel_size):
                    for j in range(0, image.size[1], pixel_size):
                        for r in range(pixel_size):
                            pixel[i + r, j] = margin_color
                            pixel[i, j + r] = margin_color

            return image

        self.image = pixelate(self.image, pixel_size=self.image.size[0] // 100)

    def liner(self):
        pix = self.image.load()
        W, H = self.image.size
        for y in range(H):
            color = random.choice([1, 2, 3])
            for x in range(W):
                r, g, b = pix[x, y]
                if color == 1:
                    pix[x, y] = r + random.randint(1, 250) % 250, g, b,
                elif color == 2:
                    pix[x, y] = r, g + random.randint(1, 250) % 250, b
                else:
                    pix[x, y] = r, g, b + random.randint(1, 250) % 250

    def nihil(self):
        pix = self.image.load()
        W, H = self.image.size
        change = [random.randint(1, 250), random.randint(1, 250), random.randint(1, 250)]
        change1 = [random.randint(1, 250), random.randint(1, 250), random.randint(1, 250)]
        for y in range(H):
            for x in range(W):
                r, g, b = pix[x, y]
                if y % 2 == 0:
                    if x % 2 == 0:
                        pix[x, y] = (r + change[0]) % 250, (g + change[0]) % 250, (b + change[0]) % 250,
                    else:
                        pix[x, y] = r + (change1[0]) % 250, (g + change1[0]) % 250, (b + change1[0]) % 250,
                else:
                    if x % 2 == 1:
                        pix[x, y] = r + (change[0]) % 250, (g + change[0]) % 250, (b + change[0]) % 250,
                    else:
                        pix[x, y] = r + (change1[0]) % 250, (g + change1[0]) % 250, (b + change1[0]) % 250,

    def edges(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)

    def save(self):
        self.image.save(f'static/images/{self.date}/{self.file}')
