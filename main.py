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
SET_HOME_SCREEN = True
SET_DIFFICULTY_SCREEN = False
SET_MENU_SCREEN = False
SET_GAME_SCREEN = False
SET_STAGE_COMPLETE_SCREEN = False
SET_HOW_TO_PLAY_SCREEN = False
LEVEL = "easy"

# Music settings
MUSIC_LOADED = False
SONG_POS = 0
SONG_BPM = 120
SONG_POS_OFFSET = 0

# Create master sprites dictionary
sprites = {}

def get_filename_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]

def get_dirname_from_directory(path):
    return os.path.basename(os.path.dirname(path))

def create_sprites_for_directory(directory, parent_dirname=""):
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
            if parent_dirname != "":
                subdirname = get_dirname_from_directory(entry.path)
                if parent_dirname not in sprites:
                    sprites[parent_dirname] = {}
                if subdirname not in sprites[parent_dirname]:
                    sprites[parent_dirname][subdirname] = {}
                sprites[parent_dirname][subdirname][get_filename_from_path(entry.path)] = image_sprite
            else:
                dirname = get_dirname_from_directory(entry.path)
                if dirname not in sprites:
                    sprites[dirname] = {}
                sprites[dirname][get_filename_from_path(entry.path)] = image_sprite

        if entry.is_dir():
            create_sprites_for_directory(entry.path, get_dirname_from_directory(entry.path))

# Backgrounds setup
backgrounds = {}

for entry in os.scandir("./art/backgrounds"):
    if entry.is_file():
        background = displayio.OnDiskBitmap(entry.path)
        background_sprite = displayio.TileGrid(
            background,
            pixel_shader=background.pixel_shader
        )
        backgrounds[get_filename_from_path(entry.path)] = background_sprite

# Home Screen Setup
home_screen = displayio.Group()
home_screen_names = []

home_screen.append(backgrounds["rabeat"])
home_screen_names.append("rabeat")

create_sprites_for_directory("./art/home")

for sprite in sprites["home"]:
    home_screen.append(sprites["home"][sprite])
    home_screen_names.append(sprite)

# Difficulty screen setup
difficulty_screen = displayio.Group()
difficulty_screen_names = []

difficulty_screen.append(backgrounds["lightened_background"])
difficulty_screen_names.append("lightened_background")

create_sprites_for_directory("./art/difficulty")

for sprite in sprites["difficulty"]:
    difficulty_screen.append(sprites["difficulty"][sprite])
    difficulty_screen_names.append(sprite)

difficulty_screen[difficulty_screen_names.index("normal")].hidden = True
difficulty_screen[difficulty_screen_names.index("hard")].hidden = True

# Game screen setup
game_screen = displayio.Group()
game_screen_names = []

game_screen.append(backgrounds["background"])
game_screen_names.append("background")

create_sprites_for_directory("./art/game")

for sprite in sprites["game"]:
    if type(sprites["game"][sprite]) == dict:
        for subsprite in sprites["game"][sprite]:
            game_screen.append(sprites["game"][sprite][subsprite])
            game_screen_names.append(subsprite)
            game_screen[-1].hidden = True
    else:
        game_screen.append(sprites["game"][sprite])
        game_screen_names.append(sprite)
        game_screen[-1].hidden = True
print(game_screen_names)
game_screen[game_screen_names.index("scoreboard")].hidden = False
game_screen[game_screen_names.index("user_neutral")].hidden = False
game_screen[game_screen_names.index("model_neutral")].hidden = False

def is_left_button_pressed():
    return keys[pygame.K_LEFT] or keys[pygame.K_1]

def is_middle_button_pressed():
    return keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_2]

def is_right_button_pressed():
    return keys[pygame.K_RIGHT] or keys[pygame.K_3]
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

    if SET_HOME_SCREEN:
        display.show(home_screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                SET_DIFFICULTY_SCREEN = True
                SET_HOME_SCREEN = False
    elif SET_DIFFICULTY_SCREEN:
        restart()
        display.show(difficulty_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or is_middle_button_pressed():
            LEVEL = change_difficulty(LEVEL)
        if keys[pygame.K_RETURN] or is_right_button_pressed():
            SET_GAME_SCREEN = True
            SET_DIFFICULTY_SCREEN = False
            time.sleep(0.5)
    elif SET_GAME_SCREEN:
        display.show(game_screen)