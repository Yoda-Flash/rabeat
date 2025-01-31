import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import adafruit_imageload

pygame.init()

display = PyGameDisplay(width=128, height=128)

# Background init
background = displayio.OnDiskBitmap("./art/background.bmp")
bg_sprite = displayio.TileGrid(
    background,
    pixel_shader=background.pixel_shader)

home_background = displayio.OnDiskBitmap("./art/rabeat.bmp")
home_bg_sprite = displayio.TileGrid(
    home_background,
    pixel_shader=home_background.pixel_shader
)

button_to_start, button_to_start_palette = adafruit_imageload.load(
    "./art/button_to_start.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
button_to_start_palette.make_transparent(0)
button_to_start_sprite = displayio.TileGrid(
    button_to_start,
    pixel_shader=button_to_start_palette
)

# Difficulty screen inits
lightened_bg = displayio.OnDiskBitmap("./art/lightened_background.bmp")
lightened_bg_sprite = displayio.TileGrid(
    lightened_bg,
    pixel_shader=lightened_bg.pixel_shader
)

difficulties, difficulties_palette = adafruit_imageload.load(
    "./art/difficulty/difficulties.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
difficulties_palette.make_transparent(0)
difficulties_sprite = displayio.TileGrid(
    difficulties,
    pixel_shader=difficulties_palette
)

select_difficulty, select_difficulty_palette = adafruit_imageload.load(
    "./art/difficulty/difficulty.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
select_difficulty_palette.make_transparent(0)
select_difficulty_sprite = displayio.TileGrid(
    select_difficulty,
    pixel_shader=select_difficulty_palette
)

easy, easy_palette = adafruit_imageload.load(
    "./art/difficulty/easy.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
easy_palette.make_transparent(0)
easy_sprite = displayio.TileGrid(
    easy,
    pixel_shader=easy_palette
)

normal, normal_palette = adafruit_imageload.load(
    "./art/difficulty/normal.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
normal_palette.make_transparent(0)
normal_sprite = displayio.TileGrid(
    normal,
    pixel_shader=normal_palette
)

hard, hard_palette = adafruit_imageload.load(
    "./art/difficulty/hard.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
hard_palette.make_transparent(0)
hard_sprite = displayio.TileGrid(
    hard,
    pixel_shader=hard_palette
)

# User rabbit inits
user_rabbits_left = []
user_rabbits_right = []

user_rabbit, user_rabbit_palette = adafruit_imageload.load(
    "./art/user_rabbit/neutral.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_palette.make_transparent(0)
user_rabbit_sprite = displayio.TileGrid(
    user_rabbit,
    pixel_shader=user_rabbit_palette
)

user_rabbit_bob, user_rabbit_bob_palette = adafruit_imageload.load(
    "./art/user_rabbit/bob.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_bob_palette.make_transparent(0)
user_rabbit_bob_sprite = displayio.TileGrid(
    user_rabbit_bob,
    pixel_shader=user_rabbit_bob_palette
)

user_rabbit_duck, user_rabbit_duck_palette = adafruit_imageload.load(
    "./art/user_rabbit/duck.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_duck_palette.make_transparent(0)
user_rabbit_duck_sprite = displayio.TileGrid(
    user_rabbit_duck,
    pixel_shader=user_rabbit_duck_palette
)

user_rabbit_back, user_rabbit_back_palette = adafruit_imageload.load(
    "./art/user_rabbit/back.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_back_palette.make_transparent(0)
user_rabbit_back_sprite = displayio.TileGrid(
    user_rabbit_back,
    pixel_shader=user_rabbit_back_palette
)

user_rabbit_left1, user_rabbit_left1_palette = adafruit_imageload.load(
    "./art/user_rabbit/left1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left1_palette.make_transparent(0)
user_rabbit_left1_sprite = displayio.TileGrid(
    user_rabbit_left1,
    pixel_shader=user_rabbit_left1_palette
)
user_rabbits_left.append(user_rabbit_left1_sprite)

user_rabbit_left2, user_rabbit_left2_palette = adafruit_imageload.load(
    "./art/user_rabbit/left2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left2_palette.make_transparent(0)
user_rabbit_left2_sprite = displayio.TileGrid(
    user_rabbit_left2,
    pixel_shader=user_rabbit_left2_palette
)
user_rabbits_left.append(user_rabbit_left2_sprite)

user_rabbit_left3, user_rabbit_left3_palette = adafruit_imageload.load(
    "./art/user_rabbit/left3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left3_palette.make_transparent(0)
user_rabbit_left3_sprite = displayio.TileGrid(
    user_rabbit_left3,
    pixel_shader=user_rabbit_left3_palette
)
user_rabbits_left.append(user_rabbit_left3_sprite)

user_rabbit_left4, user_rabbit_left4_palette = adafruit_imageload.load(
    "./art/user_rabbit/left4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left4_palette.make_transparent(0)
user_rabbit_left4_sprite = displayio.TileGrid(
    user_rabbit_left4,
    pixel_shader=user_rabbit_left4_palette
)
user_rabbits_left.append(user_rabbit_left4_sprite)

user_rabbit_right1, user_rabbit_right1_palette = adafruit_imageload.load(
    "./art/user_rabbit/right1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right1_palette.make_transparent(0)
user_rabbit_right1_sprite = displayio.TileGrid(
    user_rabbit_right1,
    pixel_shader=user_rabbit_right1_palette
)
user_rabbits_right.append(user_rabbit_right1_sprite)

user_rabbit_right2, user_rabbit_right2_palette = adafruit_imageload.load(
    "./art/user_rabbit/right2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right2_palette.make_transparent(0)
user_rabbit_right2_sprite = displayio.TileGrid(
    user_rabbit_right2,
    pixel_shader=user_rabbit_right2_palette
)
user_rabbits_right.append(user_rabbit_right2_sprite)

user_rabbit_right3, user_rabbit_right3_palette = adafruit_imageload.load(
    "./art/user_rabbit/right3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right3_palette.make_transparent(0)
user_rabbit_right3_sprite = displayio.TileGrid(
    user_rabbit_right3,
    pixel_shader=user_rabbit_right3_palette
)
user_rabbits_right.append(user_rabbit_right3_sprite)

user_rabbit_right4, user_rabbit_right4_palette = adafruit_imageload.load(
    "./art/user_rabbit/right4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right4_palette.make_transparent(0)
user_rabbit_right4_sprite = displayio.TileGrid(
    user_rabbit_right4,
    pixel_shader=user_rabbit_right4_palette
)
user_rabbits_right.append(user_rabbit_right4_sprite)

# Model rabbit inits
model_rabbits_left = []
model_rabbits_right = []

model_rabbit, model_rabbit_palette = adafruit_imageload.load(
    "./art/model_rabbit/neutral.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_palette.make_transparent(0)
model_rabbit_sprite = displayio.TileGrid(
    model_rabbit,
    pixel_shader=model_rabbit_palette
)

model_rabbit_bob, model_rabbit_bob_palette = adafruit_imageload.load(
    "./art/model_rabbit/bob.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_bob_palette.make_transparent(0)
model_rabbit_bob_sprite = displayio.TileGrid(
    model_rabbit_bob,
    pixel_shader=model_rabbit_bob_palette
)

model_rabbit_duck, model_rabbit_duck_palette = adafruit_imageload.load(
    "./art/model_rabbit/duck.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_duck_palette.make_transparent(0)
model_rabbit_duck_sprite = displayio.TileGrid(
    model_rabbit_duck,
    pixel_shader=model_rabbit_duck_palette
)

model_rabbit_back, model_rabbit_back_palette = adafruit_imageload.load(
    "./art/model_rabbit/back.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_back_palette.make_transparent(0)
model_rabbit_back_sprite = displayio.TileGrid(
    model_rabbit_back,
    pixel_shader=model_rabbit_back_palette
)

model_rabbit_left1, model_rabbit_left1_palette = adafruit_imageload.load(
    "./art/model_rabbit/left1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left1_palette.make_transparent(0)
model_rabbit_left1_sprite = displayio.TileGrid(
    model_rabbit_left1,
    pixel_shader=model_rabbit_left1_palette
)
model_rabbits_left.append(model_rabbit_left1_sprite)

model_rabbit_left2, model_rabbit_left2_palette = adafruit_imageload.load(
    "./art/model_rabbit/left2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left2_palette.make_transparent(0)
model_rabbit_left2_sprite = displayio.TileGrid(
    model_rabbit_left2,
    pixel_shader=model_rabbit_left2_palette
)
model_rabbits_left.append(model_rabbit_left2_sprite)

model_rabbit_left3, model_rabbit_left3_palette = adafruit_imageload.load(
    "./art/model_rabbit/left3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left3_palette.make_transparent(0)
model_rabbit_left3_sprite = displayio.TileGrid(
    model_rabbit_left3,
    pixel_shader=model_rabbit_left3_palette
)
model_rabbits_left.append(model_rabbit_left3_sprite)

model_rabbit_left4, model_rabbit_left4_palette = adafruit_imageload.load(
    "./art/model_rabbit/left4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left4_palette.make_transparent(0)
model_rabbit_left4_sprite = displayio.TileGrid(
    model_rabbit_left4,
    pixel_shader=model_rabbit_left4_palette
)
model_rabbits_left.append(model_rabbit_left4_sprite)

model_rabbit_right1, model_rabbit_right1_palette = adafruit_imageload.load(
    "./art/model_rabbit/right1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right1_palette.make_transparent(0)
model_rabbit_right1_sprite = displayio.TileGrid(
    model_rabbit_right1,
    pixel_shader=model_rabbit_right1_palette
)
model_rabbits_right.append(model_rabbit_right1_sprite)

model_rabbit_right2, model_rabbit_right2_palette = adafruit_imageload.load(
    "./art/model_rabbit/right2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right2_palette.make_transparent(0)
model_rabbit_right2_sprite = displayio.TileGrid(
    model_rabbit_right2,
    pixel_shader=model_rabbit_right2_palette
)
model_rabbits_right.append(model_rabbit_right2_sprite)

model_rabbit_right3, model_rabbit_right3_palette = adafruit_imageload.load(
    "./art/model_rabbit/right3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right3_palette.make_transparent(0)
model_rabbit_right3_sprite = displayio.TileGrid(
    model_rabbit_right3,
    pixel_shader=model_rabbit_right3_palette
)
model_rabbits_right.append(model_rabbit_right3_sprite)

model_rabbit_right4, model_rabbit_right4_palette = adafruit_imageload.load(
    "./art/model_rabbit/right4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right4_palette.make_transparent(0)
model_rabbit_right4_sprite = displayio.TileGrid(
    model_rabbit_right4,
    pixel_shader=model_rabbit_right4_palette
)
model_rabbits_right.append(model_rabbit_right4_sprite)

# Screen settings
set_home_screen = True
set_difficulty_screen = False
set_menu_screen = False
set_game_screen = False
set_stage_complete_screen = False
level = "easy"

home_screen = displayio.Group()
home_screen.append(home_bg_sprite)
home_screen.append(user_rabbit_sprite)
home_screen.append(button_to_start_sprite)

difficulty_screen = displayio.Group()
difficulty_screen.append(lightened_bg_sprite)
difficulty_screen.append(difficulties_sprite)
difficulty_screen.append(select_difficulty_sprite)
difficulty_screen.append(easy_sprite)
difficulty_screen[3].hidden = False
difficulty_screen.append(normal_sprite)
difficulty_screen[4].hidden = True
difficulty_screen.append(hard_sprite)
difficulty_screen[5].hidden = True

game_screen = displayio.Group()
game_screen.append(bg_sprite)
game_screen.append(user_rabbit_sprite)
game_screen.append(model_rabbit_sprite)

def difficulty(level_difficulty):
    if level_difficulty == "easy":
        difficulty_screen[3].hidden = True
        difficulty_screen[4].hidden = False
        level_difficulty = "normal"
    elif level_difficulty == "normal":
        difficulty_screen[4].hidden = True
        difficulty_screen[5].hidden = False
        level_difficulty = "hard"
    elif level_difficulty == "hard":
        difficulty_screen[5].hidden = True
        difficulty_screen[3].hidden = False
        level_difficulty = "easy"
    time.sleep(0.1)
    return level_difficulty

# Game loop and controls
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
                time.sleep(0.2)
    elif set_difficulty_screen:
        display.show(difficulty_screen)
        if keys[pygame.K_SPACE]:
            level = difficulty(level)
    elif set_game_screen:
        display.show(game_screen)






