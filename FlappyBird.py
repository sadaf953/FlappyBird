import pygame
import random
import sys
import os
from pygame.locals import *

# Game Constants and Variables
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
ELEVATION = WINDOW_HEIGHT * 0.8
FPS = 60

# Physics constants - Adjusted for better gameplay
GRAVITY = 0.3
FLAP_POWER = -5.5
PIPE_SPEED = 2.5
PIPE_GAP = 160
PIPE_FREQUENCY = 2000  # Time in milliseconds between pipe spawns

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (67, 176, 71)
BIRD_YELLOW = (255, 215, 0)

def create_programmatic_images():
    """Create game images programmatically"""
    images = {}
    
    # Create bird surface
    bird_surface = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(bird_surface, BIRD_YELLOW, (0, 0, 40, 30))
    pygame.draw.ellipse(bird_surface, (200, 160, 0), (0, 0, 40, 30), 2)  # Outline
    pygame.draw.circle(bird_surface, BLACK, (30, 12), 3)  # Eye
    images['flappybird'] = bird_surface
    
    # Create pipe surface
    pipe_surface = pygame.Surface((80, 500), pygame.SRCALPHA)
    pygame.draw.rect(pipe_surface, PIPE_GREEN, (0, 0, 80, 500))
    pygame.draw.rect(pipe_surface, (50, 150, 50), (0, 0, 80, 500), 3)  # Darker outline
    pygame.draw.rect(pipe_surface, (90, 190, 90), (5, 0, 70, 30))  # Pipe top
    images['pipeimage'] = (
        pipe_surface,  # Original pipe for bottom
        pygame.transform.flip(pipe_surface, False, True)  # Flipped pipe for top
    )
    
    # Create background
    bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg_surface.fill(SKY_BLUE)
    # Add some simple clouds
    for _ in range(5):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT//2)
        pygame.draw.ellipse(bg_surface, WHITE, (x, y, 60, 30))
    images['background'] = bg_surface
    
    # Create ground
    ground_surface = pygame.Surface((WINDOW_WIDTH, int(WINDOW_HEIGHT - ELEVATION)))
    ground_surface.fill((210, 180, 140))  # Sandy color
    # Add some texture
    for _ in range(20):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, int(WINDOW_HEIGHT - ELEVATION))
        pygame.draw.circle(ground_surface, (180, 150, 120), (x, y), 3)
    images['sea_level'] = ground_surface
    
    return images

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create programmatic images
game_images = create_programmatic_images()

def create_pipe():
    """Creates a new pair of pipes"""
    pipe_height = game_images['pipeimage'][0].get_height()
    gap_y = random.randrange(150, WINDOW_HEIGHT - PIPE_GAP - 150)  # Adjusted range for better gaps
    pipe_x = WINDOW_WIDTH + 10
    
    pipe = [
        {'x': pipe_x, 'y': gap_y - pipe_height},  # Upper pipe
        {'x': pipe_x, 'y': gap_y + PIPE_GAP}      # Lower pipe
    ]
    return pipe

def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    """Check if the game is over"""
    bird_rect = pygame.Rect(horizontal, vertical, 
                          game_images['flappybird'].get_width(),
                          game_images['flappybird'].get_height())
    
    # Bird hits the ground or ceiling
    if vertical > ELEVATION - 25 or vertical < 0:
        return True
        
    # Check collision with pipes
    for pipe in up_pipes + down_pipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'],
                              game_images['pipeimage'][0].get_width(),
                              game_images['pipeimage'][0].get_height())
        if bird_rect.colliderect(pipe_rect):
            return True
            
    return False

def show_score(score):
    """Display score on screen"""
    font = pygame.font.Font(None, 48)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    
    # Add shadow effect for better visibility
    shadow_surface = font.render(f'Score: {score}', True, BLACK)
    shadow_rect = score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2
    
    window.blit(shadow_surface, shadow_rect)
    window.blit(score_surface, score_rect)

def flappy_game():
    """Main game function"""
    score = 0
    horizontal = int(WINDOW_WIDTH/5)
    vertical = int(WINDOW_HEIGHT/2)
    bird_velocity = 0
    rotation = 0  # Bird rotation angle
    
    # Create first two pipes
    first_pipe = create_pipe()
    second_pipe = create_pipe()
    second_pipe[0]['x'] = first_pipe[0]['x'] + WINDOW_WIDTH/2
    second_pipe[1]['x'] = first_pipe[1]['x'] + WINDOW_WIDTH/2
    
    # List of pipes
    up_pipes = [first_pipe[0], second_pipe[0]]
    down_pipes = [first_pipe[1], second_pipe[1]]
    
    passed_pipe = False
    last_pipe_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird_velocity = FLAP_POWER
                rotation = 20  # Rotate bird up when flapping
        
        # Update bird position and rotation
        bird_velocity += GRAVITY
        vertical += bird_velocity
        
        # Rotate bird based on velocity
        if bird_velocity < 0:
            rotation = min(rotation + 2, 20)
        else:
            rotation = max(rotation - 2, -90)
        
        # Rotate bird image
        rotated_bird = pygame.transform.rotate(game_images['flappybird'], rotation)
        
        # Check for game over
        if is_game_over(horizontal, vertical, up_pipes, down_pipes):
            return score
        
        # Move pipes to the left
        for pipe in up_pipes + down_pipes:
            pipe['x'] -= PIPE_SPEED
        
        # Check if bird has passed a pipe
        pipe_mid = up_pipes[0]['x'] + game_images['pipeimage'][0].get_width()/2
        if not passed_pipe and horizontal > pipe_mid:
            score += 1
            passed_pipe = True
        
        # Add new pipe when first pipe is about to cross the leftmost part
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])
            up_pipes.pop(0)
            down_pipes.pop(0)
            passed_pipe = False
        
        # Draw everything
        window.blit(game_images['background'], (0, 0))
        
        # Draw pipes
        for pipe in up_pipes + down_pipes:
            if pipe in up_pipes:
                window.blit(game_images['pipeimage'][0], (pipe['x'], pipe['y']))
            else:
                window.blit(game_images['pipeimage'][1], (pipe['x'], pipe['y']))
        
        window.blit(game_images['sea_level'], (0, ELEVATION))
        
        # Get the rect for the rotated bird
        bird_rect = rotated_bird.get_rect(center=(horizontal + game_images['flappybird'].get_width()/2,
                                                 vertical + game_images['flappybird'].get_height()/2))
        window.blit(rotated_bird, bird_rect.topleft)
        
        show_score(score)
        pygame.display.update()
        clock.tick(FPS)

def show_game_over(score):
    """Show game over screen with animation"""
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill(BLACK)
    
    for alpha in range(0, 128, 2):  # Fade in animation
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)
    
    font = pygame.font.Font(None, 64)
    text = font.render(f"Game Over!", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
    
    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10))
    
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Press SPACE to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 70))
    
    window.blit(text, text_rect)
    window.blit(score_text, score_rect)
    window.blit(restart_text, restart_rect)
    pygame.display.update()
    
    pygame.time.wait(500)  # Wait before accepting input

def main():
    """Main game loop"""
    clock = pygame.time.Clock()
    
    while True:
        window.blit(game_images['background'], (0, 0))
        
        # Show welcome message
        font = pygame.font.Font(None, 48)
        text = font.render("Flappy Bird", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/3))
        window.blit(text, text_rect)
        
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        window.blit(start_text, start_rect)
        
        # Show bird in welcome screen
        bird_rect = game_images['flappybird'].get_rect(center=(WINDOW_WIDTH/3, WINDOW_HEIGHT/2))
        window.blit(game_images['flappybird'], bird_rect)
        window.blit(game_images['sea_level'], (0, ELEVATION))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                score = flappy_game()
                show_game_over(score)
        
        clock.tick(FPS)

if __name__ == "__main__":
    main()
