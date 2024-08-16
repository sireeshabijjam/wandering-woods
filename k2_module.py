import random

import pygame
import os
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def get_base_path():
    # Determine the base path
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(".")


# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
PLAYER_SIZE = 40
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60  # Countdown timer (in seconds)

# Load images
player1_img = pygame.image.load(os.path.join(
    get_base_path(), "rsc", "player_2.png"))
player2_img = pygame.image.load(os.path.join(
    get_base_path(), "rsc", "player_2.png"))
background_img = pygame.image.load(os.path.join(
    get_base_path(), "rsc", "forest.png"))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def k2_game_function():
    pygame.display.set_caption('Wandering in the Woods - K-2 Version')

    # Load sounds
    # Replace with path to your sound
    meet_sound = pygame.mixer.Sound(
        os.path.join(get_base_path(), "rsc", "meet.wav"))
    # Replace with path to your background music
    pygame.mixer.music.load(os.path.join(get_base_path(), "rsc", "music.wav"))
    pygame.mixer.music.play(-1)  # Play the background music in a loop

    player1_pos = [0, 0]
    player2_pos = [SCREEN_WIDTH - PLAYER_SIZE, SCREEN_HEIGHT - PLAYER_SIZE]

    # Countdown timer
    start_ticks = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move players
        move_randomly(player1_pos)
        move_randomly(player2_pos)

        # Check for meeting
        if player1_pos == player2_pos:
            meet_sound.play()
            print("Players have met!")
            player1_pos = [0, 0]
            player2_pos = [SCREEN_WIDTH - PLAYER_SIZE,
                           SCREEN_HEIGHT - PLAYER_SIZE]

        # Update the screen
        screen.blit(background_img, (0, 0))
        draw_grid()
        draw_players(player1_pos, player2_pos)

        # Update the countdown timer
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = MAX_TIME - seconds_passed
        if time_left <= 0:
            print("Time's up!")
            # Reset game or any other logic
            break

        pygame.display.flip()
        pygame.time.wait(500)

    pygame.quit()


def draw_grid():
    """Function to draw the grid over the background."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))


def draw_players(player1_pos, player2_pos):
    """Function to draw the players using images."""
    screen.blit(player1_img, player1_pos)
    screen.blit(player2_img, player2_pos)


def move_randomly(player_pos):
    """Function to move the player randomly."""
    direction = random.choice(['up', 'down', 'left', 'right'])
    if direction == 'up' and player_pos[1] > 0:
        player_pos[1] -= GRID_SIZE
    elif direction == 'down' and player_pos[1] < SCREEN_HEIGHT - PLAYER_SIZE:
        player_pos[1] += GRID_SIZE
    elif direction == 'left' and player_pos[0] > 0:
        player_pos[0] -= GRID_SIZE
    elif direction == 'right' and player_pos[0] < SCREEN_WIDTH - PLAYER_SIZE:
        player_pos[0] += GRID_SIZE


def draw_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.SysFont(None, 35)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (x + (width / 2), y + (height / 2))
    screen.blit(text_surf, text_rect)
    return False
