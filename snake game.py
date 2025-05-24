import pygame
import random

pygame.init()
width, height = 640, 480
border_thickness = 10 
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Eating Apple Game')

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
yellow = (255, 255, 102)
dark_green = (0, 100, 0)

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 12

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

def score_display(score):
    value = score_font.render("Score: " + str(score), True, black)
    win.blit(value, [border_thickness, border_thickness])

def draw_snake(snake_block, snake_list, x_change, y_change):
    for i, x in enumerate(snake_list):
        pygame.draw.rect(win, dark_green, [x[0], x[1], snake_block, snake_block])
        if i == len(snake_list) - 1:
            draw_snake_eye(x[0], x[1], snake_block, x_change, y_change)

def draw_snake_eye(x, y, block_size, x_change, y_change):
    eye_radius = block_size // 6
    pupil_radius = eye_radius // 2

    if x_change > 0:  # Moving right
        eye_center = (x + block_size * 3 // 4, y + block_size // 3)
    elif x_change < 0:  # Moving left
        eye_center = (x + block_size // 4, y + block_size // 3)
    elif y_change > 0:  # Moving down
        eye_center = (x + block_size // 3, y + block_size * 3 // 4)
    elif y_change < 0:  # Moving up
        eye_center = (x + block_size // 3, y + block_size // 4)
    else:
        eye_center = (x + block_size * 3 // 4, y + block_size // 3)

    pygame.draw.circle(win, white, eye_center, eye_radius)
    pygame.draw.circle(win, black, eye_center, pupil_radius)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [width / 6, height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x = width // 2
    y = height // 2

    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    def get_random_apple_pos():
        return (
            round(random.randrange(border_thickness, width - border_thickness - snake_block) / snake_block) * snake_block,
            round(random.randrange(border_thickness, height - border_thickness - snake_block) / snake_block) * snake_block
        )

    apple_x, apple_y = get_random_apple_pos()

    while not game_over:

        while game_close:
            win.fill(yellow)
            pygame.draw.rect(win, black, pygame.Rect(0, 0, width, height), border_thickness)
            message("Game Over! Press Q-Quit or C-Play Again", red)
            score_display(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        if (x >= width - border_thickness or x < border_thickness or
            y >= height - border_thickness or y < border_thickness):
            game_close = True

        x += x_change
        y += y_change

        win.fill(yellow)
        pygame.draw.rect(win, black, pygame.Rect(0, 0, width, height), border_thickness)

        pygame.draw.circle(win, red, (apple_x + snake_block // 2, apple_y + snake_block // 2), snake_block // 2)

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list, x_change, y_change)
        score_display(length_of_snake - 1)

        pygame.display.update()

        if x == apple_x and y == apple_y:
            apple_x, apple_y = get_random_apple_pos()
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
