import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Climbing Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_x = WIDTH // 2
player_y = HEIGHT - 40
player_radius = 20
player_speed = 5
velocity_y = 0
gravity = 1
is_jumping = False

# Block settings
blocks = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(400, 400, 200, 20),
    pygame.Rect(200, 300, 200, 20),
    pygame.Rect(500, 200, 200, 20),
]

# Generate new block above the highest block
def generate_new_block():
    highest_block_y = min(block.top for block in blocks)
    new_block_x = random.randint(0, WIDTH - 200)  # Random x position within screen width
    new_block_y = highest_block_y - random.randint(100, 150)  # Random height above the highest block
    return pygame.Rect(new_block_x, new_block_y, 200, 20)

# Game loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Jumping
    if keys[pygame.K_UP] and not is_jumping:
        velocity_y = -18
        is_jumping = True

    # Apply gravity
    velocity_y += gravity
    player_y += velocity_y

    # Collision with ground
    if player_y >= HEIGHT - player_radius:
        player_y = HEIGHT - player_radius
        is_jumping = False

    # Collision with blocks
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    for block in blocks:
        if player_rect.colliderect(block) and velocity_y > 0:
            player_y = block.top - player_radius
            velocity_y = 0
            is_jumping = False

    # Generate new blocks as player moves upwards
    if player_y < HEIGHT // 2:
        for block in blocks:
            block.y += 5  # Move blocks down
        player_y += 5  # Keep the player visually stable

        # Add a new block if needed
        if min(block.top for block in blocks) > 100:
            blocks.append(generate_new_block())

    # Remove blocks that go off the screen
    blocks = [block for block in blocks if block.top < HEIGHT]

    # Draw player and blocks
    pygame.draw.circle(screen, RED, (player_x, player_y), player_radius)
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    # Refresh screen
    pygame.display.flip()
    pygame.time.Clock().tick(60)
