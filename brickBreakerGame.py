import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Green paddle
ORANGE = (255, 165, 0)  # Orange ball
YELLOW = (255, 255, 0)  # Yellow counters
LIVES = 3

# Displying background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Function to display the menu
def show_menu():
    menu_font = pygame.font.Font(None, 48)
    menu_title = menu_font.render("Brick Breaker", True, YELLOW)
    menu_start = menu_font.render("1. Start Game", True, YELLOW)
    menu_high_score = menu_font.render("2. View High Score", True, YELLOW)
    menu_exit = menu_font.render("3. Exit", True, YELLOW)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start Game
                    return
                elif event.key == pygame.K_2:  # View High Score
                    print("High Score: TODO")  # Replace TODO with your high score logic
                elif event.key == pygame.K_3:  # Exit
                    pygame.quit()
                    sys.exit()

        screen.blit(background_image, (0, 0))  # Draw background image

        # Draw menu
        menu_title_rect = menu_title.get_rect(center=(WIDTH // 2, 100))
        menu_start_rect = menu_start.get_rect(center=(WIDTH // 2, 200))
        menu_high_score_rect = menu_high_score.get_rect(center=(WIDTH // 2, 250))
        menu_exit_rect = menu_exit.get_rect(center=(WIDTH // 2, 300))

        screen.blit(menu_title, menu_title_rect)
        screen.blit(menu_start, menu_start_rect)
        screen.blit(menu_high_score, menu_high_score_rect)
        screen.blit(menu_exit, menu_exit_rect)

        pygame.display.flip()
        clock.tick(60)

# Create the paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [2, 2]

# Create bricks with equally distributed colors
colors = [RED, BLUE, GREEN]
bricks = []
for row in range(5):
    for col in range(WIDTH // BRICK_WIDTH):
        brick_color = random.choice(colors)
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append((brick, brick_color))

# Initialize game variables
score = 0
lives = LIVES
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Move the paddle with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(5, 0)

        # Move the ball
        ball.move_ip(ball_speed)

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # Ball collision with paddle
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]

        # Ball collision with bricks
        for brick, brick_color in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove((brick, brick_color))
                score += 3 if brick_color == RED else 2 if brick_color == BLUE else 1

        # Check if all bricks are destroyed
        if not bricks:
            game_over = True  # Player wins
            show_menu()  # Display menu when the player wins

        # Check if the ball reaches the bottom
        if ball.top > HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True  # Player loses
                show_menu()  # Display menu when the player loses

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw background image
        pygame.draw.rect(screen, GREEN, paddle)  # Green paddle
        pygame.draw.circle(screen, ORANGE, ball.center, BALL_RADIUS)  # Orange ball

        for brick, brick_color in bricks:
            # Draw bricks with a thin gray outline
            pygame.draw.rect(screen, (169, 169, 169), brick, 1)
            pygame.draw.rect(screen, brick_color, brick)

        # Display score and lives in yellow
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, YELLOW)
        lives_text = font.render(f"Lives: {lives}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)
