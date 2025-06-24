import os
import time

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
home_screen_names = []

home_screen.append(backgrounds["rabeat"])
home_screen_names.append("rabeat")

createSpritesForDirectory("./art/home")

for sprite in sprites["home"]:
    home_screen.append(sprites["home"][sprite])
    home_screen_names.append(sprite)

# Difficulty screen setup
difficulty_screen = displayio.Group()
difficulty_screen_names = []

difficulty_screen.append(backgrounds["lightened_background"])
difficulty_screen_names.append("lightened_background")

createSpritesForDirectory("./art/difficulty")

for sprite in sprites["difficulty"]:
    difficulty_screen.append(sprites["difficulty"][sprite])
    difficulty_screen_names.append(sprite)

difficulty_screen[difficulty_screen_names.index("normal")].hidden = True
difficulty_screen[difficulty_screen_names.index("hard")].hidden = True

def is_left_button_pressed():
    if keys[pygame.K_LEFT] or keys[pygame.K_1]:
        return True

def is_middle_button_pressed():
    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_2]:
        return True

def is_right_button_pressed():
    if keys[pygame.K_RIGHT] or keys[pygame.K_3]:
        return True
def load_music(level_difficulty, offset):
    pass

def change_difficulty(level_difficulty):
    if level_difficulty == "easy":
        difficulty_screen[difficulty_screen_names.index("easy")].hidden = True
        difficulty_screen[difficulty_screen_names.index("normal")].hidden = False
        level_difficulty = "normal"
    elif level_difficulty == "normal":
        difficulty_screen[difficulty_screen_names.index("normal")].hidden = True
        difficulty_screen[difficulty_screen_names.index("hard")].hidden = False
        level_difficulty = "hard"
    elif level_difficulty == "hard":
        difficulty_screen[difficulty_screen_names.index("hard")].hidden = True
        difficulty_screen[difficulty_screen_names.index("easy")].hidden = False
        level_difficulty = "easy"
    time.sleep(0.15)
    return level_difficulty

def change_menu_option(option):
    pass

def change_endgame_option(option):
    pass

def change_score(rating):
    pass

def restart():
    pass

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
        restart()
        display.show(difficulty_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or is_middle_button_pressed():
            level = change_difficulty(level)
        if keys[pygame.K_RETURN] or is_right_button_pressed():
            set_game_screen = True
            set_difficulty_screen = False

