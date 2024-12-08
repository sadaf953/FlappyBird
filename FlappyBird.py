import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions (Increased size)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Adjusted screen size for a larger window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors (Will be used if needed for other parts of the game)
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)

# Game settings (Slower and easier settings)
FPS = 60
GRAVITY = 0.2  # Reduced gravity for slower fall
FLAP_STRENGTH = -7  # Weakened flap strength for slower upward movement
PIPE_SPEED = 1  # Slower pipe movement
PIPE_WIDTH = 180
PIPE_GAP = 200  # Increased gap between pipes to make it easier to pass
PIPE_CREATION_TIME = 150  # Increased time between creating pipes

# Bird settings
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_width = 40  # Adjust bird width
bird_height = 20  # Adjust bird height
bird_velocity = 0

# Pipe settings
pipe_list = []
pipe_timer = 0

# Fonts
font = pygame.font.SysFont("Arial", 32)

# Game state
score = 0
running = True
game_over = False

# Load bird images dynamically
bird_images = [pygame.image.load(f'bird{i}.png').convert_alpha() for i in range(1, 4)]

# Resize bird images to match bird dimensions
bird_images = [pygame.transform.scale(image, (bird_width, bird_height)) for image in bird_images]

# Select a bird image (default to first bird)
current_bird_image = bird_images[0]

# Load background image dynamically
background_image = pygame.image.load('background.png').convert_alpha()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load pipe images
pipe_image = pygame.image.load('pipe.png').convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, int(SCREEN_HEIGHT / 2)))

# Function to change bird image
def change_bird_image(index):
    global current_bird_image
    if 0 <= index < len(bird_images):
        current_bird_image = bird_images[index]

# Function to change background image
def change_background_image(image_path):
    global background_image
    background_image = pygame.image.load(image_path).convert_alpha()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Example usage: change bird to second image and update background
change_bird_image(1)
change_background_image('background.png')

# Functions
def create_pipe():
    """Create a new pipe with a random gap position."""
    gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(SCREEN_WIDTH + 50, 0, PIPE_WIDTH, gap_y)  # Start pipes slightly off-screen
    bottom_pipe = pygame.Rect(SCREEN_WIDTH + 50, gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - gap_y - PIPE_GAP)
    return top_pipe, bottom_pipe

def draw_pipes(pipes):
    """Draw all pipes on the screen using images."""
    for pipe in pipes:
        if pipe.y == 0:
            # Upper pipe, rotate the image
            rotated_pipe = pygame.transform.rotate(pipe_image, 180)
            screen.blit(rotated_pipe, pipe)
        else:
            # Lower pipe
            screen.blit(pipe_image, pipe)

def check_collision(bird_rect, pipes):
    """Check if the bird collides with any pipes or the ground."""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def flappygame():
    global running, game_over, score, pipe_list, pipe_timer, bird_y, bird_velocity
    clock = pygame.time.Clock()
    while running:
        screen.fill(BLUE)  # Background color to fill screen in case image fails to load

        # Draw the background image
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = FLAP_STRENGTH  # Flap the bird
                if event.key == pygame.K_SPACE and game_over:
                    # Restart the game
                    game_over = False
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipe_list = []
                    score = 0

                # Change bird image with up and down arrow keys
                if event.key == pygame.K_UP:
                    change_bird_image((bird_images.index(current_bird_image) + 1) % len(bird_images))
                elif event.key == pygame.K_DOWN:
                    change_bird_image((bird_images.index(current_bird_image) - 1) % len(bird_images))

        if not game_over:
            # Bird movement
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            # Constrain bird's vertical position
            bird_y = max(0, min(bird_y, SCREEN_HEIGHT - bird_height))

            # Bird rectangle for collision detection (but we only draw the image)
            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

            # Draw the current bird image based on selection
            screen.blit(current_bird_image, (bird_x, bird_y))

            # Pipe movement and creation
            pipe_timer += 1
            if pipe_timer > PIPE_CREATION_TIME:  # Add a new pipe every 'PIPE_CREATION_TIME' frames
                pipe_list.extend(create_pipe())
                pipe_timer = 0

            # Move pipes
            for pipe in pipe_list:
                pipe.x -= PIPE_SPEED

            # Remove off-screen pipes
            pipe_list = [pipe for pipe in pipe_list if pipe.x + PIPE_WIDTH > 0]

            # Draw pipes
            draw_pipes(pipe_list)

            # Check for collisions
            if check_collision(bird_rect, pipe_list):
                game_over = True

            # Update score
            for pipe in pipe_list:
                if pipe.x + PIPE_WIDTH == bird_x:
                    score += 0.5

        else:
            # Game over text
            game_over_text = font.render("Game Over! Press Space to Restart", True, WHITE)
            screen.blit(game_over_text, (20, SCREEN_HEIGHT // 2 - 20))

        # Display score
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def main():
    clock = pygame.time.Clock()
    while True:
        # sets the coordinates of flappy bird 
        horizontal = int(SCREEN_WIDTH/5) 
        vertical = int((SCREEN_HEIGHT - bird_height)/2) 
        
        # for selevel 
        ground = 0
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game 
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    pygame.quit() 
                    
                    # Exit the program 
                    sys.exit() 

                # If the user presses space or up key, 
                # start the game for them 
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP): 
                    flappygame() 
                
                # if user doesn't press anykey Nothing happen 
                else: 
                    screen.blit(background_image, (0, 0)) 
                    screen.blit(current_bird_image, (horizontal, vertical)) 
                    
                    # Just Refresh the screen 
                    pygame.display.update() 	 
                    
                    # set the rate of frame per second 
                    clock.tick(FPS)

if __name__ == "__main__":
    main()
