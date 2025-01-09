import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Selection Menu")

# Colors
BLACK, GREY, LIGHT_GREY, WHITE = (0, 0, 0), (100, 100, 100), (170, 170, 170), (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont(None, 50)
TITLE_FONT = pygame.font.SysFont(None, 70)

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_Y_POSITIONS = [200, 280, 360]  # Y positions for buttons

# Button rectangles and text
buttons = [
    {"text": "Mortal Combat", "script": "mortale_gevecht/main.py"},
    {"text": "Gokomo", "script": "ziyu/game.py"},
    {"text": "Climbing Game", "script": "zuby/climbing.py"},
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for index, button in enumerate(buttons):
                button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, BUTTON_Y_POSITIONS[index], BUTTON_WIDTH, BUTTON_HEIGHT)
                if button_rect.collidepoint(mouse_pos):
                    script_path = os.path.join(os.getcwd(), button["script"])
                    if os.path.exists(script_path):
                        subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))
                        running = False  # Close main menu

    # Fill the screen with black
    SCREEN.fill(BLACK)

    # Draw title
    title_text = TITLE_FONT.render("Select Your Game", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    SCREEN.blit(title_text, title_rect)

    # Draw buttons
    for index, button in enumerate(buttons):
        button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, BUTTON_Y_POSITIONS[index], BUTTON_WIDTH, BUTTON_HEIGHT)
        color = LIGHT_GREY if button_rect.collidepoint(pygame.mouse.get_pos()) else GREY
        pygame.draw.rect(SCREEN, color, button_rect)
        text_surface = FONT.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        SCREEN.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
