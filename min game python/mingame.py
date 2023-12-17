import pygame
import sys
import math
from PIL import Image
import io

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
FPS = 60
SQUARE_SIZE = 50
ENEMY_SIZE = 50
SQUARE_SPEED = 5
PROJECTILE_SPEED = 7
BACKGROUND_COLOR = (0, 33, 71)  # Color #002147
WHITE = (255, 255, 255)
PROJECTILE_SIZE = 30  # Adjust projectile size

# Paths to files
PROJECTILE_PATH = "C:\\Users\\jetla\\Documents\\min game python\\FB000.gif"
MUSIC_PATH = "C:\\Users\\jetla\\Documents\\min game python\\Purple Planet Music - Predator (1_30) 122bpm.mp3"
GUN_SOUND_PATH = "C:\\Users\\jetla\\Documents\\min game python\\gun-shot-6178.mp3"
ENEMY_IMAGE_PATH = "C:\\Users\\jetla\\Documents\\min game python\\Slime Trans.gif"

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Square Shooter")

# Load player image
player_image = pygame.image.load("C:\\Users\\jetla\\Documents\\min game python\\guy.png")
player_image = pygame.transform.scale(player_image, (SQUARE_SIZE, SQUARE_SIZE))

# Load enemy image
enemy_image = pygame.image.load(ENEMY_IMAGE_PATH)
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

# Initialize player properties
player_x = WINDOW_WIDTH // 2 - SQUARE_SIZE // 2
player_y = WINDOW_HEIGHT // 2 - SQUARE_SIZE // 2
player_speed = SQUARE_SPEED
player_hitpoints = 5

# Initialize enemy properties
enemy_x = 100
enemy_y = 100
enemy_speed = 2
enemy_hitpoints = 2

projectiles = []

clock = pygame.time.Clock()

# Load projectile frames from GIF
gif = Image.open(PROJECTILE_PATH)
frames = []

try:
    while True:
        gif.seek(gif.tell() + 1)
        frame = gif.copy()
        frame_bytes = io.BytesIO()
        frame.save(frame_bytes, format='PNG')
        frame_bytes.seek(0)
        frames.append(pygame.image.load(frame_bytes))
except EOFError:
    pass

projectile_frame_index = 0

# Initialize Pygame mixer and load sounds
pygame.mixer.init()
background_music = pygame.mixer.Sound(MUSIC_PATH)
gun_sound = pygame.mixer.Sound(GUN_SOUND_PATH)

# Function to calculate projectile position based on square's angle
def create_projectile(x, y, angle):
    dx = PROJECTILE_SPEED * math.cos(math.radians(angle))
    dy = -PROJECTILE_SPEED * math.sin(math.radians(angle))
    return {
        'x': x + SQUARE_SIZE // 2 - PROJECTILE_SIZE // 2,
        'y': y + SQUARE_SIZE // 2 - PROJECTILE_SIZE // 2,
        'dx': dx,
        'dy': dy
    }

# Function to check collision between two rectangles
def check_collision(rect1, rect2):
    return (rect1[0] < rect2[0] + rect2[2] and rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and rect1[1] + rect1[3] > rect2[1])

# Game loop
running = True
while running:
    window.fill(BACKGROUND_COLOR)

    # Play background music
    if not pygame.mixer.get_busy():
        background_music.play(-1)  # Loop the music indefinitely

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(player_y + SQUARE_SIZE / 2 - mouse_y, mouse_x - player_x - SQUARE_SIZE / 2))
                projectiles.append(create_projectile(player_x, player_y, angle))
                gun_sound.set_volume(0.2)  # Set volume to 20%
                gun_sound.play()

    # Handle other events and game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed

    # Ensure the player stays within the window boundaries
    player_x = max(0, min(player_x, WINDOW_WIDTH - SQUARE_SIZE))
    player_y = max(0, min(player_y, WINDOW_HEIGHT - SQUARE_SIZE))

    # Update player hitbox position and size
    player_hitbox = pygame.Rect(player_x, player_y, SQUARE_SIZE, SQUARE_SIZE)

    # Draw player image
    window.blit(player_image, (player_x, player_y))

    # Draw enemy image
    window.blit(enemy_image, (enemy_x, enemy_y))

    # Update enemy's movement (for demo purposes, moves toward the player)
    # ... (Enemy movement logic remains the same)

    # Update and draw projectiles
    projectiles_to_remove = []
    for projectile in projectiles:
        projectile['x'] += projectile['dx']
        projectile['y'] += projectile['dy']

        # Check if projectile is off-screen, mark it for removal if so
        if (projectile['x'] < 0 or projectile['x'] > WINDOW_WIDTH or
                projectile['y'] < 0 or projectile['y'] > WINDOW_HEIGHT):
            projectiles_to_remove.append(projectile)
        else:
            window.blit(frames[projectile_frame_index], (projectile['x'], projectile['y']))
            projectile_frame_index = (projectile_frame_index + 1) % len(frames)

    # Remove off-screen projectiles
    for projectile in projectiles_to_remove:
        projectiles.remove(projectile)

    # Check if either the player or enemy is defeated
    if player_hitpoints <= 0 or enemy_hitpoints <= 0:
        running = False  # End the game

    pygame.display.flip()
    clock.tick(FPS)

# Game over logic
window.fill(BACKGROUND_COLOR)  # Clear the window
if player_hitpoints <= 0:
    print("Player defeated!")
elif enemy_hitpoints <= 0:
    print("Enemy defeated!")

pygame.display.flip()  # Show game over message
pygame.time.delay(2000)  # Pause for 2 seconds before quitting
pygame.quit()
sys.exit()
