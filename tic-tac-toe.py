import pygame
import sys
import numpy

# Constants
HEIGHT = 1200
WIDTH = 1200
ROWS = 3
COLS = 3
SQUARE_SIZE = WIDTH // COLS

# Colors
BACKGROUND_COLOR = "blue"
LINE_COLOR = "black"
CIRCLE_COLOR = "white"
CROSS_COLOR = "red"
run = True
post_start_screen = False
winner = ""

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Kółko i krzyżyk")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Variables
board = numpy.zeros((ROWS, COLS))
current_player = 1  # Start with player 1

def draw_lines():
    screen.fill(BACKGROUND_COLOR)
    for col in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * col), (WIDTH, SQUARE_SIZE * col), 10)
    for row in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * row, 0), (SQUARE_SIZE * row, HEIGHT), 10)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, 15)
            elif board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 5, row * SQUARE_SIZE + SQUARE_SIZE // 5), (col * SQUARE_SIZE + SQUARE_SIZE * 4 // 5, row * SQUARE_SIZE + SQUARE_SIZE * 4 // 5), 15)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 5, row * SQUARE_SIZE + SQUARE_SIZE * 4 // 5), (col * SQUARE_SIZE + SQUARE_SIZE * 4 // 5, row * SQUARE_SIZE + SQUARE_SIZE // 5), 15)

def take_sign(row, col, player):
    board[row][col] = player

def is_full():
    global run
    if 0 not in board:
        run = False
        return True

def is_available(row, col):
    return board[row][col] == 0

def move(player):
    mouse_pos = pygame.mouse.get_pos()
    for j in range(COLS):
        for i in range(ROWS):
            if (mouse_pos[0] > 0 + (400 * j) and mouse_pos[0] < 400 * (j + 1) and 
                mouse_pos[1] > 0 + (400 * i) and mouse_pos[1] < 400 * (i + 1)):
                if is_available(i, j):
                    take_sign(i, j, player)
                    return True
        
def starting_screen():
    text_font = pygame.font.SysFont("Arial", 100)
    text = text_font.render("ZACZYNA: X ", 1, "red")
    text2 = text_font.render("KLIKNIJ SPACJĘ ABY ZACZĄĆ", 1, "red")
    text_rect = text.get_rect(center = (600, 200))
    text2_rect = text2.get_rect(center = (600, 400))
    pygame.draw.rect(screen, "black", (0, 0, HEIGHT, WIDTH))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)

def win_condition():
    global winner
    global run
    is_winner = False
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            winner = board[0][i]
            run = False
            is_winner = True
            convert()
            return run, winner, is_winner
        
        elif board[i][0] == board[i][1] == board[i][2] != 0:
            winner = board[i][0]
            run = False
            is_winner = True
            convert()
            return run, winner, is_winner
        
    if board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[1][1]
        run = False
        is_winner = True
        convert()
        return run, winner, is_winner
    
    elif board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[1][1]
        run = False
        is_winner = True
        convert()
        return run, winner, is_winner
    
    return False

def ending_screen():
    global winner
    if win_condition():
        text_font = pygame.font.SysFont("Arial", 100)
        text = text_font.render(f"WINNER: {winner} if you want to play ", 1, "red")
        text_rect = text.get_rect(center = (600, 200))
        pygame.draw.rect(screen, "black", (0, 0, HEIGHT, WIDTH))
        screen.blit(text, text_rect)
    else:
        text_font = pygame.font.SysFont("Arial", 100)
        text = text_font.render("REMIS!!!", 1, "red")
        text_rect = text.get_rect(center = (600, 200))
        pygame.draw.rect(screen, "black", (0, 0, HEIGHT, WIDTH))
        screen.blit(text, text_rect)

def convert():
    global winner
    if winner == 1:
        winner = "X"
    elif winner == 2:
        winner = "O"
    return winner

def again():
    pass

starting_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                post_start_screen = True
        if post_start_screen:        
            if run:    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if move(current_player):
                        if current_player == 1:
                            current_player = 2 
                        else: 
                            current_player = 1
                draw_lines()
                draw_figures()
                win_condition()
                if win_condition():
                    again()
            else:
                convert()
                ending_screen()
    is_full()

    pygame.display.update()