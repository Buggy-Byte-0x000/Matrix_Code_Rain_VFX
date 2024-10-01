# Code by Buggy
# Feel free to use it :)

from matrix import Matrix
from generator import Generator
import pygame
from pygame.locals import *
import sys
import os


#(settings and initiation)----------------------------------------------------------------------------------------------
FONT_SIZE = 20
MIN_DENSITY_X = FONT_SIZE/1.7  #(to avoid overlap)
MIN_DENSITY_Y = FONT_SIZE
SPEED = 10
CHAR_UPDATE_FREQ = 10
BLOOM_SCALE = 1.3
# couldn't make this work so that I could have dynamically alterable text density (like a setting that would work in par with the text scale and space)
COLS = 52
ROWS = 135

#(creates a matrix instance)
Matrix = Matrix()

#(starts the library used for 2D rendering and loads external files)
pygame.init()
pygame.mixer.init()
project_path = os.path.dirname(os.path.relpath(__file__))
font_path = os.path.join(project_path, '.venv', 'Lib', 'site-packages', 'font', 'MatrixCodeFont.ttf')
sfx1_path = os.path.join(project_path, '.venv', 'Lib', 'site-packages', 'sfx', 'beep1.mp3')
sfx2_path = os.path.join(project_path, '.venv', 'Lib', 'site-packages', 'sfx', 'beep2.mp3')
sfx3_path = os.path.join(project_path, '.venv', 'Lib', 'site-packages', 'sfx', 'beep3.mp3')
font = pygame.font.Font(font_path, FONT_SIZE)
sfx_1 = pygame.mixer.Sound(sfx1_path)
sfx_2 = pygame.mixer.Sound(sfx2_path)
sfx_3 = pygame.mixer.Sound(sfx3_path)

#(creates a fullscreen window)
flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
screen = pygame.display.set_mode((1920, 1080), flags, 16)
pygame.mouse.set_visible(False)


#(CENTRAL TICK LOOP)----------------------------------------------------------------------------------------------------
running = True
quit_animation = False
keystroke_effect = False
keystroke_effect_choice = 0
keystroke_effect_start = -1
keystroke_effect_end = -1
end = -1
quit_animation_countdown = 70
keystroke_effect_countdown = -1
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4:
                if quit_animation:
                    quit_animation_countdown = 0
                quit_animation = True
            else:
                if not keystroke_effect:
                    keystroke_effect = True
                    keystroke_effect_choice = Generator.random_number(1, 4)
                    sfx_choice = Generator.random_number(1, 3)
                    start_scanline_effect(keystroke_effect_choice)
                if sfx_choice == 1:
                    sfx_1.play()
                elif sfx_choice == 2:
                    sfx_2.play()
                else:
                    sfx_3.play()


    #(clears previous frame or does a quit animation)
    if not quit_animation:
        screen.fill((0,0,0))
    else:
        if quit_animation_countdown != 0:
            quit_animation_countdown -= 1
        else:
            pygame.quit()
            sys.exit()

    #(scanline effect animation)
    if keystroke_effect:
        if keystroke_effect_choice in [1,2]:
            keystroke_effect_countdown -= 1
            if keystroke_effect_countdown == 0:
                keystroke_effect = False
        elif keystroke_effect_choice in [3,4]:
            if keystroke_effect_start <= end:
                if keystroke_effect_choice == 3:
                    keystroke_effect_start += 5
                    keystroke_effect_end += 5
                else:
                    keystroke_effect_start += 15
                    keystroke_effect_end += 15
            else:
                keystroke_effect = False


    #(frame)-----------------------------------------------------------------------------------------------------------
    for x in range(ROWS):
        Streak_instance = Matrix.get_Streak_instance(x)
        streak_live = Streak_instance.get_status()
        for y in range(COLS):
            streak_opacities = Streak_instance.get_opacities()
            if streak_opacities[y] > 0:  #(performance optimization)
                streak_chars = Streak_instance.get_streak()
                streak_colors_red = Streak_instance.get_colors_red()
                streak_colors_green = Streak_instance.get_colors_green()
                streak_colors_blue = Streak_instance.get_colors_blue()

                char = streak_chars[y]
                opacity = streak_opacities[y]
                color_red = streak_colors_red[y]
                color_green = streak_colors_green[y]
                color_blue = streak_colors_blue[y]

                #(scanline effect)
                if keystroke_effect:
                    vertical = keystroke_effect_choice in [1,3]
                    horizontal = keystroke_effect_choice in [2, 4]
                    vertical_range = keystroke_effect_end >= y >= keystroke_effect_start
                    horizontal_range = keystroke_effect_end >= x >= keystroke_effect_start
                    in_range = (vertical and vertical_range) or (horizontal and horizontal_range)
                    if in_range:
                        opacity = 255
                        color_red = 255
                        color_green = 255
                        color_blue = 255

                #(text)
                text_surface = font.render(str(char), True, (color_red, color_green, color_blue))
                density_x = FONT_SIZE * 0.25 + x * MIN_DENSITY_X
                density_y = FONT_SIZE * 0.5 + y * MIN_DENSITY_Y
                text_rect = text_surface.get_rect(center=(density_x, density_y))

                #(RGB split)
                red_channel_surface = font.render(str(char), True, (color_red, 0, 0))
                red_channel_surface.set_alpha(opacity)
                green_channel_surface = font.render(str(char), True, (0, color_green, 0))
                green_channel_surface.set_alpha(opacity)
                blue_channel_surface = font.render(str(char), True, (0, 0, color_blue))
                blue_channel_surface.set_alpha(opacity)

                #(bloom)
                copy = text_surface.copy()
                size_x, size_y = text_rect.width, text_rect.height
                scaled_down = pygame.transform.smoothscale(copy, (size_x * 0.5, size_y * 0.5))
                bloom = pygame.transform.smoothscale(scaled_down, (size_x * BLOOM_SCALE, size_y * BLOOM_SCALE))
                if opacity != 255:
                    bloom.set_alpha(opacity*0.7)
                bloom_rect = bloom.get_rect(center=(density_x, density_y))

                #(render plus chromatic aberration)
                screen.blit(red_channel_surface, text_rect.move(2, 0))
                screen.blit(blue_channel_surface, text_rect.move(-2, 0))
                screen.blit(bloom, bloom_rect)
                screen.blit(green_channel_surface, text_rect)


                def start_scanline_effect(effect_choice):
                    global keystroke_effect_start, keystroke_effect_end, keystroke_effect_countdown, end

                    if effect_choice in [1,2]:
                        keystroke_effect_countdown = 6
                        if effect_choice == 1:
                            keystroke_effect_start = Generator.random_number(0, 52)
                            keystroke_effect_end = keystroke_effect_start + Generator.random_number(6, 8)
                        else:
                            keystroke_effect_start = Generator.random_number(0, 135)
                            keystroke_effect_end = keystroke_effect_start + Generator.random_number(8, 10)

                    elif effect_choice in [3,4]:
                        if effect_choice == 3:
                            end = 52
                            keystroke_effect_start = -10
                            keystroke_effect_end = 0
                        else:
                            end = 135
                            keystroke_effect_start = -10
                            keystroke_effect_end = 0


    #(update for the next frame)
    #clock.tick()
    #print(clock.get_fps())
    pygame.display.update()
    Matrix.update()