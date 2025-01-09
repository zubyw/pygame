import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 20
INFO_PANEL_HEIGHT = 100  # Extra ruimte voor knoppen en berichten
WIDTH = CELL_SIZE * (BOARD_SIZE - 1) + MARGIN * 2
HEIGHT = CELL_SIZE * (BOARD_SIZE - 1) + MARGIN * 2 + INFO_PANEL_HEIGHT
LINE_COLOR = (0, 0, 0)
BG_COLOR = (245, 222, 179)  # Wheat color for the board
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STONE_RADIUS = CELL_SIZE // 2 - 2
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 36
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
INFO_TEXT_COLOR = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku (Five in a Row)")

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE)
info_font = pygame.font.SysFont(None, 28)

# Game States
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'

current_state = STATE_MENU

def draw_board():
    screen.fill(BG_COLOR)
    # Draw grid lines
    for i in range(BOARD_SIZE):
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN, MARGIN + i * CELL_SIZE),
                         (WIDTH - MARGIN, MARGIN + i * CELL_SIZE), 1)
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN - INFO_PANEL_HEIGHT), 1)
    # Draw star points
    star_points = [3, 7, 11]  # Common star point positions for 15x15 board
    for i in star_points:
        for j in star_points:
            pygame.draw.circle(screen, LINE_COLOR,
                               (MARGIN + i * CELL_SIZE, MARGIN + j * CELL_SIZE),
                               5)

def get_grid_position(pos):
    x, y = pos
    # Adjust y to exclude the bottom area reserved for buttons/messages
    if y > HEIGHT - MARGIN - INFO_PANEL_HEIGHT:
        return None
    grid_x = round((x - MARGIN) / CELL_SIZE)
    grid_y = round((y - MARGIN) / CELL_SIZE)
    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
        # Snap to grid
        snapped_x = MARGIN + grid_x * CELL_SIZE
        snapped_y = MARGIN + grid_y * CELL_SIZE
        return grid_x, grid_y, snapped_x, snapped_y
    return None

def check_win(board, player, x, y):
    directions = [
        (1, 0),  # Horizontal
        (0, 1),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal up-right
    ]
    for dx, dy in directions:
        count = 1
        # Check in the positive direction
        i = 1
        while True:
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player:
                count += 1
                i += 1
            else:
                break
        # Check in the negative direction
        i = 1
        while True:
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player:
                count += 1
                i += 1
            else:
                break
        if count >= 5:
            return True
    return False

def draw_stones(board):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != 0:
                color = BLACK if board[y][x] == 1 else WHITE
                center = (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE)
                pygame.draw.circle(screen, color, center, STONE_RADIUS)
                pygame.draw.circle(screen, LINE_COLOR, center, STONE_RADIUS, 1)  # Outline

def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=5)
    text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def main_menu():
    # Draw the board background (optional)
    screen.fill(BG_COLOR)
    # Draw the "Start" button
    start_button = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2),
                               (BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_button(start_button, "Start")
    return start_button

def game_over_screen(winner):
    # Darken the board
    overlay = pygame.Surface((WIDTH, HEIGHT - INFO_PANEL_HEIGHT))
    overlay.set_alpha(180)  # Transparency
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    # Display winner message
    msg = "Black wint!" if winner == 1 else "White wint!"
    text = font.render(msg, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, MARGIN // 2))
    screen.blit(text, text_rect)
    # Draw "Home" and "Restart" buttons
    home_button = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH - 20, HEIGHT - INFO_PANEL_HEIGHT + 20),
                              (BUTTON_WIDTH, BUTTON_HEIGHT))
    restart_button = pygame.Rect((WIDTH // 2 + 20, HEIGHT - INFO_PANEL_HEIGHT + 20),
                                 (BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_button(home_button, "Home")
    draw_button(restart_button, "Herstart")
    return home_button, restart_button

def draw_info_panel(current_player):
    # Draw a rectangle for the info panel
    pygame.draw.rect(screen, (220, 220, 220), (0, HEIGHT - INFO_PANEL_HEIGHT, WIDTH, INFO_PANEL_HEIGHT))
    # Display current player's turn
    if current_player == 1:
        turn_text = "Beurt: Zwart"
        turn_color = BLACK
    else:
        turn_text = "Beurt: Wit"
        turn_color = WHITE
    text = info_font.render(turn_text, True, INFO_TEXT_COLOR)
    screen.blit(text, (MARGIN, HEIGHT - INFO_PANEL_HEIGHT + 20))

def main():
    global current_state
    draw_board()
    pygame.display.flip()

    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1  # 1 for Black, 2 for White
    game_over = False
    winner = None

    while True:
        if current_state == STATE_MENU:
            start_button = main_menu()
        elif current_state == STATE_PLAYING:
            draw_board()
            draw_stones(board)
            draw_info_panel(current_player)
        elif current_state == STATE_GAME_OVER:
            home_button, restart_button = game_over_screen(winner)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_state == STATE_MENU:
                    if start_button.collidepoint(pos):
                        # Start the game
                        current_state = STATE_PLAYING
                        # Reset the board
                        board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                        current_player = 1
                        game_over = False
                        winner = None

                elif current_state == STATE_PLAYING and not game_over:
                    grid = get_grid_position(pos)
                    if grid:
                        x, y, snapped_x, snapped_y = grid
                        if board[y][x] == 0:
                            board[y][x] = current_player
                            # Check for a win
                            if check_win(board, current_player, x, y):
                                game_over = True
                                winner = current_player
                                current_state = STATE_GAME_OVER
                            else:
                                # Switch player
                                current_player = 2 if current_player == 1 else 1

                elif current_state == STATE_GAME_OVER:
                    if home_button.collidepoint(pos):
                        # Return to main menu
                        current_state = STATE_MENU
                    elif restart_button.collidepoint(pos):
                        # Restart the game
                        current_state = STATE_PLAYING
                        board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                        current_player = 1
                        game_over = False
                        winner = None

        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
