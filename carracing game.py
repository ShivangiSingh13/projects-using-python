import pygame
import random

pygame.init()

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing with Interactive Cars")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)

player_width = 50
player_height = 90
player_speed = 7

enemy_width = 50
enemy_height = 90
enemy_speed = 7

num_enemies = 5

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

line_width = 10
line_height = 50
line_color = WHITE
line_gap = 40
line_speed = enemy_speed

def draw_road_lines(offset):
    center_x = screen_width // 2 - line_width // 2
    for y in range(-line_height, screen_height, line_height + line_gap):
        pygame.draw.rect(screen, line_color, (center_x, y + offset, line_width, line_height))

def show_score(x, y, score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (x, y))

def draw_arrow(surface, color, start_pos, direction, size=30):
    x, y = start_pos
    if direction == 'left':
        points = [(x, y), (x + size, y - size // 2), (x + size, y + size // 2)]
    else:
        points = [(x, y), (x - size, y - size // 2), (x - size, y + size // 2)]
    pygame.draw.polygon(surface, color, points)

def player_car(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=12)
    pygame.draw.rect(screen, (100, 150, 255), (x + 10, y + 20, player_width - 20, 25), border_radius=6)
    pygame.draw.rect(screen, YELLOW, (x + 5, y + 5, 10, 6))

def enemy_car(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height), border_radius=12)
    pygame.draw.rect(screen, (255, 100, 100), (x + 10, y + 20, enemy_width - 20, 25), border_radius=6)
    pygame.draw.rect(screen, WHITE, (x + enemy_width - 15, y + 5, 10, 6))

def is_collision(px, py, ex, ey):
    return (px < ex + enemy_width and
            px + player_width > ex and
            py < ey + enemy_height and
            py + player_height > ey)

def game_over_screen(score):
    screen.fill(GRAY)
    over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2,
                            screen_height // 3 - over_text.get_height() // 2))
    
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2,
                             screen_height // 3 + 50))
    
    restart_text = font.render("Press R to Restart or Q to Quit", True, YELLOW)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2,
                               screen_height // 3 + 100))
    pygame.display.update()

def game_loop():
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 20
    score = 0

    enemies = []
    enemy_x_changes = []

    for _ in range(num_enemies):
        x = random.randint(0, screen_width - enemy_width)
        y = random.randint(-1500, -enemy_height)
        enemies.append([x, y])
        enemy_x_changes.append(random.choice([-3, -2, -1, 1, 2, 3]))

    player_x_change = 0
    player_y_change = 0
    road_line_offset = 0
    clock = pygame.time.Clock()

    running = True
    game_over = False

    while running:
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_x_change = -player_speed
                    if event.key == pygame.K_RIGHT:
                        player_x_change = player_speed
                    if event.key == pygame.K_UP:
                        player_y_change = -player_speed
                    if event.key == pygame.K_DOWN:
                        player_y_change = player_speed

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_x_change = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_y_change = 0
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        return False

        if not game_over:
            road_line_offset += line_speed
            if road_line_offset > line_height + line_gap:
                road_line_offset = 0
            draw_road_lines(road_line_offset)

            player_x += player_x_change
            player_y += player_y_change

            if player_x < 0:
                player_x = 0
            if player_x > screen_width - player_width:
                player_x = screen_width - player_width

            if player_y < 0:
                player_y = 0
            if player_y > screen_height - player_height:
                player_y = screen_height - player_height

            for i, enemy in enumerate(enemies):
                enemy[1] += enemy_speed
                enemy[0] += enemy_x_changes[i]

                if enemy[0] <= 0:
                    enemy[0] = 0
                    enemy_x_changes[i] = -enemy_x_changes[i]
                elif enemy[0] >= screen_width - enemy_width:
                    enemy[0] = screen_width - enemy_width
                    enemy_x_changes[i] = -enemy_x_changes[i]

                if enemy[1] > screen_height:
                    enemy[1] = random.randint(-1500, -enemy_height)
                    enemy[0] = random.randint(0, screen_width - enemy_width)
                    enemy_x_changes[i] = random.choice([-3, -2, -1, 1, 2, 3])
                    score += 1

                enemy_car(enemy[0], enemy[1])

                if is_collision(player_x, player_y, enemy[0], enemy[1]):
                    game_over = True

            player_car(player_x, player_y)

            draw_arrow(screen, WHITE, (50, screen_height - 50), 'left')
            draw_arrow(screen, WHITE, (screen_width - 50, screen_height - 50), 'right')
            show_score(10, 10, score)
        else:
            game_over_screen(score)

        pygame.display.update()
        clock.tick(60)

def main():
    while True:
        restart = game_loop()
        if not restart:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
