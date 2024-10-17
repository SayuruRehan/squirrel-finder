import pygame
import random
import sys
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Squirrel Finder")
BACKGROUND_COLOR = (15, 15, 15)  # Dark background

# Load images and resize to 40x40 pixels
duck_image = pygame.image.load('duck.png').convert_alpha()
duck_image = pygame.transform.scale(duck_image, (40, 40))
strawberry_image = pygame.image.load('strawberry.png').convert_alpha()
strawberry_image = pygame.transform.scale(strawberry_image, (40, 40))
squirrel_image = pygame.image.load('squirrel.png').convert_alpha()
squirrel_image = pygame.transform.scale(squirrel_image, (40, 40))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = duck_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 10  # Move quickly

    def update(self, keys_pressed):
        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN]:
            self.rect.y += self.speed

        # Keep the player on the screen
        self.rect.clamp_ip(screen.get_rect())

class BouncingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x, self.speed_y = speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

def display_instructions():
    font = pygame.font.SysFont('Arial', 30)
    instructions = [
        "Squirrel Finder",
        "You are the duck. Use arrow keys to move.",
        "Avoid the strawberries!",
        "Find the squirrel to win!",
        "Press any key to start."
    ]
    screen.fill(BACKGROUND_COLOR)
    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + i * 40))
        screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                waiting = False

def main():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    game_over = False

    # Create player
    player_group = pygame.sprite.Group()
    player = Player()
    player_group.add(player)

    # Create sprite groups
    strawberry_group = pygame.sprite.Group()
    squirrel_group = pygame.sprite.Group()

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)

        # Spawn strawberries every second
        current_time = pygame.time.get_ticks()
        if (current_time - start_time) // 1000 > 0 and (current_time // 1000) % 2 == 0:
            if random.randint(0, 20) < 2:  # Reduced spawn rate
                x = random.randint(0, SCREEN_WIDTH - 40)
                y = random.randint(0, SCREEN_HEIGHT - 40)
                speed = random.choice([-3, 3]), random.choice([-3, 3])  # Reduced speed
                strawberry = BouncingSprite(strawberry_image, (x, y), speed)
                strawberry_group.add(strawberry)

        # Spawn squirrel after 3 seconds
        if (current_time - start_time) >= 3000 and not squirrel_group:
            x = random.randint(0, SCREEN_WIDTH - 40)
            y = random.randint(0, SCREEN_HEIGHT - 40)
            speed = random.choice([-3, 3]), random.choice([-3, 3])  # Reduced speed
            squirrel = BouncingSprite(squirrel_image, (x, y), speed)
            squirrel_group.add(squirrel)

        # Update sprites
        strawberry_group.update()
        squirrel_group.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(player, strawberry_group):
            game_over = True
            result_text = "You Died!"
        if pygame.sprite.spritecollideany(player, squirrel_group):
            game_over = True
            result_text = "You Win!"

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        player_group.draw(screen)
        strawberry_group.draw(screen)
        squirrel_group.draw(screen)

        # Display "Squirrel Finder"
        font = pygame.font.SysFont('Arial', 20)
        title_text = font.render("Squirrel Finder by SRRider", True, (255, 255, 255))
        screen.blit(title_text, (10, 10))

        # Display timer in corner
        elapsed_time = (current_time - start_time) // 1000
        timer_text = font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()

        if game_over:
            font = pygame.font.SysFont('Arial', 50)
            result_display = font.render(result_text, True, (255, 0, 0))
            result_rect = result_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(result_display, result_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            break

        clock.tick(60)

def main_loop():
    while True:
        display_instructions()
        main()

if __name__ == "__main__":
    main_loop()
