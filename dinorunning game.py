import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

WHITE = (255, 255, 255)
GROUND_COLOR = (83, 83, 83)
DINO_COLOR_1 = (120, 128, 0)
DINO_COLOR_2 = (100, 110, 0)
CACTUS_COLOR_1 = (34, 139, 34)
CACTUS_COLOR_2 = (0, 100, 0)

ground_y = 360

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Dino properties
dino_x = 80
dino_y = 300
dino_width = 40
dino_height = 60

gravity = 0
jumps_done = 0
max_jumps = 2
cactus_speed = 6

game_active = True
score = 0

# Animation frames counters
dino_frame = 0
dino_frame_rate = 5  # frames per update
dino_animation_counter = 0

cactus_frame = 0
cactus_frame_rate = 10
cactus_animation_counter = 0

def create_cactus(x_pos):
    height = random.choice([40, 60, 80, 100, 120])
    return pygame.Rect(x_pos, ground_y - height, 20, height)

cactuses = [
    create_cactus(WIDTH + 200),
    create_cactus(WIDTH + 600),
    create_cactus(WIDTH + 1000),
]

def reset_game():
    global gravity, jumps_done, game_active, score, cactuses, dino_y
    dino_y = 300
    gravity = 0
    jumps_done = 0
    score = 0
    game_active = True
    cactuses.clear()
    cactuses.extend([
        create_cactus(WIDTH + 200),
        create_cactus(WIDTH + 600),
        create_cactus(WIDTH + 1000),
    ])

def draw_dino(x, y, frame):
    # Simulate running animation by alternating rectangle colors and "leg" movement
    color = DINO_COLOR_1 if frame == 0 else DINO_COLOR_2
    pygame.draw.rect(screen, color, (x, y, dino_width, dino_height))
    
    # Draw legs moving animation
    leg_offset = 5 if frame == 0 else 0
    pygame.draw.rect(screen, (0, 0, 0), (x + 10, y + dino_height, 10, 15 - leg_offset))
    pygame.draw.rect(screen, (0, 0, 0), (x + 20, y + dino_height, 10, 10 + leg_offset))

def draw_cactus(cactus_rect, frame):
    # Alternate color for subtle animation
    color = CACTUS_COLOR_1 if frame == 0 else CACTUS_COLOR_2
    pygame.draw.rect(screen, color, cactus_rect)
    # Add "spikes" with small triangles for visual interest
    spike_height = 10
    spike_width = 6
    left = cactus_rect.left
    top = cactus_rect.top
    for i in range(3):
        # Draw spikes alternating sides
        if i % 2 == frame:
            points = [
                (left, top + i * 20),
                (left - spike_width, top + i * 20 + spike_height // 2),
                (left, top + i * 20 + spike_height),
            ]
            pygame.draw.polygon(screen, (0, 150, 0), points)

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if game_active:
                if event.key == pygame.K_SPACE and jumps_done < max_jumps:
                    gravity = -12
                    jumps_done += 1
            else:
                if event.key == pygame.K_SPACE:
                    reset_game()

    if game_active:
        gravity += 0.6
        dino_y += gravity

        if dino_y >= 300:
            dino_y = 300
            jumps_done = 0

        # Update cactus positions
        for cactus in cactuses:
            cactus.x -= cactus_speed

        # Remove off-screen cactuses and add new ones
        if cactuses and cactuses[0].right < 0:
            cactuses.pop(0)
            last_x = cactuses[-1].x if cactuses else WIDTH
            new_x = last_x + random.randint(300, 600)
            cactuses.append(create_cactus(new_x))
            score += 1

        # Collision check
        dino_rect = pygame.Rect(dino_x, int(dino_y), dino_width, dino_height)
        for cactus in cactuses:
            if dino_rect.colliderect(cactus):
                game_active = False
                break

        # Draw ground
        pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, WIDTH, 40))

        # Animate dino
        dino_animation_counter += 1
        if dino_animation_counter >= dino_frame_rate:
            dino_animation_counter = 0
            dino_frame = (dino_frame + 1) % 2

        draw_dino(dino_x, int(dino_y), dino_frame)

        # Animate cactus
        cactus_animation_counter += 1
        if cactus_animation_counter >= cactus_frame_rate:
            cactus_animation_counter = 0
            cactus_frame = (cactus_frame + 1) % 2

        for cactus in cactuses:
            draw_cactus(cactus, cactus_frame)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))
    else:
        msg = font.render("Game Over! Press SPACE to Restart", True, (200, 0, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(60)
