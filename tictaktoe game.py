import pygame
import sys
import random

pygame.init()

width, height = 300, 350
line_width = 4
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe: Player vs Random AI')

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 60)
msg_font = pygame.font.SysFont(None, 40)

board = [["" for _ in range(3)] for _ in range(3)]
player_turn = True
game_over = False
result_text = ""
wait_for_ai = False
ai_timer_start = 0
AI_DELAY = 800

def draw_board():
    screen.fill(white)
    for i in range(1, 3):
        pygame.draw.line(screen, black, (0, i * 100), (300, i * 100), line_width)
        pygame.draw.line(screen, black, (i * 100, 0), (i * 100, 300), line_width)
    for i in range(3):
        for j in range(3):
            symbol = board[i][j]
            if symbol:
                text = font.render(symbol, True, black)
                screen.blit(text, (j * 100 + 30, i * 100 + 20))

def draw_result(text):
    message = msg_font.render(text, True, black)
    screen.blit(message, (50, 310))

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def is_draw():
    return all(cell != "" for row in board for cell in row)

def ai_move():
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    if empty:
        move = random.choice(empty)
        board[move[0]][move[1]] = "O"

def reset_game():
    global board, player_turn, game_over, result_text, wait_for_ai
    board = [["" for _ in range(3)] for _ in range(3)]
    player_turn = True
    game_over = False
    result_text = ""
    wait_for_ai = False

clock = pygame.time.Clock()

while True:
    draw_board()
    if game_over:
        draw_result(result_text)
    pygame.display.update()

    if not game_over and wait_for_ai and pygame.time.get_ticks() - ai_timer_start >= AI_DELAY:
        ai_move()
        wait_for_ai = False
        player_turn = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_game()

        elif not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < 300:
                row, col = y // 100, x // 100
                if board[row][col] == "":
                    board[row][col] = "X"
                    player_turn = False
                    wait_for_ai = True
                    ai_timer_start = pygame.time.get_ticks()

    if not game_over:
        winner = check_winner()
        if winner:
            result_text = f"{winner} wins!"
            game_over = True
            wait_for_ai = False
        elif is_draw():
            result_text = "It's a Draw!"
            game_over = True
            wait_for_ai = False

    clock.tick(60)
