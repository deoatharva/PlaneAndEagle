import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 700
NUM_OBSTACLES = 5  # Number of obstacles
BG_COLOR = (135, 206, 235)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planes and Birds")

# Load the images
try:
    player_image = pygame.image.load("image1.png")
    PLAYER_WIDTH, PLAYER_HEIGHT = player_image.get_size()
    
    obstacle_image = pygame.image.load("image2.png")
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = obstacle_image.get_size()
    
    game_over_image = pygame.image.load("image3.png")
    game_over_width, game_over_height = game_over_image.get_size()
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Player setup
player_rect = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT , PLAYER_WIDTH, PLAYER_HEIGHT)
player_speed = 5

# Initialize obstacles
obstacles = []
for _ in range(NUM_OBSTACLES):
    x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    y = random.randint(-HEIGHT, -OBSTACLE_HEIGHT)
    obstacles.append(pygame.Rect(x, y, OBSTACLE_WIDTH - 30, OBSTACLE_HEIGHT - 30))

obstacle_speed = 3

# Game loop
clock = pygame.time.Clock()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Ensure the player stays within the window boundaries
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH

        # Move and update obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacle.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
                obstacle.y = random.randint(-HEIGHT, -OBSTACLE_HEIGHT)

        # Collision detection
        player_rect = pygame.Rect(player_rect.x, player_rect.y, PLAYER_WIDTH - 50, PLAYER_HEIGHT - 100)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                print("Collision detected!")
                game_over = True
                break

        # Draw everything
        screen.fill(BG_COLOR)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    else:
        # Draw Game Over image
        print("Game Over!")
        game_over_x = (WIDTH - game_over_width) // 2
        game_over_y = (HEIGHT - game_over_height) // 2
        screen.blit(game_over_image, (game_over_x, game_over_y))

    pygame.display.flip()
    clock.tick(60)
