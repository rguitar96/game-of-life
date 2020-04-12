'''
Rules:
1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''

import pygame, sys
from pygame.locals import *
from random import choices

N_FPS = 10

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

CELL_SIZE = 10

if (WINDOW_WIDTH % CELL_SIZE != 0):
	WINDOW_WIDTH = floor(WINDOW_WIDTH / CELL_SIZE) * CELL_SIZE
if (WINDOW_HEIGHT % CELL_SIZE != 0):
	WINDOW_HEIGHT = floor(WINDOW_HEIGHT / CELL_SIZE) * CELL_SIZE

N_CELL_W = int(WINDOW_WIDTH / CELL_SIZE)
N_CELL_H = int(WINDOW_HEIGHT / CELL_SIZE)

BLACK =	(0,  0,  0)
WHITE =	(255,255,255)
GRAY =	(60, 60, 60)
GREEN =	(0,255,0)

DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def printGrid(state, show_grid):
	for cell in state:
		if state[cell] == 0:
		    pygame.draw.rect(DISPLAY, WHITE, (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
		elif state[cell] == 1:
			pygame.draw.rect(DISPLAY, GREEN, (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

	if show_grid:
		for x in range(0, N_CELL_W):
			pygame.draw.line(DISPLAY, GRAY, (x*CELL_SIZE,0),(x*CELL_SIZE,WINDOW_HEIGHT))

		for y in range(0, N_CELL_H):
			pygame.draw.line(DISPLAY, GRAY, (0,y*CELL_SIZE),(WINDOW_WIDTH,y*CELL_SIZE))

def getNeighbors(cell, state):
	n = 0
	for x in range(-1, 2):
		for y in range(-1, 2):
			neighborCell = (cell[0]+x, cell[1]+y)
			if (neighborCell != cell and neighborCell[0] >= 0 and neighborCell[0] < N_CELL_W and neighborCell[1] >= 0 and neighborCell[1] < N_CELL_H):
				n += state[neighborCell]
	return n

def tick(state):
	tmp_state = {}
	for cell in state:
		nNeighbours = getNeighbors(cell, state)

		if state[cell] == 1:			# if cell is alive
			if nNeighbours < 2:				# under population
				tmp_state[cell] = 0
			elif nNeighbours > 3:			# over population
				tmp_state[cell] = 0
			else:							# keep alive
				tmp_state[cell] = 1
		elif state[cell] == 0:			# if cell is dead
			if nNeighbours == 3:			# reproduction
				tmp_state[cell] = 1
			else:							# keep dead
				tmp_state[cell] = 0
	return tmp_state

def random_state(live_ratio=0.3):
	game_state = {}
	for x in range (N_CELL_W):
		for y in range (N_CELL_H):
			game_state[x,y] = 0

	for cell in game_state:
		game_state[cell] = choices(population=[0,1], weights=[1-live_ratio, live_ratio], k=1)[0]
	return game_state

def blank_state():
	game_state = {}
	for x in range (N_CELL_W):
		for y in range (N_CELL_H):
			game_state[x,y] = 0
	return game_state

def main():
	pygame.init()
	DISPLAY.fill(WHITE)

	paused = False
	show_grid = True

	# STATE initialization
	game_state = {}
	for x in range (N_CELL_W):
		for y in range (N_CELL_H):
			game_state[x,y] = 0

	printGrid(game_state, show_grid)
	pygame.display.update()
	pygame.display.set_caption("Game of Life")

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				# P: pause state
				if event.key == pygame.K_p:
					paused = not paused
				# R: random state
				if event.key == pygame.K_r:
					game_state = random_state()
				# B: blank state
				if event.key == pygame.K_b:
					game_state = blank_state()
				# G: show grid
				if event.key == pygame.K_g:
					show_grid = not show_grid
				# F: single frame
				if event.key == pygame.K_f:
					game_state = tick(game_state)

		mouse_pos = pygame.mouse.get_pos()

		if pygame.mouse.get_pressed()[0]:
			x = int(mouse_pos[0] / CELL_SIZE)
			y = int(mouse_pos[1] / CELL_SIZE)
			game_state[(x,y)] = 1
		
		if pygame.mouse.get_pressed()[2]:
			x = int(mouse_pos[0] / CELL_SIZE)
			y = int(mouse_pos[1] / CELL_SIZE)
			game_state[(x,y)] = 0

		if not paused:
			game_state = tick(game_state)

		printGrid(game_state, show_grid)
		pygame.display.update()

if __name__=='__main__':
    main()