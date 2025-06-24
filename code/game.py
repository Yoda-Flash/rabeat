import os
import adafruit_imageload
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay

pygame.init()

display = PyGameDisplay(width=128, height=128)

images = []
test_screen = displayio.Group()

# image, image_palette = adafruit_imageload.load(
#     "./art/background.bmp",
#     bitmap=displayio.Bitmap,
#     palette=displayio.Palette
# )
# image_palette.make_transparent(0)
# image_sprite = displayio.TileGrid(
#     image,
#     pixel_shader=image_palette
# )

image = displayio.OnDiskBitmap("./art/background.bmp")
image_sprite = displayio.TileGrid(
    image,
    pixel_shader=image.pixel_shader
)

test_screen.append(image_sprite)

for entry in os.scandir("./art/words"):
    if entry.is_file():
        image, image_palette = adafruit_imageload.load(
            entry.path,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )
        image_palette.make_transparent(0)
        image_sprite = displayio.TileGrid(
            image,
            pixel_shader=image_palette
        )
        test_screen.append(image_sprite)
        images.append(image_sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

    display.show(test_screen)
