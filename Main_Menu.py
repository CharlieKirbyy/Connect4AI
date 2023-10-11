import pygame, sys, math, random, numpy as np
from button import Button

# Variables used throughout the program often used to eliminate magic numbers 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_NO = 6
COLUMN_NO = 7
PLAYER_PIECE = 1
AI_PIECE = 2
PLAYER = 0
AI = 1
PLAYER2 = 1
WINDOW_LENGTH = 4
EMPTY = 0
pygame.init() # Initialises pygame
SCREEN = pygame.display.set_mode((1280, 720)) # Sets menu screen size to the correct resolution
pygame.display.set_caption("Connect4") # Renames game window to "Connect4"
BG = pygame.image.load("assets/Background.png") # Loads in the ambient background for the menu

def create_board():
    # Creates a 6 by 7 Matrix of all zeros (the board)
    board = np.zeros((ROW_NO,COLUMN_NO))
    return board

def place_piece(board, row, column, piece):
    # Fills the board with the piece that the player just dropped
    board[row][column] = piece

def valid_location(board, column):
    # Checks to see whether a piece can be placed in the chosen location
    return board[ROW_NO -1][column] == 0

def get_next_open_row(board, column):
    # Checks to see which row is open in the column and stack the new piece on any existing piece
    for r in range(ROW_NO):
        if board[r][column] == 0:
            return r

def flipped_board(board):
    # Flips the matrix vertically (board)       
    print(np.flip(board, 0))

def game_win(board, row, column):
    # Checks the game for a game win  
    item = board[row][column]
    rows = len(board)
    cols = len(board[0])
    if item == 0:
        return False
    for deltrow, deltcolumn in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        consecutive_items = 1
        for delta in (1, -1):
            deltrow *= delta
            deltcolumn *= delta
            next_row = row + deltrow
            next_col = column + deltcolumn
            while 0 <= next_row < rows and 0 <= next_col < cols:
                if board[next_row][next_col] == item:
                    consecutive_items += 1
                else:
                    break
                if consecutive_items == 4:
                    return True
                next_row += deltrow
                next_col += deltcolumn
    return False

def game_win2(board, piece):
	# Check Horizontal Win
	for c in range(COLUMN_NO-3):
		for r in range(ROW_NO):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check Vertical Win
	for c in range(COLUMN_NO):
		for r in range(ROW_NO-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check Positive Diagonal Win
	for c in range(COLUMN_NO-3):
		for r in range(ROW_NO-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check Negative Diagonal Win
	for c in range(COLUMN_NO-3):
		for r in range(3, ROW_NO):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
    # Evaluates how much each empty position will be worth in terms of placing each piece to try and achieve 4 in a row
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
    # Creates lists in windows of 4 and evaluates them using the evaluate_window function to score each move
	total_points = 0

	# Total points Center Column
	center_array = [int(i) for i in list(board[:, COLUMN_NO//2])]
	center_count = center_array.count(piece)
	total_points += center_count * 2

	# Horizontal total points
	for r in range(ROW_NO):
		row_list = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_NO-3):
			window = row_list[c:c+WINDOW_LENGTH]
			total_points += evaluate_window(window, piece)

	# Vertical total points
	for c in range(COLUMN_NO):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_NO-3):
			window = col_array[r:r+WINDOW_LENGTH]
			total_points += evaluate_window(window, piece)

	# Diagonal total points Positive
	for r in range(ROW_NO-3):
		for c in range(COLUMN_NO-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			total_points += evaluate_window(window, piece)

    # Diagonal total points Negative
	for r in range(ROW_NO-3):
		for c in range(COLUMN_NO-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			total_points += evaluate_window(window, piece)
	return total_points

def is_terminal_node(board):
    # A True or False function to see whether or not the node is terminal, meaning that there are no possible options to choose from
	return game_win2(board, PLAYER_PIECE) or game_win2(board, AI_PIECE) or len(get_is_valid_loc(board)) == 0

def minimax(board, depth, alpha, beta, maximisingPlayer):
    # Minimax algorithm that is allowing the AI to evaluate the best possible move
	is_valid_loc = get_is_valid_loc(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal: # Terminal conditions
			if game_win2(board, AI_PIECE):
				return (None, 10000000) # If the AI can make a winning move then the position move is worth a substantial amount 
			elif game_win2(board, PLAYER_PIECE):
				return (None, -1000000) # If the player can make a winning move then the position move is worth a large negative number for the AI 
			else: #Game Over
				return (None, 0)
		else: #Depth is 0
			return (None, total_points_position(board, AI_PIECE))
	if maximisingPlayer: 
		value = -math.inf
		col = random.choice(is_valid_loc)
		for column in is_valid_loc:
			row = get_next_open_row(board, column)
			b_copy = board.copy() # Another copy of the board to prevent using the same memory location which could lead to issues when recursing back up the tree
			place_piece(b_copy, row, column, AI_PIECE)
			updated_total = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if updated_total > value: # Chooses which column is best and updates the score
				value = updated_total
				col = column
			alpha = max(alpha, value) # Alpha Beta pruning to determine which is the best possible value, acts quicker than the base minimax algorithm
			if alpha >= beta:
				break
		return col, value # To see the new score and the column that produces that score

	else: #Minimising Player
		value = math.inf
		column = random.choice(is_valid_loc)
		for column in is_valid_loc:
			row = get_next_open_row(board, column)
			b_copy = board.copy()
			place_piece(b_copy, row, column, PLAYER_PIECE)
			updated_total = minimax(b_copy, depth-1, alpha, beta, True)[1] # False and True (in maximising player) are what is being used to switch back and forth between min and max players
			if updated_total < value:
				value = updated_total
				col = column
			beta = min(beta, value)
			if alpha >= beta:
				break
		return col, value

def get_is_valid_loc(board):
    # Checks if the location is valid for the AI before it places a piece there, useful within the choose_best_move function
	is_valid_loc = []
	for column in range(COLUMN_NO):
		if valid_location(board, column):
			is_valid_loc.append(column)
	return is_valid_loc

def choose_best_move(board, piece):
    # Ensures that with each move the AI is building a better score to win the game
	is_valid_loc = get_is_valid_loc(board)
	most_points = -10000 # Using a low number so that the AI will find it easier to improve upon this and aim for the best possible positions 
	best_column = random.choice(is_valid_loc)
	for column in is_valid_loc:
		row = get_next_open_row(board, column)
		temp_board = board.copy() # Creates a new memory location for the board so that it does not modify the original board when choosing the new position
		place_piece(temp_board, row, column, piece)
		total_points = total_points_position(temp_board, piece)
		if total_points > most_points: # If the new position is more valuable then it will place it in this new position
			most_points = total_points
			best_column = column
	return best_column

def draw_board(SCREEN, board, PIXELSIZE, RADIUS, height):
    # Draws the classic Connect 4 board in pygame
	for c in range(COLUMN_NO):
		for r in range(ROW_NO):
			pygame.draw.rect(SCREEN, BLUE, (c*PIXELSIZE, r*PIXELSIZE+PIXELSIZE, PIXELSIZE, PIXELSIZE))
			pygame.draw.circle(SCREEN, BLACK, (int(c*PIXELSIZE+PIXELSIZE/2), int(r*PIXELSIZE+PIXELSIZE+PIXELSIZE/2)), RADIUS)
	
	for c in range(COLUMN_NO):
		for r in range(ROW_NO):		
			if board[r][c] == PLAYER_PIECE: # Draws a red piece for the Player when placed
				pygame.draw.circle(SCREEN, RED, (int(c*PIXELSIZE+PIXELSIZE/2), height-int(r*PIXELSIZE+PIXELSIZE/2)), RADIUS) # "-height" allows the piece to drop to the bottom available position in the column 
			elif board[r][c] == AI_PIECE: # Draws a yellow piece for the AI when placed
				pygame.draw.circle(SCREEN, YELLOW, (int(c*PIXELSIZE+PIXELSIZE/2), height-int(r*PIXELSIZE+PIXELSIZE/2)), RADIUS)
	pygame.display.update()              

# Defines board
board = create_board()
flipped_board(board)

def get_font(size):
    # Obtains the font style from the downloaded file to use in the game and its menu
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    # Creates the main menu that is presented when the game is booted up
    pygame.display.set_mode((1280, 720)) # Sets screen resolution
    while True:
        SCREEN.blit(BG, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render(" CONNECT 4 ", True, "Orange")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        # Gives the menu buttons colours when hovered over to ensure the user knows it is being interacted with
        AI_BUTTON = Button(image=pygame.image.load("assets/AI Rect.png"), pos=(640, 250), 
                            text_input="AI", font=get_font(75), base_colour="White", hovering_colour="Yellow")
        TWO_PLAYERS_BUTTON = Button(image=pygame.image.load("assets/2P Rect.png"), pos=(640, 400), 
                            text_input="2 PLAYER", font=get_font(70), base_colour="White", hovering_colour="Red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_colour="White", hovering_colour="Blue")
        

        # Uses the button class to ensure the menu screen can be interacted with when clicking the desired button
        for button in [AI_BUTTON, TWO_PLAYERS_BUTTON, QUIT_BUTTON]:
            button.change_colour(MOUSE_POS)
            button.update(SCREEN)
        # Tells the program which functions to use depending on which button is clicked within the menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AI_BUTTON.checkForInput(MOUSE_POS):
                    AI_game()
                if TWO_PLAYERS_BUTTON.checkForInput(MOUSE_POS):
                    no_AI_game()
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Allows the minimax algorithm to work within the AI_game function, tells the depth of how many positions to evaluate ahead of the current position
col, minimax_total_points = minimax(board, 1, -math.inf, math.inf, True)

def AI_game():  
    # Main game loop for one player and the AI 
    myfont = pygame.font.Font("assets/font.ttf", 45)
    # Creates the size of the board and pieces
    PIXELSIZE = 100
    width = COLUMN_NO * PIXELSIZE
    height = (ROW_NO + 1) * PIXELSIZE # We want the height to be one higher than the board so that we can see the piece above the board before we place it
    size = (width, height)
    RADIUS = int(PIXELSIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(size)

    while True:  
        # Creates a fresh board every time the function is called
        board = create_board()
        flipped_board(board)
        draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)
        pygame.display.update()
        game_over = False
        turn = random.randint(PLAYER, AI) # Allows the starting player to be randomised
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # Allows the player to close window at any point 

                if event.type == pygame.MOUSEMOTION: # Draws the piece and shows its position on every mouse motion  
                    pygame.draw.rect(SCREEN, BLACK, (0,0, width, PIXELSIZE)) # Fills in black where the piece is not currently hovering
                    posx = event.pos[0]
                    if turn == PLAYER: # This means that whenever it is the player's mover their piece will be Red
                        pygame.draw.circle(SCREEN, RED, (posx, int(PIXELSIZE/2)), RADIUS)
                pygame.display.update() # Updates screen on every mouse motion
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(SCREEN, BLACK, (0,0, width, PIXELSIZE))
                    # Ask for Player's move
                    if turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/PIXELSIZE))
                        # Checks if the chosen position is available and then drops a piece
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            place_piece(board, row, col, PLAYER_PIECE)
                            # Checks if there is a winning move and tells the player they are the winner 
                            if game_win2(board, PLAYER_PIECE):
                                win_msg = myfont.render("YOU Win!", 1, RED)
                                SCREEN.blit(win_msg, (180,25))
                                game_over = True
                            # Alternates turns between each player 
                            turn = (turn + 1) % 2
                        # Drawns the new board after each turn is taken
                        flipped_board(board)
                        draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)
            # If it is the AI player's turn this if loop will run instead
            if turn == AI and not game_over:				
                column, minimax_total_points = minimax(board, 1, -math.inf, math.inf, True) # Calls on the minimax algorithm function to evaluate the best possible move

                if valid_location(board, column):
                    pygame.time.wait(500) # Gives half a second before the AI chooses where to place its piece, this gives the impression of the AI being a real player
                    row = get_next_open_row(board, column)
                    place_piece(board, row, column, AI_PIECE)
                    
                    flipped_board(board)
                    draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)

                    if game_win2(board, AI_PIECE): # If the AI wins it lets the player know and turns the game_over boolean to True
                        win_msg = myfont.render("YELLOW Wins!", 2, YELLOW)
                        SCREEN.blit(win_msg, (50,25))
                        game_over = True
                        # Prints an updated board after every move
                        flipped_board(board)
                        draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)
                    
                    # Alternates turns after every move 
                    turn = (turn + 1) % 2
            # Once the game_boolean is True the game waits for 3 seconds before returning to the main menu
            if game_over:
                pygame.time.wait(3000)
                main_menu()

def no_AI_game():
    # Main game loop for two players, similar to AI game function however it allows two players to play one another
    myfont = pygame.font.Font("assets/font.ttf", 45)
    PIXELSIZE = 100
    width = COLUMN_NO * PIXELSIZE
    height = (ROW_NO + 1) * PIXELSIZE
    size = (width, height)
    RADIUS = int(PIXELSIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(size)

    while True:  
        board = create_board()
        flipped_board(board)
        draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)
        pygame.display.update()
        game_over = False
        turn = random.randint(PLAYER, PLAYER2) # Randomly chooses which player goes first
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION: # Draws the pieces along the top row on mouse motion
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, width, PIXELSIZE))
                    posx = event.pos[0]
                    if turn == PLAYER: # Draws a red piece for player 1
                        pygame.draw.circle(SCREEN, RED, (posx, int(PIXELSIZE / 2)), RADIUS)
                    else: # Draws a yellow piece for player 2
                        pygame.draw.circle(SCREEN, YELLOW, (posx, int(PIXELSIZE / 2)), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN: # Executes everything inside the loop when the mouse is clicked
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, width, PIXELSIZE))
                    posx = event.pos[0] # Stores the clicked position value 
                    column = int(math.floor(posx / PIXELSIZE)) # Rounds the clicked position value down to a number between 0-6

                    # Checks if the chosen postion is available, if so it places the piece
                    if valid_location(board, column):
                        row = get_next_open_row(board, column)
                        place_piece(board, row, column, turn + 1)

                        # If a game winning move is found the game announces who wins and changes the game_over variable to True
                        if game_win(board, row, column):
                            win_msg = myfont.render(f"PLAYER {turn + 1} WINS!", 1, RED if turn == 0 else YELLOW)
                            SCREEN.blit(win_msg, (50, 25))
                            game_over = True

                        flipped_board(board)
                        draw_board(SCREEN, board, PIXELSIZE, RADIUS, height)

                    turn = (turn + 1) % 2
        # Once the game is over the game waits 3 seconds before returning to the main menu
        if game_over:
            pygame.time.wait(3000)
            main_menu()

# Ensures that when the program is booted up that the Menu is called and used
main_menu()