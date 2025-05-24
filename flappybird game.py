import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 520, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

BACKGROUND_COLOR = (135, 206, 235)
PIPE_COLOR = (70, 130, 180)
BIRD_COLOR = (255, 127, 37)
EYE_COLOR = (0, 0, 0)
BEAK_COLOR = (255, 200, 50)
TEXT_COLOR = (30, 144, 255)

gravity = 0.5
bird_movement = 0
bird_x = 50
bird_y = HEIGHT // 2
bird_width = 34
bird_height = 24

pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipe_frequency = 1500
pipes = []

score = 0
game_active = True

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

def draw_bird(x, y, movement):
    angle = max(min(-movement * 3, 25), -25) 
    bird_surface = pygame.Surface((bird_width * 2, bird_height * 2), pygame.SRCALPHA)
    bird_rect = bird_surface.get_rect(center=(bird_width, bird_height))
    pygame.draw.ellipse(bird_surface, BIRD_COLOR, (bird_width // 2, bird_height // 2, bird_width, bird_height))
    wing_points = [
        (bird_width + 5, bird_height),
        (bird_width + 25, bird_height - 10),
        (bird_width + 15, bird_height + 10)
    ]
    pygame.draw.polygon(bird_surface, BIRD_COLOR, wing_points)

    pygame.draw.circle(bird_surface, EYE_COLOR, (bird_width + 10, bird_height), 4)

    beak_points = [
        (bird_width + bird_width - 5, bird_height + 5),
        (bird_width + bird_width + 5, bird_height + 2),
        (bird_width + bird_width + 5, bird_height + 10)
    ]
    pygame.draw.polygon(bird_surface, BEAK_COLOR, beak_points)

    rotated_bird = pygame.transform.rotate(bird_surface, angle)
    new_rect = rotated_bird.get_rect(center=(x + bird_width // 2, y + bird_height // 2))

    screen.blit(rotated_bird, new_rect.topleft)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, pipe['top'])
        pygame.draw.rect(screen, PIPE_COLOR, pipe['bottom'])

def move_pipes():
    for pipe in pipes:
        pipe['top'].x -= pipe_speed
        pipe['bottom'].x -= pipe_speed
    pipes[:] = [pipe for pipe in pipes if pipe['top'].right > 0]

def check_collision(bird_rect):
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return False
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            return False
    return True

def display_score():
    score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_surface, (10, 10))

def display_game_over():
    go_surface = font.render("Game Over! Press SPACE to Restart", True, TEXT_COLOR)
    screen.blit(go_surface, (20, HEIGHT // 2 - 20))

def display_quit_instruction():
    quit_surface = small_font.render("Press Q to Quit", True, TEXT_COLOR)
    screen.blit(quit_surface, (WIDTH - 120, HEIGHT - 30))

bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if game_active:
                if event.key == pygame.K_SPACE:
                    bird_movement = -10
            else:
                if event.key == pygame.K_SPACE:
                    bird_rect.y = HEIGHT // 2
                    bird_movement = 0
                    pipes.clear()
                    score = 0
                    game_active = True

        if game_active and event.type == SPAWNPIPE:
            pipe_height = random.randint(100, HEIGHT - 200)
            top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
            bottom_pipe = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - (pipe_height + pipe_gap))
            pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'scored': False})

    if game_active:
        screen.fill(BACKGROUND_COLOR)
        bird_movement += gravity
        bird_rect.y += int(bird_movement)
        
        draw_bird(bird_rect.x, bird_rect.y, bird_movement)

        move_pipes()
        draw_pipes()
        game_active = check_collision(bird_rect)

        for pipe in pipes:
            if not pipe['scored'] and pipe['top'].right < bird_rect.left:
                pipe['scored'] = True
                score += 1

        display_score()
        display_quit_instruction()
    else:
        screen.fill(BACKGROUND_COLOR)
        display_game_over()
        display_quit_instruction()

    pygame.display.update()
    clock.tick(60)
