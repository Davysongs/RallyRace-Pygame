import os
import random
import sys
import time
import pygame
from pygame.locals import *

screen_width = 800
screen_height = 600
txt_c = (255, 255, 0)
bckg_c = (0, 0, 0)
FPS = 120
minimum_size_car = 10
maximum_size_car = 40
minimum_speed_car = 8
maximum_speed_car = 8
new_rate_car_added = 6
pl_movement_rate = 5
counting_seconds = 3

def Exit():
    pygame.quit()
    sys.exit()


def Press_Key_shortcut(): # waiting for player to press any key
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    Exit()
                return


def player_crash(pl_crashRect, opponent):
    for ado in opponent:
        if pl_crashRect.colliderect(ado['rect']):
            return True
    return False


def txt_objects(t, f, s, x, y):
    txt_objects = f.render(t, 1, txt_c)
    txt_Rect = txt_objects.get_rect()
    txt_Rect.topleft = (x, y)
    s.blit(txt_objects, txt_Rect)


# set up pygame, the window, and the mouse cursor
pygame.init()
time_clock = pygame.time.Clock()
screen_display_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont('Arial', 30)

# sounds
game_over_music = pygame.mixer.Sound('audio_sound/crash.wav')
pygame.mixer.music.load('audio_sound/loop.wav')
chuckle = pygame.mixer.Sound('audio_sound/done.mp3')

# images
car1 = pygame.image.load('image/car1.png')
car2 = pygame.image.load('image/car2.png')
car3 = pygame.image.load('image/car3.png')
player_car_photo = pygame.image.load('image/car4.png')
car5 = pygame.image.load('image/car5.png')
car6 = pygame.image.load('image/car6.png')
car7 = pygame.image.load('image/car2.png')
another = [car1, car2, car3, car5, car6, car7]
gamer_Rect = player_car_photo.get_rect()
w_left = pygame.image.load('image/left_side.png')
w_right = pygame.image.load('image/right_side.png')

# "welcome" screen
datafile = open("datafiles/save.dat", 'r')
highest_score = int(datafile.readline())
datafile.close()
txt_objects('RALLY RACE', font, screen_display_window, (screen_width / 3) - 30, (screen_height / 3))
txt_objects('Press any key to begin', font, screen_display_window, (screen_width / 3), (screen_height / 3) + 30)
txt_objects(f'Score to beat : {highest_score}', font, screen_display_window, (screen_width / 3), (screen_height / 3) + 60)
pygame.display.update()
Press_Key_shortcut()
zero = 0
if not os.path.exists("datafiles/save.dat"):
    ado = open("datafiles/save.dat", 'w')
    ado.write(str(zero))
    ado.close()
while (counting_seconds > 0):
    # start of the game
    opponent = []
    score = 0
    gamer_Rect.topleft = (screen_width / 2, screen_height - 50)
    moving_left = moving_right = moving_up = moving_down = False
    counter_reverse = slowing_reverse = False
    adding_counter_opponent = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # the game loop
        score += 1  # increase score

        for event in pygame.event.get():

            if event.type == QUIT:
                Exit()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    counter_reverse = True
                if event.key == ord('x'):
                    slowing_reverse = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moving_right = False
                    moving_left = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moving_left = False
                    moving_right = True
                if event.key == K_UP or event.key == ord('w'):
                    moving_down = False
                    moving_up = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moving_up = False
                    moving_down = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    counter_reverse = False
                    score = 0
                if event.key == ord('x'):
                    slowing_reverse = False
                    score = 0
                if event.key == K_ESCAPE:
                    Exit()

                if event.key == K_LEFT or event.key == ord('a'):
                    moving_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moving_right = False
                if event.key == K_UP or event.key == ord('w'):
                    moving_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moving_down = False

        # Add new car at the top of the screen
        if not counter_reverse and not slowing_reverse:
            adding_counter_opponent += 1
        if adding_counter_opponent == new_rate_car_added:
            adding_counter_opponent = 0
            computer_car_size = 30
            new_computer_car = {'rect': pygame.Rect(random.randint(140, 485), 0 - computer_car_size, 23, 47),
                         'speed': random.randint(minimum_speed_car, maximum_speed_car),
                         'surface': pygame.transform.scale(random.choice(another), (23, 47)),
                                }
            opponent.append(new_computer_car)
            left_side = {'rect': pygame.Rect(0, 0, 126, 600),
                        'speed': random.randint(minimum_speed_car, maximum_speed_car),
                        'surface': pygame.transform.scale(w_left, (126, 599)),
                         }
            opponent.append(left_side)
            right_side = {'rect': pygame.Rect(497, 0, 303, 600),
                         'speed': random.randint(minimum_speed_car, maximum_speed_car),
                         'surface': pygame.transform.scale(w_right, (203, 599)),
                          }
            opponent.append(right_side)

        # Move the player around.
        if moving_left and gamer_Rect.left > 0:
            gamer_Rect.move_ip(-1.5 * pl_movement_rate, 0)
        if moving_right and gamer_Rect.right < screen_width:
            gamer_Rect.move_ip(1.5 * pl_movement_rate, 0)
        if moving_up and gamer_Rect.top > 0:
            gamer_Rect.move_ip(0, -1.5 * pl_movement_rate)
        if moving_down and gamer_Rect.bottom < screen_height:
            gamer_Rect.move_ip(0, pl_movement_rate)

        for car in opponent:
            if not counter_reverse and not slowing_reverse:
                car['rect'].move_ip(0, car['speed'])
            elif counter_reverse:
                car['rect'].move_ip(0, -5)
            elif slowing_reverse:
                car['rect'].move_ip(0, 1)

        for car in opponent[:]:
            if car['rect'].top > screen_height:
                opponent.remove(car)

        # Draw the game world on the window.
        screen_display_window.fill(bckg_c)

        # Draw the score and top score.
        def txt_objects(text, font, color, bg_color, x, y):
            # Render the text onto a surface with the specified font and color
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            
            # Create a surface for the background color and blit it behind the text
            bg_surface = pygame.Surface((text_rect.width, text_rect.height))
            bg_surface.fill(bg_color)
            screen_display_window.blit(bg_surface, text_rect)

            # Blit the text onto the main display surface
            screen_display_window.blit(text_surface, text_rect)

        # Example usage:
        txt_objects('Score: %s' % (score), font, txt_c, bckg_c, 80, 0)
        txt_objects('High score: %s' % (highest_score), font, txt_c, bckg_c, 220, 0)
        txt_objects('LIFE: %s' % (counting_seconds), font, txt_c, bckg_c, 428, 0)


        screen_display_window.blit(player_car_photo, gamer_Rect)

        for car in opponent:
            screen_display_window.blit(car['surface'], car['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if player_crash(gamer_Rect, opponent):
            if score > highest_score:
                g = open("datafiles/save.dat", 'w')
                g.write(str(score))
                g.close()
                highest_score = score
            break

        time_clock.tick(FPS)

    # "Game Over" screen.
    pygame.mixer.music.stop()
    counting_seconds = counting_seconds - 1
    game_over_music.play()
    time.sleep(1)
    if (counting_seconds == 0):
        chuckle.play()
        txt_objects('GAME OVER', font, screen_display_window, (screen_width / 3), (screen_height / 3))
        txt_objects('Press any key to try again.', font, screen_display_window, (screen_width / 3) - 80, (screen_height / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        Press_Key_shortcut()
        counting_seconds = 3
        game_over_music.stop()
