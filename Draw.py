# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 21:11:34 2022

@author: danny
"""
import pygame
import random as r

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
lime = (0, 255, 0)
blue = (0, 0, 255)
red = (128, 0, 0)
navy = (30, 30, 255)

width = 800
rows = 80
Game = pygame.display.set_mode((width, width))
pygame.display.set_caption("Game Test")
    
def find_neighbours(i, j):
    return [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]

def is_valid(i, j, m_row):
    if (0 <= i < m_row):
                
        return True
    
    else:
        
        return False
    
def manhattan_distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)
    
class square():
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.colour = (255, 255, 255)
        self.neighbours = []
        
    def get_pos(self):
        return (self.row, self.col)
    
    def closed_spot(self):
        return self.colour == red
        
    def opened_spot(self):
        return self.colour == blue
    
    def get_wall(self):
        return self.colour == black
    
    def get_start(self):
        return self.colour == lime
    
    def get_end(self):
        return self.colour == navy
    
    def reset(self):
        self.colour = white
        
    def draw_closed(self):
        self.colour = red
        
    def draw_opened(self):
        self.colour = lime
        
    def draw_wall(self):
        self.colour = black
        
    def draw_end(self):
        self.colour = navy
        
    def draw_start(self):
        self.colour = lime
    
    def draw(self,  Game):
        pygame.draw.rect(Game, self.colour, (self.x, self.y, self.width, self.width))
    
    def find_nearby_spots(self, matrix):
        self.neighbours = []
        
        for k in find_neighbours(self.row, self.col):
            look_row, look_col = k
            
            if (is_valid(look_row, look_col, self.total_rows) and not matrix[look_row][look_col].get_wall()):
                self.neighbours.append(matrix[look_row][look_col])
                
    def __lt__ (self, other):
        return False
    
# Creates square objects, puts it in a grid
def make_grid(rows, width):
    
    grid = []
    
    for x in range(rows):
        
        temp = []
        
        for y in range(rows):
            
            # Create square objects
            spot = square(x, y, (width // rows), rows)
            
            temp.append(spot)
            
        grid.append(temp)

    return grid

def draw_grid(Game, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(Game, white, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(Game, white, (j * gap, 0), (j * gap, width))

def draw(Game, grid, rows, width):
    Game.fill(white)

    for x in grid:
        for square in x:
            square.draw(Game)


    draw_grid(Game, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def initialize_game(Game, grid):
    for x in grid:
        for square in x:
            if (r.randint(0, 100) <= 75):
                square.draw(Game)
            else:
                square.draw_wall()
    
def main(Game, rows, width, generate):
    grid = make_grid(rows, width)
    
    start = None
    end = None
    
    if(generate):
        initialize_game(Game, grid)
    
    run = True
    while run:
        draw(Game, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                                
                spot.find_nearby_spots(grid)
                            
                spot.draw_wall()
        
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

    pygame.quit()

main(Game, rows, width, False)
