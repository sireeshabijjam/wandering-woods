import random
import sys
import os
import pygame

# Re-initializing pygame and other constants
pygame.init()


def get_base_path():
    # Determine the base path
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(".")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
PLAYER_SIZE = 40
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60  # Countdown timer (in seconds)

# Setting up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering in the Woods Game')

# Grades 3-5 Game Version: Setup Screen
MIN_GRID_SIZE = 10
MAX_GRID_SIZE = 20
grid_width = MIN_GRID_SIZE
grid_height = MIN_GRID_SIZE
number_of_players = 2
player_positions = []
player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
background_img = pygame.image.load(os.path.join(
    get_base_path(), "rsc", "forest.png"))
player_imgs = [
    pygame.image.load(os.path.join(
        get_base_path(), "rsc", "player_2.png")),
    pygame.image.load(os.path.join(
        get_base_path(), "rsc", "player_2.png")),
    pygame.image.load(os.path.join(
        get_base_path(), "rsc", "player_2.png")),
    pygame.image.load(os.path.join(
        get_base_path(), "rsc", "player_2.png")),
]

clicked = False  # Global variable to keep track of button clicks

# New variables to store game statistics
longest_run = 0
shortest_run = float('inf')
total_runs = 0
total_time_taken = 0


def update_statistics(run_time):
    global longest_run, shortest_run, total_runs, total_time_taken

    longest_run = max(longest_run, run_time)
    shortest_run = min(shortest_run, run_time)
    total_runs += 1
    total_time_taken += run_time


def display_statistics():
    avg_run = total_time_taken / total_runs if total_runs > 0 else 0

    font = pygame.font.SysFont(None, 50)

    longest_str = f"Longest Run: {longest_run:.2f} seconds"
    text_surf = font.render(longest_str, True, RED)
    text_rect = text_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(text_surf, text_rect)

    shortest_str = f"Shortest Run: {shortest_run:.2f} seconds"
    text_surf = font.render(shortest_str, True, RED)
    text_rect = text_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surf, text_rect)

    avg_str = f"Average Run: {avg_run:.2f} seconds"
    text_surf = font.render(avg_str, True, RED)
    text_rect = text_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    pygame.time.wait(3000)  # Show for 3 seconds


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


def g3_5_setup_screen():
    global grid_width, grid_height, number_of_players, player_positions

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

        # If not placing players, draw the setup options
        if not placing_players:
            # Allow user to choose grid width
            if draw_button("<", 50, 50, 50, 50, BLUE, RED) and grid_width > MIN_GRID_SIZE:
                grid_width -= 1
            if draw_button(">", 150, 50, 50, 50, BLUE, RED) and grid_width < MAX_GRID_SIZE:
                grid_width += 1
            draw_text(f"Grid Width: {grid_width}", 300, 75)

            # Allow user to choose grid height
            if draw_button("<", 50, 150, 50, 50, BLUE, RED) and grid_height > MIN_GRID_SIZE:
                grid_height -= 1
            if draw_button(">", 150, 150, 50, 50, BLUE, RED) and grid_height < MAX_GRID_SIZE:
                grid_height += 1
            draw_text(f"Grid Height: {grid_height}", 300, 175)

            # Allow user to choose number of players
            if draw_button("<", 50, 250, 50, 50, BLUE, RED) and number_of_players > 2:
                number_of_players -= 1
            if draw_button(">", 150, 250, 50, 50, BLUE, RED) and number_of_players < 4:
                number_of_players += 1
            draw_text(f"Players: {number_of_players}", 300, 275)

            # Start player placement
            if draw_button("Place Players", 50, 350, 250, 50, BLUE, RED):
                placing_players = True
                player_positions = []
                placed_players = 0

        pygame.display.update()


def draw_text(text, x, y):
    font = pygame.font.SysFont(None, 35)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)


def move_players_randomly(positions, met_groups):
    """Function to move multiple players and groups randomly."""
    new_positions = positions.copy()
    occupied_positions = set(positions + [group[0] for group in met_groups])
    # To track positions players have moved to in this iteration
    new_occupied_positions = set()

    for idx, pos in enumerate(positions):
        direction = random.choice(['up', 'down', 'left', 'right'])
        new_pos = list(pos)
        if direction == 'up' and new_pos[1] > 0:
            new_pos[1] -= 1
        elif direction == 'down' and new_pos[1] < grid_height - 1:
            new_pos[1] += 1
        elif direction == 'left' and new_pos[0] > 0:
            new_pos[0] -= 1
        elif direction == 'right' and new_pos[0] < grid_width - 1:
            new_pos[0] += 1

        # If the new position isn't occupied, update the position
        if tuple(new_pos) not in occupied_positions and tuple(new_pos) not in new_occupied_positions:
            new_positions[idx] = tuple(new_pos)
            new_occupied_positions.add(tuple(new_pos))

    # Move groups
    for group in met_groups:
        direction = random.choice(['up', 'down', 'left', 'right'])
        new_group_pos = list(group[0])
        if direction == 'up' and new_group_pos[1] > 0:
            new_group_pos[1] -= 1
        elif direction == 'down' and new_group_pos[1] < grid_height - 1:
            new_group_pos[1] += 1
        elif direction == 'left' and new_group_pos[0] > 0:
            new_group_pos[0] -= 1
        elif direction == 'right' and new_group_pos[0] < grid_width - 1:
            new_group_pos[0] += 1

        # If the new group position isn't occupied, update the group's position
        if tuple(new_group_pos) not in new_positions and tuple(new_group_pos) not in occupied_positions and tuple(
                new_group_pos) not in new_occupied_positions:
            for idx in range(len(group)):
                group[idx] = tuple(new_group_pos)
            new_occupied_positions.add(tuple(new_group_pos))

    return new_positions, met_groups


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
            met_groups.append(met_players)
        else:
            single_players.append(pos)

    return met_groups, single_players


def display_timer(time_left):
    font = pygame.font.SysFont(None, 50)
    mins = int(time_left) // 60
    secs = int(time_left) % 60
    time_str = f"{mins:02}:{secs:02}"
    text_surf = font.render(time_str, True, RED)
    text_rect = text_surf.get_rect()
    text_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
    screen.blit(text_surf, text_rect)


def handle_time_out():
    font = pygame.font.SysFont(None, 100)
    text_surf = font.render("TIME OUT", True, RED)
    text_rect = text_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surf, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Show for 3 seconds
    pygame.mixer.music.stop()
    g3_5_setup_screen()


def g3_5_game_loop():
    timer = 180  # 3 minutes in seconds
    start_time = timer

    global player_positions

    pygame.display.set_caption('Wandering in the Woods - Grades 3-5 Version')
    music_path = os.path.join(get_base_path(), "rsc", "music.wav")

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    meet_path = pos.path.join(get_base_path(), "rsc", "meet.wav")
    meet_sound = pygame.mixer.Sound(meet_path)

    all_players = player_positions.copy()
    met_groups = []
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_timer(timer)
        timer -= 0.5
        if timer <= 0:
            handle_time_out()
            return

        all_players, met_groups = move_players_randomly(
            all_players, met_groups)

        new_met_groups, all_players = check_meetings(all_players)
        met_groups.extend(new_met_groups)

        for group in new_met_groups:
            meet_sound.play()

        screen.blit(background_img, (0, 0))

        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(screen, BLACK, (x * GRID_SIZE,
                                 y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                pos = (x, y)
                if pos in all_players:
                    idx = all_players.index(pos)
                    screen.blit(player_imgs[idx],
                                (x * GRID_SIZE, y * GRID_SIZE))
                for group in met_groups:
                    if pos in group:
                        idx = group.index(pos)
                        screen.blit(player_imgs[idx],
                                    (x * GRID_SIZE, y * GRID_SIZE))

        if len(met_groups) == 1 and len(met_groups[0]) == number_of_players:
            game_time_taken = start_time - timer
            update_statistics(game_time_taken)
            display_statistics()
            g3_5_setup_screen()

        pygame.display.flip()
        pygame.time.wait(500)


def start():
    while True:
        g3_5_setup_screen()
        g3_5_game_loop()
