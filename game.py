import os
import adafruit_imageload
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay

# PyGame setup
pygame.init()

display = PyGameDisplay(width=128, height=128)

# Background setup
backgrounds = {}

for entry in os.scandir("./art/backgrounds"):
    if entry.is_file():
        background = displayio.OnDiskBitmap(entry.path)
        background_sprite = displayio.TileGrid(
            background,
            pixel_shader=background.pixel_shader
        )
        # Get the filename of the bmp file without the extension
        background_filename = os.path.splitext(os.path.basename(entry.path))[0]
        backgrounds[background_filename] = background_sprite

print(backgrounds)

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

home_screen = displayio.Group()

home_screen.append(backgrounds["background"])

# for entry in os.scandir("./art/words"):
#     if entry.is_file():
#         image, image_palette = adafruit_imageload.load(
#             entry.path,
#             bitmap=displayio.Bitmap,
#             palette=displayio.Palette
#         )
#         image_palette.make_transparent(0)
#         image_sprite = displayio.TileGrid(
#             image,
#             pixel_shader=image_palette
#         )
#         test_screen.append(image_sprite)
#         images.append(image_sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

    display.show(home_screen)
