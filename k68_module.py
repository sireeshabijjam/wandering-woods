import random
import sys
import os

import pygame

# Initialize pygame and define constants
pygame.init()


def get_base_path():
    # Determine the base path
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(".")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
PLAYER_SIZE = 40
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60  # Countdown timer (in seconds)
MAX_MOVES = 10000

# Display setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering in the Woods Game: Grades 6-8')

# Variables for the Grades 6-8 version
MIN_GRID_SIZE = 10
MAX_GRID_SIZE = 20
grid_width = MIN_GRID_SIZE
grid_height = MIN_GRID_SIZE
number_of_players = 2
player_positions = []
player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                 (255, 255, 0)]  # Colors for players
background_img = pygame.image.load(os.path.join(
    get_base_path(), "rsc", "forest.png"))
player_imgs = [pygame.image.load(os.path.join(
    get_base_path(), "rsc", "player_2.png")) for _ in range(4)]
clicked = False  # Global variable for button clicks

# Additional controls for Grades 6-8
experimental_runs = 1
current_run = 1
wandering_protocol = 'Random Walk'
WANDERING_PROTOCOLS = ['Random Walk', 'Edges First', 'Center Outwards']
run_times = []
last_movement_directions = {}


# Function to draw a button on the screen
def draw_button(text, x, y, width, height, inactive_color, active_color):
    global clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and not clicked:
            clicked = True
            return True
        if click[0] == 0:
            clicked = False
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.SysFont(None, 35)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (x + (width / 2), y + (height / 2))
    screen.blit(text_surf, text_rect)
    return False


# Function to display text on the screen
def draw_text(text, x, y):
    font = pygame.font.SysFont(None, 35)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)


def move_players_based_on_protocol(positions, protocol):
    new_positions = positions.copy()

    RANDOM_FACTOR = 0.1  # 10% chance of random movement

    for idx, pos in enumerate(positions):
        directions = ['up', 'down', 'left', 'right']

        if random.random() < RANDOM_FACTOR:
            random.shuffle(directions)

        elif protocol == 'Random Walk':
            random.shuffle(directions)

        elif protocol == 'Edges First':
            x, y = pos
            if x == 0:
                directions = ['right', 'up', 'down']
            elif x == grid_width - 1:
                directions = ['left', 'up', 'down']
            elif y == 0:
                directions = ['down', 'left', 'right']
            elif y == grid_height - 1:
                directions = ['up', 'left', 'right']

        elif protocol == 'Center Outwards':
            x, y = pos
            center_x, center_y = grid_width // 2, grid_height // 2
            if x < center_x and y < center_y:
                directions = ['right', 'down'] + directions
            elif x > center_x and y < center_y:
                directions = ['left', 'down'] + directions
            elif x < center_x and y > center_y:
                directions = ['right', 'up'] + directions
            elif x > center_x and y > center_y:
                directions = ['left', 'up'] + directions

        new_pos = list(pos)
        for direction in directions:
            if direction == 'up' and new_pos[1] > 0:
                new_pos[1] -= 1
            elif direction == 'down' and new_pos[1] < grid_height - 1:
                new_pos[1] += 1
            elif direction == 'left' and new_pos[0] > 0:
                new_pos[0] -= 1
            elif direction == 'right' and new_pos[0] < grid_width - 1:
                new_pos[0] += 1

            if tuple(new_pos) not in new_positions and tuple(new_pos) not in positions:
                break
            else:
                new_pos = list(pos)

        new_positions[idx] = tuple(new_pos)
    return new_positions


def check_meetings(positions):
    """Check if any players have met and group them together."""
    met_groups = []
    single_players = []

    # Check for any meetings
    meetings = {}
    for pos in positions:
        if pos in meetings:
            meetings[pos].append(pos)
        else:
            meetings[pos] = [pos]

    # Separate out groups and single players
    for pos, met_players in meetings.items():
        if len(met_players) > 1:
            met_group = sorted(met_players)
            if met_group not in met_groups:
                met_groups.append(met_group)
        else:
            single_players.append(pos)

    return met_groups, single_players


# The Grades 6-8 game loop
def g6_8_setup_screen():
    global grid_width, grid_height, number_of_players, player_positions, wandering_protocol, experimental_runs
    global initial_player_positions

    setup_done = False
    placing_players = False
    placed_players = 0
    player_positions = []

    screen.fill(WHITE)

    while not setup_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if placing_players and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cell_x = x // GRID_SIZE
                cell_y = y // GRID_SIZE

                if (cell_x, cell_y) not in player_positions:
                    player_positions.append((cell_x, cell_y))
                    placed_players += 1
                    if placed_players == number_of_players:
                        placing_players = False
                        setup_done = True

        screen.fill(WHITE)

        # Draw the current grid
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(screen, BLACK, (x * GRID_SIZE,
                                 y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if (x, y) in player_positions:
                    pygame.draw.circle(screen, player_colors[player_positions.index((x, y))],
                                       (x * GRID_SIZE + GRID_SIZE // 2,
                                        y * GRID_SIZE + GRID_SIZE // 2),
                                       PLAYER_SIZE // 2)

        # Draw the setup options
        if not placing_players:
            # Set grid width
            if draw_button("<", 50, 50, 50, 50, BLUE, RED) and grid_width > MIN_GRID_SIZE:
                grid_width -= 1
            if draw_button(">", 150, 50, 50, 50, BLUE, RED) and grid_width < MAX_GRID_SIZE:
                grid_width += 1
            draw_text(f"Grid Width: {grid_width}", 300, 75)

            # Set grid height
            if draw_button("<", 50, 150, 50, 50, BLUE, RED) and grid_height > MIN_GRID_SIZE:
                grid_height -= 1
            if draw_button(">", 150, 150, 50, 50, BLUE, RED) and grid_height < MAX_GRID_SIZE:
                grid_height += 1
            draw_text(f"Grid Height: {grid_height}", 300, 175)

            # Set number of players
            if draw_button("<", 50, 250, 50, 50, BLUE, RED) and number_of_players > 2:
                number_of_players -= 1
            if draw_button(">", 150, 250, 50, 50, BLUE, RED) and number_of_players < 4:
                number_of_players += 1
            draw_text(f"Players: {number_of_players}", 300, 275)

            # Choose wandering protocol
            if draw_button("<", 50, 350, 50, 50, BLUE, RED):
                curr_idx = WANDERING_PROTOCOLS.index(wandering_protocol)
                wandering_protocol = WANDERING_PROTOCOLS[(
                    curr_idx - 1) % len(WANDERING_PROTOCOLS)]
            if draw_button(">", 150, 350, 50, 50, BLUE, RED):
                curr_idx = WANDERING_PROTOCOLS.index(wandering_protocol)
                wandering_protocol = WANDERING_PROTOCOLS[(
                    curr_idx + 1) % len(WANDERING_PROTOCOLS)]
            draw_text(f"Wandering Protocol: {wandering_protocol}", 300, 375)

            # Choose number of experimental runs
            if draw_button("<", 50, 450, 50, 50, BLUE, RED) and experimental_runs > 1:
                experimental_runs -= 1
            if draw_button(">", 150, 450, 50, 50, BLUE, RED):
                experimental_runs += 1
            draw_text(f"Experimental Runs: {experimental_runs}", 300, 475)

            # Start player placement
            if draw_button("Place Players", 50, 550, 250, 50, BLUE, RED):
                placing_players = True
                player_positions = []
                placed_players = 0

        pygame.display.update()

    initial_player_positions = player_positions.copy()


def g6_8_game_loop():
    global player_positions, wandering_protocol, experimental_runs
    global initial_player_positions

    pygame.display.set_caption('Wandering in the Woods - Grades 6-8 Version')

    music_path = os.path.join(get_base_path(), "rsc", "music.wav")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    meet_path = os.path.join(
        get_base_path(), "rsc", "meet.wav")
    meet_sound = pygame.mixer.Sound(meet_path)

    for run in range(experimental_runs):
        all_players = initial_player_positions.copy()
        met_groups = []
        move_count = 0
        game_over = False

        while not game_over and move_count < MAX_MOVES:
            move_count += 1

            # Move players based on the selected protocol
            all_players = move_players_based_on_protocol(
                all_players, wandering_protocol)

            # Check for meetings
            new_met_groups, all_players = check_meetings(all_players)
            print(all_players)
            met_groups.extend(new_met_groups)

            for group in new_met_groups:
                meet_sound.play()

            # Display
            screen.blit(background_img, (0, 0))
            for x in range(grid_width):
                for y in range(grid_height):
                    pygame.draw.rect(
                        screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                    pos = (x, y)
                    if pos in all_players:
                        idx = all_players.index(pos)
                        screen.blit(player_imgs[idx],
                                    (x * GRID_SIZE, y * GRID_SIZE))
                    for group in met_groups:
                        if pos in group:
                            idx = group.index(pos)
                            screen.blit(
                                player_imgs[idx], (x * GRID_SIZE, y * GRID_SIZE))

            # Check if all players have met
            if len(met_groups) == 1 and len(met_groups[0]) == number_of_players:
                game_over = True

            pygame.display.flip()
            pygame.time.wait(500)

        print(
            f"Run {run + 1}: All players met in {move_count} moves or reached max moves!")

    g6_8_setup_screen()


# Start the game
def start():
    g6_8_setup_screen()
    g6_8_game_loop()
