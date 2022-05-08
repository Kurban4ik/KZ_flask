import os
import random

from PIL import Image, ImageFilter


def pixelator(date, file):
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

    image = Image.open(f'static/inner/{date}/{file}').convert('RGB')
    for size in (image.size[0] // 100,):
        image_pixelate = pixelate(image, pixel_size=size)
        os.mkdir(f'static/images/{date}')
        image_pixelate.save(str(f'static/images/{date}/{file}').format(size))


def liner(date, file):
    image = Image.open(f'static/inner/{date}/{file}').convert('RGB')
    pix = image.load()
    W, H = image.size
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
    os.mkdir(f'static/images/{date}')
    image.save(f'static/images/{date}/{file}')


def nihil(date, file):
    image = Image.open(f'static/inner/{date}/{file}').convert('RGB')
    pix = image.load()
    W, H = image.size
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


def edges(date, file):
    image = Image.open(f'static/inner/{date}/{file}').convert('RGB')
    edges = image.filter(ImageFilter.FIND_EDGES)
    os.mkdir(f'static/images/{date}')
    edges.save(f'static/images/{date}/{file}')