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

# Create master sprites dictionary
sprites = {}

def getFilenameFromPath(path):
    return os.path.splitext(os.path.basename(path))[0]

def getDirnameFromDirectory(path):
    return os.path.basename(os.path.dirname(path))

def createSpritesForDirectory(directory):
    for entry in os.scandir(directory):
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
            if getDirnameFromDirectory(entry.path) not in sprites:
                sprites[getDirnameFromDirectory(entry.path)] = {}
            print(getFilenameFromPath(entry.path))
            sprites[getDirnameFromDirectory(entry.path)][getFilenameFromPath(entry.path)] = image_sprite

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
createSpritesForDirectory("./art/home")

for sprite in sprites["home"].values():
    home_screen.append(sprite)

# Difficulty screen setup
difficulty_screen = displayio.Group()
difficulty_screen.append(backgrounds["lightened_background"])
createSpritesForDirectory("./art/difficulty")

for sprite in sprites["difficulty"].values():
    difficulty_screen.append(sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

    if set_home_screen:
        display.show(home_screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                set_difficulty_screen = True
                set_home_screen = False
    elif set_difficulty_screen:
        display.show(difficulty_screen)
