import sys

import pygame

import k2_module as k2
import k35_module as k35
import k68_module as k68

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Setting up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering in the Woods Game')


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


def menu_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw buttons
        k2_button = draw_button("K-2", 100, 100, 200, 50, BLUE, RED)
        g3_5_button = draw_button("3-5", 100, 175, 200, 50, BLUE, RED)
        g6_8_button = draw_button("6-8", 100, 250, 200, 50, BLUE, RED)

        if k2_button:
            # Start the K-2 version (existing code)
            k2.k2_game_function()  # This function should contain the main K-2 game logic
        elif g3_5_button:
            k35.start()
        elif g6_8_button:
            k68.start()
        pygame.display.update()


# Call the menu screen

menu_screen()
