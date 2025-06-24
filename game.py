import os
import adafruit_imageload
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay

# PyGame setup
pygame.init()

display = PyGameDisplay(width=128, height=128)

# Screen settings
set_home_screen = True
set_difficulty_screen = False
set_menu_screen = False
set_game_screen = False
set_stage_complete_screen = False
set_how_to_play_screen = False
level = "easy"

# Music settings
music_loaded = False
song_pos = 0
song_bpm = 120
song_pos_offset = 0

def getFilenameFromPath(path):
    return os.path.splitext(os.path.basename(path))[0]

# Backgrounds setup
backgrounds = {}

for entry in os.scandir("./art/backgrounds"):
    if entry.is_file():
        background = displayio.OnDiskBitmap(entry.path)
        background_sprite = displayio.TileGrid(
            background,
            pixel_shader=background.pixel_shader
        )
        backgrounds[getFilenameFromPath(entry.path)] = background_sprite

# Home Screen Setup
home_screen = displayio.Group()
home_screen.append(backgrounds["rabeat"])

home_screen_sprites = {}

for entry in os.scandir("./art/home"):
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
        home_screen_sprites[getFilenameFromPath(entry.path)] = image_sprite

for sprite in home_screen_sprites.values():
    home_screen.append(sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

    display.show(home_screen)
