import math
import os
import time
from random import randint

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

RANDOM_POSE_INDEX = 1
RANDOM_POSE_INDEX_TIMER = 0

USER_LOCK = False
RATING_ON = False
RATING_ON_TIMER = 0
ATTEMPTED = 0
ATTEMPTED_THRESHOLD = 600

# Score settings
NUM_SONG_TIMESTAMPS = 0
CURRENT_SCORE = 0
PERCENTAGE_SCORE = 0

CONFETTI_TIMER = 1

SET_MODEL_TIMESTAMPS = {
    "easy": {
        "neutral": [12000, 21000, 33000],
        "left": [4000, 16000, 19000, 25000, 37000],
        "right": [8000, 27000, 35000],
        "random": [23000, 29000, 31000]
    }, "normal": {
        "neutral": [5500, 13500, 28500, 41500, 47500],
        "left": [9500, 24500, 40500],
        "right": [17500, 30500, 37000, 47000],
        "random": [22500, 26500, 32500, 36500, 41000, 44500, 45500, 46500]
    }, "hard": {
        "neutral": [7000, 16800, 31000, 35350, 40500, 42000],
        "left": [5000, 16400, 23000, 39000],
        "right": [9000, 15000, 23350, 42500],
        "random": [8000, 16000, 27000, 27350, 31350, 35000, 40000, 41000]
    }
}

SET_USER_TIMESTAMPS = {
    "easy": {
        "neutral": [14000, 22000, 34000],
        "left": [6000, 18000, 20000, 26000, 38000],
        "right": [10000, 28000, 36000],
        "random": [24000, 30000, 32000]
    }, "normal": {
        "neutral": [7500, 15500, 29500, 43500, 51500],
        "left": [11500, 25500, 42500],
        "right": [19500, 31500, 39000, 51000],
        "random": [23500, 27500, 33500, 38500, 43000, 48500, 49500, 50500]
    }, "hard": {
        "neutral": [11000, 20800, 33000, 37350, 44500, 46000],
        "left": [6000, 20400, 25000, 43000],
        "right": [13000, 19000, 25350, 46500],
        "random": [12000, 20000, 29000, 29350, 33350, 37000, 44000, 45000]
    }
}

RANDOMIZED_MODEL_TIMESTAMPS = {}
RANDOMIZED_USER_TIMESTAMPS = {}
ALL_USER_LEVEL_TIMESTAMPS = []

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
ratings = ["miss", "good", "great", "perfect"]

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
game_screen[game_screen_names.index("0")].hidden = False

# Menu screen setup
menu_screen = displayio.Group()
menu_screen_names = []
menu_options = ["back_to_game", "restart", "how_to_play", "difficulty", "quit"]

menu_screen.append(backgrounds["menu"])
menu_screen_names.append("menu")

create_sprites_for_directory("./art/menu")

# Move "options" to the start of the sprites["menu"] so the layer will be first
unordered_menu = sprites["menu"]
ordered_menu = {"options": unordered_menu["options"]}
unordered_menu.pop("options")
sprites["menu"] = ordered_menu | unordered_menu

for sprite in sprites["menu"]:
    menu_screen.append(sprites["menu"][sprite])
    menu_screen_names.append(sprite)
    menu_screen[-1].hidden = True
menu_screen[menu_screen_names.index("options")].hidden = False
menu_screen[menu_screen_names.index("back_to_game")].hidden = False

# How to play screen setup
how_to_play_screen = displayio.Group()

how_to_play_screen.append(backgrounds["lightened_background"])

qr, qr_palette = adafruit_imageload.load(
    "./qr.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
qr_palette.make_transparent(0)
qr_sprite = displayio.TileGrid(
    qr,
    pixel_shader=qr_palette
)

how_to_play_screen.append(qr_sprite)

# End screen setup
stage_complete_screen = displayio.Group()
stage_complete_screen_names = []
stage_complete_options = ["restart", "quit"]

stage_complete_screen.append(backgrounds["stage_complete"])
stage_complete_screen_names.append("stage_complete")

create_sprites_for_directory("./art/stage_complete")

# Move "options" to the start of the sprites["stage_complete"] so the layer will be first
unordered_stage_complete = sprites["stage_complete"]
ordered_stage_complete = {"options": unordered_stage_complete["options"]}
unordered_stage_complete.pop("options")
sprites["stage_complete"] = ordered_stage_complete | unordered_stage_complete

for sprite in sprites["stage_complete"]:
    if type(sprites["stage_complete"][sprite]) == dict:
        for subsprite in sprites["stage_complete"][sprite]:
            stage_complete_screen.append(sprites["stage_complete"][sprite][subsprite])
            stage_complete_screen_names.append(subsprite)
            stage_complete_screen[-1].hidden = True
    else:
        stage_complete_screen.append(sprites["stage_complete"][sprite])
        stage_complete_screen_names.append(sprite)
        stage_complete_screen[-1].hidden = True

stage_complete_screen[stage_complete_screen_names.index("options")].hidden = False
stage_complete_screen[stage_complete_screen_names.index("rabbit")].hidden = False
stage_complete_screen[stage_complete_screen_names.index("restart")].hidden = False

def is_left_button_pressed():
    return keys[pygame.K_LEFT] or keys[pygame.K_1]

def is_middle_button_pressed():
    return keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_2]

def is_right_button_pressed():
    return keys[pygame.K_RIGHT] or keys[pygame.K_3]

def is_two_buttons_pressed():
    return (is_left_button_pressed() + is_middle_button_pressed() + is_right_button_pressed()) >= 2

def is_any_button_pressed():
    return is_left_button_pressed() or is_middle_button_pressed() or is_right_button_pressed()

def load_music(level_difficulty, offset):
    match level_difficulty:
        case "easy":
            pygame.mixer.music.load("./music/take_a_stab.mp3")
            offset = 100
        case "normal":
            pygame.mixer.music.load("./music/copycat_curry.mp3")
            offset = 100
        case "hard":
            pygame.mixer.music.load("./music/time_to_shine.mp3")
    return True, offset

def set_poses(level_difficulty):
    global RANDOMIZED_MODEL_TIMESTAMPS, RANDOMIZED_USER_TIMESTAMPS, ALL_USER_LEVEL_TIMESTAMPS
    RANDOMIZED_MODEL_TIMESTAMPS = SET_MODEL_TIMESTAMPS[level_difficulty]
    RANDOMIZED_USER_TIMESTAMPS = SET_USER_TIMESTAMPS[level_difficulty]
    ALL_USER_LEVEL_TIMESTAMPS = []
    for timestamps in RANDOMIZED_USER_TIMESTAMPS.values():
        ALL_USER_LEVEL_TIMESTAMPS.extend(timestamps)
    ALL_USER_LEVEL_TIMESTAMPS.sort()

def distribute_randoms(level_difficulty):
    index = 0
    for timestamp in SET_MODEL_TIMESTAMPS[level_difficulty]["random"]:
        direction = randint(0, 1)
        if direction == 0:
            RANDOMIZED_MODEL_TIMESTAMPS["left"].append(timestamp)
            RANDOMIZED_USER_TIMESTAMPS["left"].append(SET_USER_TIMESTAMPS[level_difficulty]["random"][index])
        elif direction == 1:
            RANDOMIZED_MODEL_TIMESTAMPS["right"].append(timestamp)
            RANDOMIZED_USER_TIMESTAMPS["right"].append(SET_USER_TIMESTAMPS[level_difficulty]["random"][index])
        index += 1

def set_num_timestamps():
    global NUM_SONG_TIMESTAMPS
    NUM_SONG_TIMESTAMPS = len(RANDOMIZED_MODEL_TIMESTAMPS["neutral"]) + len(RANDOMIZED_MODEL_TIMESTAMPS["left"]) + len(RANDOMIZED_MODEL_TIMESTAMPS["right"])

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
    stage_complete_screen[stage_complete_screen_names.index(option)].hidden = True
    option = next_option(option, stage_complete_options)
    stage_complete_screen[stage_complete_screen_names.index(option)].hidden = False
    time.sleep(0.15)
    return option

def show_beat_sign(beat=0):
    if beat == 0:
        game_screen[game_screen_names.index("beat_1")].hidden = True
        game_screen[game_screen_names.index("beat_2")].hidden = True
        game_screen[game_screen_names.index("beat_3")].hidden = True
    else:
        game_screen[game_screen_names.index(f"beat_{beat}")].hidden = False
        i = 1
        while i <= 3:
            if i != beat:
                game_screen[game_screen_names.index(f"beat_{i}")].hidden = True
            i += 1

def show_model_pose(direction):
    global RANDOM_POSE_INDEX_TIMER, RANDOM_POSE_INDEX
    game_screen[game_screen_names.index("model_neutral")].hidden = True
    game_screen[game_screen_names.index("model_bob")].hidden = True

    if RANDOM_POSE_INDEX_TIMER == 0:
        RANDOM_POSE_INDEX = randint(1, 4)
        RANDOM_POSE_INDEX_TIMER += 1

    if direction == "neutral":
        if RANDOM_POSE_INDEX % 2 == 0:
            game_screen[game_screen_names.index("model_back")].hidden = False
        else:
            game_screen[game_screen_names.index("model_duck")].hidden = False
    else:
        game_screen[game_screen_names.index(f"model_{direction}{RANDOM_POSE_INDEX}")].hidden = False

def hide_model_poses(direction=""):
    hide_model_poses_inside_direction(direction)
    hide_model_poses_outside_direction(direction)
def hide_model_poses_inside_direction(direction=""):
    if direction == "neutral":
        if RANDOM_POSE_INDEX % 2 == 0:
            game_screen[game_screen_names.index("model_duck")].hidden = True
        else:
            game_screen[game_screen_names.index("model_back")].hidden = True
    elif direction == "left" or direction == "right":
        i = 1
        while i <= 4:
            if RANDOM_POSE_INDEX != i:
                game_screen[game_screen_names.index(f"model_{direction}{i}")].hidden = True
            i += 1

def hide_model_poses_outside_direction(direction=""):
    # Hide all poses not in the specified direction
    if direction != "left":
        i = 1
        while i <= 4:
            game_screen[game_screen_names.index(f"model_left{i}")].hidden = True
            i += 1
    if direction != "neutral":
        game_screen[game_screen_names.index("model_back")].hidden = True
        game_screen[game_screen_names.index("model_duck")].hidden = True
    if direction != "right":
        i = 1
        while i <= 4:
            game_screen[game_screen_names.index(f"model_right{i}")].hidden = True
            i += 1

def show_user_pose(direction):
    global RANDOM_POSE_INDEX_TIMER, RANDOM_POSE_INDEX
    game_screen[game_screen_names.index("user_neutral")].hidden = True
    game_screen[game_screen_names.index("user_bob")].hidden = True

    if direction == "neutral":
        if RANDOM_POSE_INDEX % 2 == 0:
            game_screen[game_screen_names.index("user_back")].hidden = False
        else:
            game_screen[game_screen_names.index("user_duck")].hidden = False
    else:
        game_screen[game_screen_names.index(f"user_{direction}{RANDOM_POSE_INDEX}")].hidden = False

def hide_user_pose():
    i = 1
    while i <= 4:
        game_screen[game_screen_names.index(f"user_left{i}")].hidden = True
        game_screen[game_screen_names.index(f"user_right{i}")].hidden = True
        i += 1

    game_screen[game_screen_names.index("user_back")].hidden = True
    game_screen[game_screen_names.index("user_duck")].hidden = True

def show_ratings(rating):
    global RATING_ON
    RATING_ON = True
    if rating == "none":
        game_screen[game_screen_names.index("miss")].hidden = True
        game_screen[game_screen_names.index("good")].hidden = True
        game_screen[game_screen_names.index("great")].hidden = True
        game_screen[game_screen_names.index("perfect")].hidden = True
    else:
        game_screen[game_screen_names.index(rating)].hidden = False

        for rating_option in ratings:
            if rating_option != rating:
                game_screen[game_screen_names.index(rating_option)].hidden = True

def get_attempted_threshold(timestamp):
    timestamp_index = ALL_USER_LEVEL_TIMESTAMPS.index(timestamp)
    if timestamp_index > 0:
        return (ALL_USER_LEVEL_TIMESTAMPS[timestamp_index] - ALL_USER_LEVEL_TIMESTAMPS[timestamp_index - 1])/2.5
    else:
        return (ALL_USER_LEVEL_TIMESTAMPS[timestamp_index + 1] - ALL_USER_LEVEL_TIMESTAMPS[timestamp_index])/2.5

def not_attempted(timestamp):
    global ATTEMPTED_THRESHOLD
    ATTEMPTED_THRESHOLD = get_attempted_threshold(timestamp)
    return timestamp - ATTEMPTED >= ATTEMPTED_THRESHOLD

def rate_keypress(direction):
    global SONG_POS, ATTEMPTED
    if any(abs(SONG_POS - timestamp) <= 150 and not_attempted(timestamp) for timestamp in RANDOMIZED_USER_TIMESTAMPS[direction]):
        show_ratings("perfect")
        change_score("perfect")
    elif any(abs(SONG_POS - timestamp) <= 200 and not_attempted(timestamp) for timestamp in RANDOMIZED_USER_TIMESTAMPS[direction]):
        show_ratings("great")
        change_score("great")
    elif any(abs(SONG_POS - timestamp) <= 300 and not_attempted(timestamp) for timestamp in RANDOMIZED_USER_TIMESTAMPS[direction]):
        show_ratings("good")
        change_score("good")
    else:
        show_ratings("miss")
        change_score("miss")
    ATTEMPTED = SONG_POS


def show_score(score):
    game_screen[game_screen_names.index(f"{score}")].hidden = False
    i = 0
    while i <= 12:
        if i != score:
            game_screen[game_screen_names.index(f"{i}")].hidden = True
        i += 1


def change_score(rating):
    change_percentage_score(rating)
    change_current_score()

def change_percentage_score(rating):
    global PERCENTAGE_SCORE
    match rating:
        case "perfect":
            PERCENTAGE_SCORE += (1/NUM_SONG_TIMESTAMPS)
        case "great":
            PERCENTAGE_SCORE += (0.75/NUM_SONG_TIMESTAMPS)
        case "good":
            PERCENTAGE_SCORE += (0.25/NUM_SONG_TIMESTAMPS)

def change_current_score():
    global CURRENT_SCORE, PERCENTAGE_SCORE

    if PERCENTAGE_SCORE >= 0.999:
        CURRENT_SCORE = 12
    elif PERCENTAGE_SCORE >= 0.98:
        CURRENT_SCORE = 11
    elif PERCENTAGE_SCORE >= 0.95:
        CURRENT_SCORE = 10
    elif PERCENTAGE_SCORE >= 0.90:
        CURRENT_SCORE = 9
    elif PERCENTAGE_SCORE >= 0.75:
        CURRENT_SCORE = 8
    elif PERCENTAGE_SCORE >= 0.5:
        CURRENT_SCORE = 7
    elif PERCENTAGE_SCORE >= 0.25:
        CURRENT_SCORE = 6
    elif PERCENTAGE_SCORE >= 0.20:
        CURRENT_SCORE = 5
    elif PERCENTAGE_SCORE >= 0.15:
        CURRENT_SCORE = 4
    elif PERCENTAGE_SCORE >= 0.10:
        CURRENT_SCORE = 3
    elif PERCENTAGE_SCORE >= 0.05:
        CURRENT_SCORE = 2
    elif PERCENTAGE_SCORE >= 0.01:
        CURRENT_SCORE = 1
    else:
        CURRENT_SCORE = 0

    show_score(CURRENT_SCORE)

def move_confetti():
    global CONFETTI_TIMER
    if CONFETTI_TIMER > 4:
        CONFETTI_TIMER = 1
    stage_complete_screen[stage_complete_screen_names.index(f"confetti_{math.floor(CONFETTI_TIMER)}")].hidden = False
    i = 1
    while i <= 4:
        if i != math.floor(CONFETTI_TIMER):
            stage_complete_screen[stage_complete_screen_names.index(f"confetti_{i}")].hidden = True
        i += 1
    CONFETTI_TIMER += 0.25

def restart():
    global MUSIC_LOADED, RATING_ON, CURRENT_SCORE, PERCENTAGE_SCORE, USER_LOCK, ATTEMPTED
    MUSIC_LOADED = False
    RATING_ON = False

    hide_user_pose()
    hide_model_poses()
    game_screen[game_screen_names.index("user_bob")].hidden = True
    game_screen[game_screen_names.index("model_bob")].hidden = True

    show_beat_sign()
    show_ratings("none")

    CURRENT_SCORE = 0
    PERCENTAGE_SCORE = 0
    show_score(0)

    USER_LOCK = False
    ATTEMPTED = False

restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

    if SET_HOME_SCREEN:
        display.show(home_screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or is_any_button_pressed():
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
            set_poses(LEVEL)
            distribute_randoms(LEVEL)
            set_num_timestamps()
            time.sleep(0.5)
    elif SET_GAME_SCREEN:
        display.show(game_screen)

        if is_two_buttons_pressed():
            SET_MENU_SCREEN = True
            SET_GAME_SCREEN = False
            time.sleep(0.2)

        if RATING_ON:
            RATING_ON_TIMER += 1
            if RATING_ON_TIMER >= 50:
                hide_user_pose()
                show_ratings("none")
                RATING_ON_TIMER = 0
                RATING_ON = False

        if RANDOM_POSE_INDEX_TIMER >= 1:
            RANDOM_POSE_INDEX_TIMER += 1
            if RANDOM_POSE_INDEX_TIMER >= 150:
                RANDOM_POSE_INDEX_TIMER = 0

        if not MUSIC_LOADED:
            MUSIC_LOADED, SONG_POS_OFFSET = load_music(LEVEL, SONG_POS_OFFSET)
            pygame.mixer.music.play(loops=0)

        SONG_POS = pygame.mixer.music.get_pos() - SONG_POS_OFFSET

        # Beat signs for user
        if any(abs(timestamp - SONG_POS) <= 50 for timestamp in ALL_USER_LEVEL_TIMESTAMPS):
            show_beat_sign()
        elif any(0 <= (timestamp - SONG_POS) <= 550 for timestamp in ALL_USER_LEVEL_TIMESTAMPS):
            show_beat_sign(1)
        elif any(0 <= (timestamp - SONG_POS) <= 1050 for timestamp in ALL_USER_LEVEL_TIMESTAMPS):
            show_beat_sign(2)
        elif any(0 <= (timestamp - SONG_POS) <= 1550 for timestamp in ALL_USER_LEVEL_TIMESTAMPS):
            show_beat_sign(3)

        if any(-300 <= (timestamp - SONG_POS) <= 20 for timestamp in RANDOMIZED_MODEL_TIMESTAMPS["left"]):
            hide_model_poses("left")
            show_model_pose("left")
        elif any(-300 <= (timestamp - SONG_POS) <= 20 for timestamp in RANDOMIZED_MODEL_TIMESTAMPS["right"]):
            hide_model_poses("right")
            show_model_pose("right")
        elif any(-300 <= (timestamp - SONG_POS) <= 20 for timestamp in RANDOMIZED_MODEL_TIMESTAMPS["neutral"]):
            hide_model_poses("neutral")
            show_model_pose("neutral")
        elif SONG_POS % 500 <= 50:
            game_screen[game_screen_names.index("model_neutral")].hidden = True
            hide_model_poses()
            game_screen[game_screen_names.index("model_bob")].hidden = False
        else:
            game_screen[game_screen_names.index("model_bob")].hidden = True
            hide_model_poses()
            game_screen[game_screen_names.index("model_neutral")].hidden = False

        if not RATING_ON and not USER_LOCK:
            if is_left_button_pressed():
                rate_keypress("left")
                show_user_pose("left")
            elif is_middle_button_pressed():
                rate_keypress("neutral")
                show_user_pose("neutral")
            elif is_right_button_pressed():
                rate_keypress("right")
                show_user_pose("right")

        if not RATING_ON:
            if SONG_POS % 500 <= 50:
                game_screen[game_screen_names.index("user_neutral")].hidden = True
                game_screen[game_screen_names.index("user_bob")].hidden = False
            else:
                game_screen[game_screen_names.index("user_neutral")].hidden = False
                game_screen[game_screen_names.index("user_bob")].hidden = True

        if is_any_button_pressed():
            USER_LOCK = True
        else:
            USER_LOCK = False

        if not pygame.mixer.music.get_busy():
            SET_STAGE_COMPLETE_SCREEN = True
            SET_GAME_SCREEN = False
            time.sleep(0.2)

        time.sleep(0.005)
    elif SET_MENU_SCREEN:
        pygame.mixer.music.pause()
        show_ratings("none")
        ATTEMPTED = False

        display.show(menu_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or is_middle_button_pressed():
            MENU_OPTION = change_menu_option(MENU_OPTION)
        if keys[pygame.K_RETURN] or is_right_button_pressed():
            if MENU_OPTION == "back_to_game":
                SET_GAME_SCREEN = True
                pygame.mixer.music.unpause()
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
    elif SET_HOW_TO_PLAY_SCREEN:
        display.show(how_to_play_screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or is_any_button_pressed():
                SET_MENU_SCREEN = True
                SET_HOW_TO_PLAY_SCREEN = False
                time.sleep(0.2)
    elif SET_STAGE_COMPLETE_SCREEN:
        display.show(stage_complete_screen)
        time.sleep(0.05)
        stage_complete_screen[stage_complete_screen_names.index(f"{CURRENT_SCORE}")].hidden = False
        if CURRENT_SCORE == 12:
            stage_complete_screen[stage_complete_screen_names.index("perfect_stage")].hidden = False
            move_confetti()
        if keys[pygame.K_SPACE] or is_middle_button_pressed():
            ENDGAME_OPTION = change_endgame_option(ENDGAME_OPTION)
        if keys[pygame.K_RETURN] or is_right_button_pressed():
            if ENDGAME_OPTION == "restart":
                SET_GAME_SCREEN = True
                restart()
            elif ENDGAME_OPTION == "quit":
                SET_HOME_SCREEN = True
                restart()
            SET_STAGE_COMPLETE_SCREEN = False
            MUSIC_LOADED = False
            time.sleep(0.2)