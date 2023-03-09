import numpy as np
import random
import pygame
import sys
import math

## Instellingen ##

Row_Number = 4
Column_Number = 4
Square_Size = 100
Radius = int(Square_Size/2 - 12)
notVisited = 0
visited  = 1
PlayerPiece = 0
AIPiece = 1

BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
GREY = (128,128,128)
WHITE = (255,255,255)

## Instellingen ##

def isValidLocation(board,row,col,myPosition,opponentPosition):
    r,c = myPosition
    r2,c2 = opponentPosition
    return (row != -1 and (board[row][col] == notVisited) and (row!=r or col!=c) and (row!=r2 or col!=c2) and (abs(row-r)<=1) and (abs(col-c)<=1)) #zorgt dat alle stappen mogelijk zijn

def isValidPosition(row,col):
    return (row>=0 and row<Row_Number and col>=0 and col<Column_Number)

def get_valid_locations(board,position,opponentPosition):
	valid_locations = []
	r,c = position
	if isValidPosition(r+1,c) and isValidLocation(board,r+1,c,position,opponentPosition):
		valid_locations.append((r+1,c))
	if isValidPosition(r-1,c) and isValidLocation(board,r-1,c,position,opponentPosition):
		valid_locations.append((r-1,c))
	if isValidPosition(r,c+1) and isValidLocation(board,r,c+1,position,opponentPosition):
		valid_locations.append((r,c+1))
	if isValidPosition(r,c-1) and isValidLocation(board,r,c-1,position,opponentPosition):
		valid_locations.append((r,c-1))
	if isValidPosition(r+1,c+1) and isValidLocation(board,r+1,c+1,position,opponentPosition):
		valid_locations.append((r+1,c+1))
	if isValidPosition(r+1,c-1) and isValidLocation(board,r+1,c-1,position,opponentPosition):
		valid_locations.append((r+1,c-1))
	if isValidPosition(r-1,c+1) and isValidLocation(board,r-1,c+1,position,opponentPosition):
		valid_locations.append((r-1,c+1))
	if isValidPosition(r-1,c-1) and isValidLocation(board,r-1,c-1,position,opponentPosition):
		valid_locations.append((r-1,c-1))
	return valid_locations

def winningMove(board,position,opponentPosition):
    return len(get_valid_locations(board,position,opponentPosition)) == 0

def is_terminal_node(board, PlayerPosition, AIPosition):
	return winningMove(board, PlayerPosition,AIPosition) or winningMove(board, AIPosition,PlayerPosition)

def score_position(a, b, board, AIPosition, PlayerPosition):
    return (a*len(get_valid_locations(board,AIPosition,PlayerPosition)) - b*len(get_valid_locations(board,PlayerPosition,AIPosition)))

def minimax(board, depth, alpha, beta, maximizingPlayer, PlayerPosition, AIPosition):
	is_terminal = is_terminal_node(board,PlayerPosition,AIPosition)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winningMove(board, PlayerPosition,AIPosition):
				return (None, None, 100000000000000)
			elif winningMove(board, AIPosition,PlayerPosition):
				return (None, None, -10000000000000)
		else: # Depth is 0
			return (None, None, score_position(1,2,board, AIPosition, PlayerPosition))


	if maximizingPlayer:
		valid_locations = get_valid_locations(board, AIPosition,PlayerPosition)
		value = -math.inf # begin met de slechtst mogelijke score
		temp = random.randrange(len(valid_locations))
		row,column = valid_locations[temp]
		for _ in valid_locations:
			b_copy = board.copy()
			r,c = AIPosition
			if not(b_copy[r][c] == 2):
				b_copy[r][c] = visited
			AIPosition = _
			new_score = minimax(b_copy, depth-1, alpha, beta, False, PlayerPosition, AIPosition)[2]
			if new_score > value:
				value = new_score
				row,column = _
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return row, column, value

	else: # Minimizing player
		valid_locations = get_valid_locations(board, PlayerPosition,AIPosition)
		value = math.inf #begin met de slechtst mogelijke score
		temp = random.randrange(len(valid_locations))
		row,column = valid_locations[temp]
		for _ in valid_locations:
			b_copy = board.copy()
			r,c = PlayerPosition
			if not(b_copy[r][c] == 2):
				b_copy[r][c] = visited
			PlayerPosition = _
			new_score = minimax(b_copy, depth-1, alpha, beta, True, PlayerPosition, AIPosition)[2]
			if new_score < value:
				value = new_score
				row,column = _
			beta = min(beta, value)
			if alpha >= beta:
				break
		return row, column, value     

def draw_board(board):
	for c in range(Column_Number):
		for r in range(Row_Number):
			if board[r][c]==1:
				pygame.draw.rect(screen, BLACK, (c*Square_Size + 5, (r+1)*Square_Size + 5, Square_Size-5, Square_Size-5))
			elif board[r][c] == 2:
				pygame.draw.rect(screen, WHITE, (c*Square_Size + 5, (r+1)*Square_Size + 5, Square_Size-5, Square_Size-5))
			else:
				pygame.draw.rect(screen, WHITE, (c*Square_Size + 5, (r+1)*Square_Size + 5, Square_Size-5, Square_Size-5))

board = np.zeros((Row_Number,Column_Number))
gameOver = False

pygame.init()

width = Column_Number * Square_Size + 5
height = (Row_Number+1) * Square_Size + 5

size = (width, height)

screen = pygame.display.set_mode(size)

#0,0 is linksboven, 3,3 is rechtsonder
ROW1 = 0 
COL1 = 0 

ROW2 = 3 
COL2 = 3 
    
PlayerPosition = (ROW1,COL1)
AIPosition = (ROW2,COL2)    
   
draw_board(board)

queenwhite = pygame.image.load('queenwhitev2.png')
queenwhite = pygame.transform.scale(queenwhite, (100, 100))
queenblack = pygame.image.load('queenblack.png')
queenblack = pygame.transform.scale(queenblack, (100, 100))

screen.blit(queenblack, ((COL1-0.5)*Square_Size + int(Square_Size/2 + 2.5),(ROW1+0.5)*Square_Size + int(Square_Size/2 + 2.5))) #Initialiseert beide koninginnen op het bord.
screen.blit(queenwhite, ((COL2-0.5)*Square_Size + int(Square_Size/2 + 2.5),(ROW2+0.5)*Square_Size + int(Square_Size/2 + 2.5)))

pygame.display.update()

myfont = pygame.font.SysFont("tahoma", 50)
pygame.display.set_caption('Isolation Game')
pygame.display.set_icon(queenblack)

turn = 0

while not gameOver: #game loop
    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if turn == PlayerPiece:
				posx = event.pos[0]
				col = int(math.floor(posx/Square_Size))
				posy = event.pos[1]
				row = int(math.floor(posy/Square_Size)) - 1
				

				if isValidLocation(board, row, col, PlayerPosition,AIPosition):
					r,c = PlayerPosition
					if not(board[r][c] == 2):
						board[r][c] = visited
					PlayerPosition = (row,col)
                    
					if winningMove(board, AIPosition,PlayerPosition):
						label = myfont.render("speler wint", 1, WHITE)
						screen.blit(label, (50,10)) #(125,10))
						gameOver = True
					elif winningMove(board, PlayerPosition,AIPosition):
						label = myfont.render("AI wint", 1, WHITE)
						screen.blit(label, (50,10)) #(200,10))
						gameOver = True

					turn += 1
					turn = turn % 2

					draw_board(board) #na spel
					screen.blit(queenblack, ((col-0.5)*Square_Size + int(Square_Size/2 + 2.5),(row+0.5)*Square_Size + int(Square_Size/2 + 2.5)))
					row2,col2 = AIPosition
					screen.blit(queenwhite, ((col2-0.5)*Square_Size + int(Square_Size/2 + 2.5),(row2+0.5)*Square_Size + int(Square_Size/2 + 2.5)))
					pygame.display.update()

	if turn == AIPiece and not gameOver:				
		row, col, minimax_score = minimax(board, 8, -math.inf, math.inf, True, PlayerPosition, AIPosition)
		if isValidLocation(board, row, col, AIPosition, PlayerPosition):
			r,c = AIPosition
			if not(board[r][c] == 2):
				board[r][c] = visited
			AIPosition = (row,col)
   
			if winningMove(board, PlayerPosition,AIPosition):
				label = myfont.render("AI wint", 1, WHITE)
				screen.blit(label, (200,10))
				gameOver = True
			elif winningMove(board, AIPosition,PlayerPosition):
				label = myfont.render("speler wint", 1, WHITE)
				screen.blit(label, (125,10))
				gameOver = True

			draw_board(board) #tijdens spel
			screen.blit(queenwhite, ((col-0.5)*Square_Size + int(Square_Size/2 + 2.5),(row+0.5)*Square_Size + int(Square_Size/2 + 2.5)))
			row2,col2 = PlayerPosition
			screen.blit(queenblack, ((col2-0.5)*Square_Size + int(Square_Size/2 + 2.5),(row2+0.5)*Square_Size + int(Square_Size/2 + 2.5)))
			pygame.display.update()
   
			turn += 1
			turn = turn % 2

	if gameOver:
		pygame.time.wait(5000)