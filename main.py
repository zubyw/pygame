import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Selection Menu")

# Colors
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
LIGHT_GREY = (170, 170, 170)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont(None, 50)
TITLE_FONT = pygame.font.SysFont(None, 70)

# Button settings
button_width = 300
button_height = 80
button_x = (SCREEN_WIDTH - button_width) // 2
button_y1 = 200
button_y2 = button_y1 + button_height + 50  # 50 pixels below the first button

# Define button rectangles
button1_rect = pygame.Rect(button_x, button_y1, button_width, button_height)
button2_rect = pygame.Rect(button_x, button_y2, button_width, button_height)

# Render button text
button1_text = FONT.render("Mortal Combat", True, WHITE)
button2_text = FONT.render("Gokomo", True, WHITE)

# Render title text
title_text = TITLE_FONT.render("Select Your Game", True, WHITE)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button1_rect.collidepoint(mouse_pos):
                # Launch mortalcombat.py
                script_path = os.path.join(os.getcwd(), "../brawler_tut-main/main.py")
                if os.path.exists(script_path):
                    subprocess.Popen([sys.executable, script_path])
                    running = False  # Close main menu
                else:
                    print("mortalcombat.py not found.")
            elif button2_rect.collidepoint(mouse_pos):
                # Launch gokomo.py
                script_path = os.path.join(os.getcwd(), "game.py")
                if os.path.exists(script_path):
                    subprocess.Popen([sys.executable, script_path])
                    running = False  # Close main menu
                else:
                    print("gokomo.py not found.")

    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()

    # Fill the screen with black
    SCREEN.fill(BLACK)

    # Draw title
    SCREEN.blit(title_text, title_rect)

    # Button 1 (Mortal Combat)
    if button1_rect.collidepoint(mouse_pos):
        pygame.draw.rect(SCREEN, LIGHT_GREY, button1_rect)
    else:
        pygame.draw.rect(SCREEN, GREY, button1_rect)
    pygame.draw.rect(SCREEN, WHITE, button1_rect, 2)  # Button border
    text_rect1 = button1_text.get_rect(center=button1_rect.center)
    SCREEN.blit(button1_text, text_rect1)

    # Button 2 (Gokomo)
    if button2_rect.collidepoint(mouse_pos):
        pygame.draw.rect(SCREEN, LIGHT_GREY, button2_rect)
    else:
        pygame.draw.rect(SCREEN, GREY, button2_rect)
    pygame.draw.rect(SCREEN, WHITE, button2_rect, 2)  # Button border
    text_rect2 = button2_text.get_rect(center=button2_rect.center)
    SCREEN.blit(button2_text, text_rect2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
