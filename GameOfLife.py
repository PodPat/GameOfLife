import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (width - button_width) // 2, height - button_height - 10

# Pause/Resume button dimensions
pause_button_x, pause_button_y = 50, height - button_height - 10
resume_button_x, resume_button_y = width - 50 - button_width, height - button_height - 10

# Save/Load button dimensions
save_button_x, save_button_y = 50, 10
load_button_x, load_button_y = width - 50 - button_width, 10

# New variables for real-time simulation
tick_interval = 1  # in seconds
last_tick = time.time()
running = True
paused = False

def draw_button(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)

def draw_buttons():
    draw_button(button_x, button_y, button_width, button_height, green, "Next Generation")
    draw_button(pause_button_x, pause_button_y, button_width, button_height, green, "Pause")
    draw_button(resume_button_x, resume_button_y, button_width, button_height, green, "Resume")
    draw_button(save_button_x, save_button_y, button_width, button_height, green, "Save")
    draw_button(load_button_x, load_button_y, button_width, button_height, green, "Load")

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

def save_state():
    np.save('game_state.npy', game_state)

def load_state():
    global game_state
    try:
        game_state = np.load('game_state.npy')
    except FileNotFoundError:
        print("No saved state found.")

# Main game loop
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_buttons()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                next_generation()
            elif pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_button_y <= event.pos[1] <= pause_button_y + button_height:
                paused = True
                print("Simulation Paused")
            elif resume_button_x <= event.pos[0] <= resume_button_x + button_width and resume_button_y <= event.pos[1] <= resume_button_y + button_height:
                paused = False
                print("Simulation Resumed")
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_button_y <= event.pos[1] <= save_button_y + button_height:
                save_state()
                print("Game state saved.")
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_button_y <= event.pos[1] <= load_button_y + button_height:
                load_state()
                print("Game state loaded.")
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_state()
                print("Game state saved.")
            elif event.key == pygame.K_l:
                load_state()
                print("Game state loaded.")

    # Real-time simulation logic
    if not paused and time.time() - last_tick > tick_interval:
        next_generation()
        last_tick = time.time()

pygame.quit()
