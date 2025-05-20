#This is a breakout game
#The player has to destroy the bricks by hitting them with the ball
#The player has 3 lives
#The player can move the paddle using the left and right arrow keys
#The player can launch the ball using the space bar
#Initialise the game
import pygame
pygame.init()
import sys
import random
import time
import math  # Import math for trigonometric calculations
# Ensure pygame is installed
# You can install pygame using the following command:

#Game Settings
WIDTH, HEIGHT = 700, 700
FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Create the game window
screen= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

#Clock to control the frame rate
clock = pygame.time.Clock()

#Player Settings
player_width = 50
player_height = 50
player_speed = 5

# Bullet Settings
bullet_width = 5.5  # Reduced bullet width by 5
bullet_width = bullet_width / 2  # Reduce bullet width by 50%
bullet_width = bullet_width * 2  # Increase bullet width by 1.5x
bullet_height = 20
bullet_speed = 15  # Increased bullet speed
bullet = []

# Bullet cooldown timer
bullet_cooldown_timer = 0
bullet_cooldown_interval = 100  # 0.2 seconds in milliseconds

# Alien Settings
alien_width = 50
alien_height = 50
alien_speed = 2  # Increased alien speed
aliens = []

# Alien movement direction
alien_direction_x = 1  # 1 for right, -1 for left
# Removed alien_direction_y

# Adjust alien movement boundaries to be 20 units below the "SCORE" text
score_text_height = 35  # Height of the "SCORE" text
alien_min_y = score_text_height + 20  # 20 units below the text
alien_max_y = HEIGHT - 250  # Keep the original max boundary

# Alien generation timer
alien_spawn_timer = 0
alien_spawn_interval = 1000  # Reduced time to 1 second between new rows of aliens
player = pygame.Rect(WIDTH/2 - player_width/2, HEIGHT - player_height - 10, player_width, player_height)  # Shifted 10 units up

# Load sprites
player_sprite = pygame.image.load("player.png")  # Replace with the path to your player sprite
alien_sprite = pygame.image.load("alien.png")    # Replace with the path to your alien sprite

# Load sprites for additional aliens
alien1_sprite = pygame.image.load("alien1.png")  # Replace with the path to your alien1 sprite
alien2_sprite = pygame.image.load("alien2.png")  # Replace with the path to your alien2 sprite

# Scale sprites to match object dimensions
player_sprite = pygame.transform.scale(player_sprite, (player_width, player_height))
alien_sprite = pygame.transform.scale(alien_sprite, (alien_width, alien_height))

# Scale sprites to match alien dimensions
alien1_sprite = pygame.transform.scale(alien1_sprite, (alien_width, alien_height))
alien2_sprite = pygame.transform.scale(alien2_sprite, (alien_width, alien_height))

# Load and scale the background image once
bg = pygame.image.load("bg.png")  # Replace with the path to your background image
bg_width, bg_height = bg.get_size()
aspect_ratio = bg_height / bg_width
bg = pygame.transform.scale(bg, (WIDTH, int(WIDTH * aspect_ratio)))  # Scale width to fit screen, adjust height proportionally

# Update the number of tiles needed to cover the height of the window
bg_height = bg.get_height()
tiles = math.ceil(HEIGHT / bg_height) + 1

scroll = 0  # Initialize scroll position

# Load and scale the title screen background image
bg1 = pygame.image.load("bg1.jpg")  # Replace with the path to your title screen background image
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))  # Scale to fit the screen dimensions

import itertools

# Alien bullet settings
alien_bullet_width = 5
alien_bullet_height = 20
alien_bullet_speed = 5
alien_bullets = []

# Alien bullet cooldown interval and timer for interval reduction
alien_bullet_cooldown_interval = 1500  # 1.5 seconds in milliseconds
alien_bullet_min_interval = 500  # Minimum interval of 500 milliseconds
interval_reduction_timer = 0
interval_reduction_interval = 60000  # 1 minute in milliseconds

# Alien bullet cooldown timer
alien_bullet_cooldown_timer = 0  # Initialize the cooldown timer

# Initialize score
score = 0

# Player lives settings
player_lives = 3
life_width = 40  # 25% size of player
life_height = 40
lives_display = [pygame.Rect(WIDTH - (i + 1) * (life_width + 10), 10, life_width, life_height) for i in range(player_lives)]

# Load sprite for lives
life_sprite = pygame.image.load("life.png")  # Replace with the path to your life sprite
life_sprite = pygame.transform.scale(life_sprite, (life_width, life_height))  # Scale sprite to match life dimensions

# Counter to track the number of times create_aliens is called
alien_creation_counter = 0

# Power-up settings
power_up_width = 40
power_up_height = 40
power_up_speed = 3
power_up_active = False
power_up_timer = 0
power_up_duration = 5000  # Power-up lasts for 5 seconds
power_up = None  # Initialize power-up as None

# Load sprite for power-up
power_up_sprite = pygame.image.load("power_up.png")  # Replace with the path to your power-up sprite
power_up_sprite = pygame.transform.scale(power_up_sprite, (power_up_width, power_up_height))  # Scale sprite to match power-up dimensions

# Life power-up settings
life_power_up_width = 40
life_power_up_height = 40
life_power_up_speed = 3
life_power_up = None  # Initialize life power-up as None
life_power_up_timer = 0  # Timer to track frames for life power-up
life_power_up_interval = random.randint(1000, 2000)  # Random interval between 1000 and 2000 frames

# Load sprite for life power-up
life_power_up_sprite = pygame.image.load("life.png")  # Replace with the path to your life power-up sprite
life_power_up_sprite = pygame.transform.scale(life_power_up_sprite, (life_power_up_width, life_power_up_height))

# Initialize waves variable
waves = random.randint(3, 8)

def create_aliens():
    """
    Create a 4-row system of aliens aligned properly with reduced columns.
    Start replacing 11 random aliens with alien1 after 2 loops and alien2 after 4 loops.
    """
    global alien_creation_counter
    aliens.clear()  # Clear existing aliens
    for row in range(4):  # Reduced rows from 5 to 4
        for col in range(1, (WIDTH // (alien_width + 10)) - 1):  # Reduced columns by 1 on each side
            alien_rect = pygame.Rect(col * (alien_width + 10), row * (alien_height + 25) + alien_min_y + 10, alien_width, alien_height)
            aliens.append({"rect": alien_rect, "type": "alien", "hits": 0})  # Store the Rect, type, and hit counter in a dictionary
    
    alien_creation_counter += 1  # Increment the counter

    if alien_creation_counter >= 3:  # After 2 loops, start replacing aliens with alien1
        alien1_indices = random.sample([i for i, alien in enumerate(aliens) if alien["type"] == "alien"], 11)
        for index in alien1_indices:
            aliens[index]["type"] = "alien1"  # Update the type to alien1

    if alien_creation_counter >= 5:  # After 4 loops, start replacing aliens with alien2
        alien2_indices = random.sample([i for i, alien in enumerate(aliens) if alien["type"] == "alien"], 11)
        for index in alien2_indices:
            aliens[index]["type"] = "alien2"  # Update the type to alien2

    if alien_creation_counter >= 6:  # After 2 loops, start replacing aliens with alien1
        alien1_indices = random.sample([i for i, alien in enumerate(aliens) if alien["type"] == "alien"], 11)
        for index in alien1_indices:
            aliens[index]["type"] = "alien1"  # Update the type to alien1

    if alien_creation_counter >= 7:  # After 4 loops, start replacing aliens with alien2
        alien2_indices = random.sample([i for i, alien in enumerate(aliens) if alien["type"] == "alien"], 11)
        for index in alien2_indices:
            aliens[index]["type"] = "alien2"  # Update the type to alien2

create_aliens()

def reset_game():
    """
    Resets the game state to its initial configuration.
    """
    global aliens, bullet, alien_bullets, alien_bullet_cooldown_timer, alien_bullet_cooldown_interval, interval_reduction_timer, score, player_lives, lives_display, alien_creation_counter, waves, first_round
    aliens = []
    bullet = []
    alien_bullets = []
    alien_bullet_cooldown_timer = 0
    alien_bullet_cooldown_interval = 1500  # Reset to initial interval
    interval_reduction_timer = 0
    score = 0  # Reset score
    player_lives = 3  # Reset lives
    alien_creation_counter = 0  # Reset alien creation loop count
    waves = random.randint(3, 8)  # Reset waves to a random value
    lives_display = [pygame.Rect(WIDTH - (i + 1) * (life_width + 10), 10, life_width, life_height) for i in range(player_lives)]
    create_aliens()
    player.x = WIDTH / 2 - player_width / 2  # Reset player position
    first_round = False  # Reset the first round flag

def game_over():
    """
    Displays a "GAME OVER" message with Restart and Exit buttons, and the final score.
    """
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    credits_font = pygame.font.Font(None, 30)  # Font for credits text
    text = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Score: {score}", True, WHITE)  # Display final score
    restart_text = small_font.render("Restart", True, WHITE)
    exit_text = small_font.render("Exit", True, WHITE)
    credits_text = credits_font.render("Credits: @lasya65 and @Nox-Invicte (Github)", True, WHITE)

    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120 + 10, 200, 50)  # Add 10 units of spacing below Restart button

    while True:
        screen.fill(BLACK)
        # Shift "GAME OVER" text up by 25 units
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 25))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))  # Display score below "GAME OVER"
        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, exit_button)
        # Center-align the "Restart" and "Exit" text within their respective buttons
        screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2, 
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, 
                                exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        # Display credits text at the bottom center
        screen.blit(credits_text, (WIDTH // 2 - credits_text.get_width() // 2, HEIGHT - credits_text.get_height() - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_game()
                    return  # Exit the game_over loop and restart the game
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def show_start_screen():
    """
    Displays a start screen with a "Play" button to begin the game.
    """
    global alien_creation_counter  # Ensure the counter is reset
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    title_text = font.render("SPACE INVADERS", True, WHITE)
    play_text = small_font.render("Play", True, WHITE)

    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

    while True:
        # Draw the title screen background
        screen.blit(bg1, (0, 0))

        # Display title text
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        # Draw the play button
        pygame.draw.rect(screen, GREEN, play_button)
        # Center-align the "Play" text within the button
        screen.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) // 2, 
                                play_button.y + (play_button.height - play_text.get_height()) // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    alien_creation_counter = 0  # Reset the creation counter
                    return  # Exit the start screen and begin the game

def draw_waves(current_wave):
    """
    Draws boxes at the top center of the window to represent the number of waves.
    Displays "Wave N" above the boxes, where N is the current wave.
    """
    font = pygame.font.Font(None, 35)
    wave_text = font.render(f"Wave {current_wave}", True, WHITE)
    wave_text_x = WIDTH // 2 - wave_text.get_width() // 2
    wave_text_y = 10  # Top margin for the text
    screen.blit(wave_text, (wave_text_x, wave_text_y))

    box_width = 10
    box_height = 10
    spacing = 5
    total_width = waves * (box_width + spacing) - spacing
    start_x = WIDTH // 2 - total_width // 2
    y = wave_text_y + wave_text.get_height() + 5  # Position boxes below the text

    for i in range(waves):
        pygame.draw.rect(screen, GREEN, (start_x + i * (box_width + spacing), y, box_width, box_height))

def show_countdown(seconds):
    """
    Displays a countdown timer on the main game screen with all controls active.
    """
    font = pygame.font.Font(None, 74)
    countdown_timer = seconds * 1000  # Convert seconds to milliseconds
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < countdown_timer:
        # Calculate remaining time
        remaining_time = seconds - (pygame.time.get_ticks() - start_time) // 1000

        # Handle events and allow player controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Allow player movement during countdown
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_speed > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player_speed + player_width < WIDTH:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y - player_speed > HEIGHT - player_height - 200:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y + player_speed + player_height < HEIGHT - 10:
            player.y += player_speed

        # Draw the game screen
        screen.fill(BLACK)
        for i in range(tiles):
            screen.blit(bg, (0, i * bg_height - scroll))
        screen.blit(player_sprite, (player.x, player.y))
        draw_waves(current_wave)
        font_small = pygame.font.Font(None, 35)
        score_text = font_small.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        for life in lives_display:
            screen.blit(life_sprite, (life.x, life.y))

        # Display countdown timer
        countdown_text = font.render(f"Next Round in: {remaining_time}", True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

# Show the start screen before the game loop
show_start_screen()

#Game Loop
while True:
    first_round = True  # Flag to skip countdown for the first round
    while True:  # Infinite loop to keep running waves
        if not first_round:
            # Show a 10-second countdown before generating aliens
            show_countdown(10)
        first_round = False  # Reset the flag after the first round

        # Reset alien creation counter and clear all bullets
        alien_creation_counter = 0
        bullet.clear()
        alien_bullets.clear()

        for current_wave in range(1, waves + 1):  # Track the current wave
            create_aliens()
            while aliens:  # Wait until all aliens are cleared
                #Check for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                # Increment the bullet cooldown timer
                bullet_cooldown_timer += clock.get_time()

                # Increment the alien bullet cooldown timer
                alien_bullet_cooldown_timer += clock.get_time()

                # Increment the interval reduction timer
                interval_reduction_timer += clock.get_time()

                # Reduce the alien bullet cooldown interval every 1 minute
                if interval_reduction_timer >= interval_reduction_interval:
                    interval_reduction_timer = 0  # Reset the reduction timer
                    if alien_bullet_cooldown_interval > alien_bullet_min_interval:
                        alien_bullet_cooldown_interval = max(alien_bullet_cooldown_interval - 100, alien_bullet_min_interval)

                # Randomly spawn a power-up
                if power_up is None and random.randint(1, 750) == 1:  # 1 in 500 chance per frame
                    power_up = pygame.Rect(random.randint(1,WIDTH), 0, power_up_width, power_up_height)

                # Move the power-up downwards
                if power_up:
                    power_up.y += power_up_speed
                    if power_up.y > HEIGHT:  # Remove power-up if it goes off-screen
                        power_up = None

                # Check for collision between the player and the power-up
                if power_up and power_up.colliderect(player):
                    power_up = None  # Remove the power-up
                    power_up_active = True
                    power_up_timer = pygame.time.get_ticks()  # Start the power-up timer

                # Deactivate the power-up after its duration
                if power_up_active and pygame.time.get_ticks() - power_up_timer > power_up_duration:
                    power_up_active = False

                # Increment the life power-up timer
                life_power_up_timer += 1

                # Spawn a life power-up after the interval
                if life_power_up_timer >= life_power_up_interval:
                    life_power_up_timer = 0  # Reset the timer
                    life_power_up_interval = random.randint(1000, 2000)  # Set a new random interval
                    if life_power_up is None:  # Ensure only one life power-up exists at a time
                        life_power_up = pygame.Rect(random.randint(1, WIDTH - life_power_up_width), 0, life_power_up_width, life_power_up_height)

                # Move the life power-up downwards
                if life_power_up:
                    life_power_up.y += life_power_up_speed
                    if life_power_up.y > HEIGHT:  # Remove life power-up if it goes off-screen
                        life_power_up = None

                # Check for collision between the player and the life power-up
                if life_power_up and life_power_up.colliderect(player):
                    if player_lives < 3:  # Only replenish life if lives are below the maximum
                        player_lives += 1
                        lives_display.append(pygame.Rect(WIDTH - (player_lives) * (life_width + 10), 10, life_width, life_height))
                    life_power_up = None  # Remove the life power-up after collection

                #Check for key presses
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_LEFT] and player.x - player_speed > 0:
                    player.x -= player_speed
                if keys[pygame.K_RIGHT] and player.x + player_speed + player_width < WIDTH:
                    player.x += player_speed
                if keys[pygame.K_UP] and player.y - player_speed > HEIGHT - player_height - 200:  # Move up within range
                    player.y -= player_speed
                if keys[pygame.K_DOWN] and player.y + player_speed + player_height < HEIGHT - 10:  # Move down within range
                    player.y += player_speed
                    
                if keys[pygame.K_SPACE] and bullet_cooldown_timer >= bullet_cooldown_interval:
                    bullet_cooldown_timer = 0  # Reset the cooldown timer
                    if power_up_active:
                        # Shoot 3 bullets
                        bullet.append(pygame.Rect(player.x + player_width / 2 - bullet_width / 2, player.y, bullet_width, bullet_height))
                        bullet.append(pygame.Rect(player.x + player_width / 2 - bullet_width / 2 - 10, player.y, bullet_width, bullet_height))
                        bullet.append(pygame.Rect(player.x + player_width / 2 - bullet_width / 2 + 10, player.y, bullet_width, bullet_height))
                    else:
                        # Shoot 1 bullet
                        bullet.append(pygame.Rect(player.x + player_width / 2 - bullet_width / 2, player.y, bullet_width, bullet_height))
                    
                # Update bullet positions
                for b in bullet[:]:  # Iterate over a copy of the bullet list
                    b.y -= bullet_speed
                    if b.y < 0:  # Remove if off-screen
                        bullet.remove(b)

                # Randomly choose an alien to shoot a bullet based on the cooldown interval
                if alien_bullet_cooldown_timer >= alien_bullet_cooldown_interval and aliens:
                    alien_bullet_cooldown_timer = 0  # Reset the cooldown timer
                    shooting_alien = random.choice(aliens)["rect"]  # Choose a random alien
                    alien_bullets.append(pygame.Rect(shooting_alien.x + alien_width / 2 - alien_bullet_width / 2, 
                                                     shooting_alien.y + alien_height, 
                                                     alien_bullet_width, 
                                                     alien_bullet_height))

                # Move alien bullets
                for ab in alien_bullets[:]:  # Iterate over a copy of the alien bullets list
                    ab.y += alien_bullet_speed
                    if ab.y > HEIGHT:  # Remove bullets that go off-screen
                        alien_bullets.remove(ab)

                # Check for collisions between alien bullets and the player
                for ab in alien_bullets[:]:
                    if ab.colliderect(player):
                        alien_bullets.remove(ab)  # Remove the alien bullet
                        if player_lives > 0:
                            player_lives -= 1  # Decrease lives
                            lives_display.pop()  # Remove one life from the display
                        if player_lives == 0:  # If no lives are left, show game over
                            game_over()

                # Move aliens
                for alien in aliens:
                    alien["rect"].x += alien_direction_x * alien_speed
                    # Removed Y-axis movement

                # Check for alien boundary collisions
                if any(alien["rect"].x <= 25 or alien["rect"].x + alien_width >= WIDTH - 25 for alien in aliens):  # 25-unit margin
                    alien_direction_x *= -1  # Reverse horizontal direction
                # Removed vertical boundary checks and direction reversal

                # Regenerate aliens if all are removed
                if not aliens:
                    create_aliens()
                    # Decrease the alien bullet cooldown interval
                    if alien_bullet_cooldown_interval > alien_bullet_min_interval:
                        alien_bullet_cooldown_interval = max(alien_bullet_cooldown_interval - 50, alien_bullet_min_interval)

                for b in bullet[:]:  # Iterate over a copy of the bullet list
                    for alien in aliens[:]:  # Iterate over a copy of the aliens list
                        if b.colliderect(alien["rect"]):
                            bullet.remove(b)  # Remove bullet after collision
                            alien["hits"] += 1  # Increment the hit counter for the alien

                            # Check if the alien should be removed based on its type
                            if alien["type"] == "alien1" and alien["hits"] >= 3:  # Remove alien1 after 3 hits
                                aliens.remove(alien)
                                score += 3  # Reward 3 points for alien1
                            elif alien["type"] == "alien2" and alien["hits"] >= 5:  # Remove alien2 after 5 hits
                                aliens.remove(alien)
                                score += 5  # Reward 5 points for alien2
                            elif alien["type"] == "alien" and alien["hits"] >= 1:  # Remove regular alien after 1 hit
                                aliens.remove(alien)
                                score += 1  # Reward 1 point for regular alien
                            break  # Exit inner loop to avoid modifying the list during iteration

                for alien in aliens:
                    if alien["rect"].colliderect(player):
                        game_over()
                        
                # Scroll the background downwards
                scroll += 5  # Adjust the scroll speed as needed
                if scroll >= bg_height:  # Reset scroll when it exceeds the background height
                    scroll = 0

                # Draw the scrolling background
                for i in range(tiles):
                    screen.blit(bg, (0, i * bg_height - scroll))

                screen.blit(player_sprite, (player.x, player.y))  # Draw player sprite

                # Add "SCORE" text with the current score
                font = pygame.font.Font(None, 35)  # Set font size to 35
                score_text = font.render(f"SCORE: {score}", True, WHITE)
                screen.blit(score_text, (10, 10))  # Draw "SCORE" with the score at the top-left corner

                # Draw lives on the top-right corner
                for life in lives_display:
                    screen.blit(life_sprite, (life.x, life.y))  # Draw each life as a sprite

                for b in bullet:
                    # Draw bullets as triangles
                    pygame.draw.polygon(screen, WHITE, [
                        (b.x + bullet_width / 2, b.y),  # Top point of the triangle
                        (b.x, b.y + bullet_height),  # Bottom-left point
                        (b.x + bullet_width, b.y + bullet_height)  # Bottom-right point
                    ])
                for ab in alien_bullets:
                    pygame.draw.rect(screen, RED, ab)  # Draw alien bullets as red rectangles

                # Draw aliens with their respective sprites
                for alien in aliens:
                    if alien["type"] == "alien1":
                        screen.blit(alien1_sprite, (alien["rect"].x, alien["rect"].y))  # Draw alien1 sprite
                    elif alien["type"] == "alien2":
                        screen.blit(alien2_sprite, (alien["rect"].x, alien["rect"].y))  # Draw alien2 sprite
                    else:
                        screen.blit(alien_sprite, (alien["rect"].x, alien["rect"].y))  # Draw default alien sprite

                # Draw the power-up
                if power_up:
                    screen.blit(power_up_sprite, (power_up.x, power_up.y))  # Draw the power-up as a sprite

                # Draw the life power-up
                if life_power_up:
                    screen.blit(life_power_up_sprite, (life_power_up.x, life_power_up.y))  # Draw the life power-up as a sprite
                    
                draw_waves(current_wave)  # Pass the current wave to the draw_waves function
                pygame.display.flip()
                clock.tick(FPS)

        # Choose a new random value for waves
        waves = random.randint(3, 8)

#Update player positions

player.left = max(player.left, 0)
player.right = min(player.right, WIDTH)

#Update bullet positions
for b in bullet:  # Iterate over the bullet list
    b.y -= bullet_speed
