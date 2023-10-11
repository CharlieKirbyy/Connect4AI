import numpy as np
import pygame
import sys
import random
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
EMPTY = 0
#Static Variables, all caps to show this
#These are also to remove all magic numbers in the code

def create_board():
	board = np.zeros((ROW_COUNT
, COLUMN_COUNT))
	return board

def place_piece(board, row, column, piece):
	board[row][column] = piece

def valid_location(board, column):
	return board[ROW_COUNT
-1][column] == 0

def get_next_open_row(board, column):
	for r in range(ROW_COUNT
):
		if board[r][column] == 0:
			return r

def flipped_board(board):
	print(np.flip(board, 0))
 #Since it is reading the top left poition of our Connect 4 board as [0,0] we have to 
 #flip the board to allow the first placed piece to be on the botttom row

def game_win2(board, piece):
	# Check Horizontal Win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT
	):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check Vertical Win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT
	-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check Positive Diagonal Win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT
	-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check Negative Diagonal Win
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT
	):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	total_points = 0
	Opponent_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		Opponent_piece = AI_PIECE

	if window.count(piece) == 4:
		total_points += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		total_points += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		total_points += 2
	if window.count(Opponent_piece) == 3 and window.count(EMPTY) == 1:
		total_points -= 4
	return total_points

def total_points_position(board, piece):
	total_points = 0

	#total_points Center Column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	total_points += center_count * 3

	##Horizontal total_points
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			total_points += evaluate_window(window, piece)

	#Vertical total_points
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT
	-3):
			window = col_array[r:r+WINDOW_LENGTH]
			total_points += evaluate_window(window, piece)

	#Diagonal total_points Positive
	for r in range(ROW_COUNT
-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			total_points += evaluate_window(window, piece)

    #Diagonal total_points Negative
	for r in range(ROW_COUNT
-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			total_points += evaluate_window(window, piece)

	return total_points

def is_terminal_node(board):
	return game_win2(board, PLAYER_PIECE) or game_win2(board, AI_PIECE) or len(get_is_valid_loc(board)) == 0

def minimax(board, depth, alpha, beta, maximisingPlayer):
	is_valid_loc = get_is_valid_loc(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if game_win2(board, AI_PIECE):
				return (None, 100000000000000)
			elif game_win2(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: #Game Over
				return (None, 0)
		else: #Depth is 0
			return (None, total_points_position(board, AI_PIECE))
	if maximisingPlayer: 
		value = -math.inf
		col = random.choice(is_valid_loc)
		for column in is_valid_loc:
			row = get_next_open_row(board, column)
			b_copy = board.copy()
			place_piece(b_copy, row, column, AI_PIECE)
			updated_total = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if updated_total > value:
				value = updated_total
				col = column
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return col, value

	else: #Minimising Player
		value = math.inf
		column = random.choice(is_valid_loc)
		for column in is_valid_loc:
			row = get_next_open_row(board, column)
			b_copy = board.copy()
			place_piece(b_copy, row, column, PLAYER_PIECE)
			updated_total = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if updated_total < value:
				value = updated_total
				col = column
			beta = min(beta, value)
			if alpha >= beta:
				break
		return col, value

def get_is_valid_loc(board):
	is_valid_loc = []
	for column in range(COLUMN_COUNT):
		if valid_location(board, column):
			is_valid_loc.append(column)
	return is_valid_loc

def pick_best_move(board, piece):
	is_valid_loc = get_is_valid_loc(board)
	most_points = -10000
	best_column = random.choice(is_valid_loc)
	for column in is_valid_loc:
		row = get_next_open_row(board, column)
		temp_board = board.copy()
		place_piece(temp_board, row, column, piece)
		total_points = total_points_position(temp_board, piece)
		if total_points > most_points:
			most_points = total_points
			best_column = column
	return best_column

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT
	):
			pygame.draw.rect(screen, BLUE, (c*PIXELSIZE, r*PIXELSIZE+PIXELSIZE, PIXELSIZE, PIXELSIZE))
			pygame.draw.circle(screen, BLACK, (int(c*PIXELSIZE+PIXELSIZE/2), int(r*PIXELSIZE+PIXELSIZE+PIXELSIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT
	):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*PIXELSIZE+PIXELSIZE/2), height-int(r*PIXELSIZE+PIXELSIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*PIXELSIZE+PIXELSIZE/2), height-int(r*PIXELSIZE+PIXELSIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
flipped_board(board)
game_over = False

pygame.init()

PIXELSIZE = 105

width = COLUMN_COUNT * PIXELSIZE
height = (ROW_COUNT+1) * PIXELSIZE

size = (width, height)

RADIUS = int(PIXELSIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.Font("assets/font.ttf", 45)

turn = random.randint(PLAYER, AI)

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, PIXELSIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(PIXELSIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, PIXELSIZE))
			
            # Ask for the Player's move
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/PIXELSIZE))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					place_piece(board, row, col, PLAYER_PIECE)

					if game_win2(board, PLAYER_PIECE):
						label = myfont.render("YOU Win!", 1, RED)
						screen.blit(label, (180,25))
						game_over = True

					turn += 1
					turn = turn % 2

					flipped_board(board)
					draw_board(board)

	if turn == AI and not game_over:				
		column, minimax_total_points = minimax(board, 3, -math.inf, math.inf, True)

		if valid_location(board, column):
			pygame.time.wait(500)
			row = get_next_open_row(board, column)
			place_piece(board, row, column, AI_PIECE)

			if game_win2(board, AI_PIECE):
				label = myfont.render("YELLOW Wins!", 2, YELLOW)
				screen.blit(label, (50,25))
				game_over = True

			flipped_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(2000)