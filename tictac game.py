import pygame
import sys

pygame.init()

screen_size = 400
grid_size = 300
margin = (screen_size - grid_size) // 2
cell_size = grid_size // 3
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Tic Tac Toe: 2 Player')

bg_color = (240, 240, 240)
line_color = (0, 0, 0)
x_color = (220, 20, 60)
o_color = (65, 105, 225)
text_color = (20, 20, 20)

font = pygame.font.SysFont(None, 80)
menu_font = pygame.font.SysFont(None, 28)

board = [["" for _ in range(3)] for _ in range(3)]

def draw_board():
    screen.fill(bg_color)
    for i in range(1, 3):
        pygame.draw.line(screen, line_color, 
                         (margin + i * cell_size, margin), 
                         (margin + i * cell_size, margin + grid_size), 4)
        pygame.draw.line(screen, line_color, 
                         (margin, margin + i * cell_size), 
                         (margin + grid_size, margin + i * cell_size), 4)

    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol:
                color = x_color if symbol == "X" else o_color
                text = font.render(symbol, True, color)
                x = margin + col * cell_size + (cell_size - text.get_width()) // 2
                y = margin + row * cell_size + (cell_size - text.get_height()) // 2
                screen.blit(text, (x, y))

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

def reset_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]

def draw_end_menu(message):
    screen.fill(bg_color)
    text = font.render(message, True, text_color)
    screen.blit(text, (screen_size // 2 - text.get_width() // 2, 100))

    instructions = menu_font.render("Press R to Play Again or Q to Quit", True, text_color)
    screen.blit(instructions, (screen_size // 2 - instructions.get_width() // 2, 180))

player_turn = "X"
game_over = False
winner = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    player_turn = "X"
                    game_over = False
                    winner = None
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if margin <= x <= margin + grid_size and margin <= y <= margin + grid_size:
                    col = (x - margin) // cell_size
                    row = (y - margin) // cell_size

                    if board[row][col] == "":
                        board[row][col] = player_turn
                        player_turn = "O" if player_turn == "X" else "X"

    if not game_over:
        winner = check_winner()
        if winner:
            game_over = True
        elif is_draw():
            game_over = True

    if game_over:
        if winner:
            draw_end_menu(f"{winner} Wins!")
        else:
            draw_end_menu("It's a Draw!")
    else:
        draw_board()

    pygame.display.update()