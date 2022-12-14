import numpy as np
import pygame
import sys
import math

#setting colors in rgb notation
WHITE=(255,255,255)
BLACK = (0, 0, 0)
BLUE = (93, 63, 211)
YELLOW = (255, 255, 0)

#setting number of rows and columns for disk holders
numberofrows = 6
numberofcolumns = 7

#creating board by numpy arrays of zeros initially(empty holders only)
def create_board():
    board = np.zeros((numberofrows, numberofcolumns))
    return board

#function to drop the disk (setting the piece to the index of array specified as row and column
def drop_disk(board, row, col, piece):
    board[row][col] = piece

#checking id location to drop is valid/checking if the holder above is empty
def location_is_valid(board, col):
    return board[numberofrows - 1][col] == 0

#getting the next open row where to put disk
def get_next_open_row(board, col):
    for r in range(numberofrows):
        if board[r][col] == 0:
            return r

#printing the game board
def print_board(board):
    print(np.flip(board, 0))

#checking if 4 disks are connected
def check_win(board, piece):
    # horizontal win checks
    for c in range(numberofcolumns - 3):
        for r in range(numberofrows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # vertical win checks
    for c in range(numberofcolumns):
        for r in range(numberofrows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # positive sloped diagonals check
    for c in range(numberofcolumns - 3):
        for r in range(numberofrows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # negative sloped diagonals check
    for c in range(numberofcolumns - 3):
        for r in range(3, numberofrows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

#board is drawn to the screen with circles as holders
def draw_board(board):
    for c in range(numberofcolumns):
        for r in range(numberofrows):
            pygame.draw.rect(screen, WHITE, (c * gameboardsize, r * gameboardsize + gameboardsize, gameboardsize, gameboardsize))
            pygame.draw.circle(screen, BLACK, (
            int(c * gameboardsize + gameboardsize / 2), int(r * gameboardsize + gameboardsize + gameboardsize / 2)), RADIUS)

    for c in range(numberofcolumns):
        for r in range(numberofrows):
            if board[r][c] == 1:
                pygame.draw.circle(screen, BLUE, (
                int(c * gameboardsize + gameboardsize / 2), height - int(r * gameboardsize + gameboardsize / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * gameboardsize + gameboardsize / 2), height - int(r * gameboardsize + gameboardsize / 2)), RADIUS)
    pygame.display.update()

#calling the functions and initializing variables
board = create_board()
print_board(board)
game_over = False
turn = 0

# initalize pygame
pygame.init()

# screen size definition
gameboardsize = 100

# calculating the board width and height
width = numberofcolumns * gameboardsize
height = (numberofrows + 1) * gameboardsize

#setting size to width and height and the radius of the circles calculation
size = (width, height)

RADIUS = int(gameboardsize / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
#setting the font by pygame fonts
myfont = pygame.font.SysFont("arial", 75)

#checking if game_over is not true(it will run until no player wins
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, gameboardsize))
            posx = event.pos[0]
            if turn == 0:
                #checking if it is player 1's turn or not
                pygame.draw.circle(screen, BLUE, (posx, int(gameboardsize / 2)), RADIUS)
            else:
                #adding yellow circles if it is player 2's turn
                pygame.draw.circle(screen, YELLOW, (posx, int(gameboardsize / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, gameboardsize))
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / gameboardsize))

                if location_is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_disk(board, row, col, 1)

                    if check_win(board, 1):
                        label = myfont.render("PLAYER 1 WINS!", 1, BLUE)
                        screen.blit(label, (40, 10))
                        #game_over is true when player 1 connects 4 and program comes out of while loop
                        game_over = True


            # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / gameboardsize))

                if location_is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_disk(board, row, col, 2)

                    if check_win(board, 2):
                        label = myfont.render("PLAYER 2 WINS!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        #game_over is true when player 2 connects 4 and program comes out of while loop
                        game_over = True

            #again printing board which is updated
            print_board(board)
            draw_board(board)

            #changing turns to give to player 1 and 2
            turn += 1
            turn = turn % 2

            # makes the gameboard wait for time specified if any player wins
            if game_over:
                pygame.time.wait(5000)