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
MENU_OPTION = "back_to_game"
ENDGAME_OPTION = "restart"

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
difficulty_options = ["easy", "normal", "hard"]

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
game_screen[game_screen_names.index("scoreboard")].hidden = False
game_screen[game_screen_names.index("user_neutral")].hidden = False
game_screen[game_screen_names.index("model_neutral")].hidden = False

# Menu screen setup
menu_screen = displayio.Group()
menu_screen_names = []
menu_options = ["back_to_game", "restart", "how_to_play", "difficulty", "quit"]

menu_screen.append(backgrounds["menu"])
menu_screen_names.append("menu")

create_sprites_for_directory("./art/menu")

# Move "options" to the start of the sprites["menu"] so the layer will be first
unordered_menu = sprites["menu"]
ordered_menu = {}
ordered_menu["options"] = unordered_menu["options"]
unordered_menu.pop("options")
sprites["menu"] = ordered_menu | unordered_menu

for sprite in sprites["menu"]:
    menu_screen.append(sprites["menu"][sprite])
    menu_screen_names.append(sprite)
    menu_screen[-1].hidden = True
menu_screen[menu_screen_names.index("options")].hidden = False
menu_screen[menu_screen_names.index("back_to_game")].hidden = False

def is_left_button_pressed():
    return keys[pygame.K_LEFT] or keys[pygame.K_1]

def is_middle_button_pressed():
    return keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_2]

def is_right_button_pressed():
    return keys[pygame.K_RIGHT] or keys[pygame.K_3]

def is_two_buttons_pressed():
    return (is_left_button_pressed() + is_middle_button_pressed() + is_right_button_pressed()) >= 2

def load_music(level_difficulty, offset):
    pass

def next_option(current_option, options):
    current_index = options.index(current_option)
    if current_index == (len(options) - 1):
        return options[0]
    else:
        return options[current_index + 1]

def change_difficulty(level_difficulty):
    difficulty_screen[difficulty_screen_names.index(level_difficulty)].hidden = True
    level_difficulty = next_option(level_difficulty, difficulty_options)
    difficulty_screen[difficulty_screen_names.index(level_difficulty)].hidden = False
    time.sleep(0.15)
    return level_difficulty



def change_menu_option(option):
    menu_screen[menu_screen_names.index(option)].hidden = True
    option = next_option(option, menu_options)
    menu_screen[menu_screen_names.index(option)].hidden = False
    time.sleep(0.15)
    return option


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
        if is_two_buttons_pressed():
            SET_MENU_SCREEN = True
            SET_GAME_SCREEN = False
            time.sleep(0.2)
    elif SET_MENU_SCREEN:
        display.show(menu_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or is_middle_button_pressed():
            MENU_OPTION = change_menu_option(MENU_OPTION)
        if keys[pygame.K_RETURN] or is_right_button_pressed():
            if MENU_OPTION == "back_to_game":
                SET_GAME_SCREEN = True
            elif MENU_OPTION == "restart":
                restart()
                SET_GAME_SCREEN = True
            elif MENU_OPTION == "how_to_play":
                SET_HOW_TO_PLAY_SCREEN = True
            elif MENU_OPTION == "difficulty":
                SET_DIFFICULTY_SCREEN = True
            elif MENU_OPTION == "quit":
                restart()
                SET_HOME_SCREEN = True

            SET_MENU_SCREEN = False
            time.sleep(0.2)