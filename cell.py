import os
import pygame


PATH_COLOR = (255, 254, 106) # yellow
VISITED_COLOR = (64, 227, 206) # green
OPEN_COLOR = (197, 114, 255)# purple
WALL_COLOR = (30, 30, 30) # black
UNVISITED_COLOR = (255, 255, 255) # white
GREY = (130, 127, 125)
  

class Cell:
	POINT_A_IMG = None
	POINT_B_IMG = None


	def __init__(self, row, col, width, grid_size, grid_position):
		self.row = row
		self.col = col
		self.width = width
		self.total_rows, self.total_columns = grid_size
		self.color = UNVISITED_COLOR
		self.neighbors = []
		self.neighbor_by_direction = {}
		self.x = grid_position[0] + self.col * self.width
		self.y = grid_position[1] + self.row * self.width
	

	def get_pos(self):
		return self.row, self.col


	def is_visited(self):
		return self.color == VISITED_COLOR

	def is_open(self):	
		return self.color == OPEN_COLOR

	def is_wall(self):
		return self.color == WALL_COLOR

	def is_start(self):
		return self.color == Cell.POINT_A_IMG

	def is_end(self):
		return self.color == Cell.POINT_B_IMG
	
	def is_path(self):
		return self.color == PATH_COLOR

	def is_unvisited(self):
		return self.color == UNVISITED_COLOR


	def reset(self):
		self.color = UNVISITED_COLOR

	def make_start(self):
		self.color = self.POINT_A_IMG

	def visit(self):
		self.color = VISITED_COLOR

	def make_open(self):
		self.color = OPEN_COLOR

	def make_wall(self):
		self.color = WALL_COLOR

	def make_end(self):
		self.color = self.POINT_B_IMG	

	def make_path(self):
		self.color = PATH_COLOR


	def draw(self, win, animation=False):
		if self.is_start() or self.is_end():
			pygame.draw.rect(win, UNVISITED_COLOR, (self.x, self.y, self.width, self.width))
			win.blit(self.color, (self.x, self.y))	
		else:
			pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

		if animation:
			pygame.draw.line(win, GREY, (self.x, self.y), (self.x,  self.y + self.width))
			pygame.draw.line(win, GREY, (self.x + self.width, self.y), (self.x + self.width, self.y + self.width))
			pygame.draw.line(win, GREY, (self.x, self.y), (self.x + self.width, self.y))
			pygame.draw.line(win, GREY, (self.x, self.y + self.width), (self.x + self.width,  self.y + self.width))



	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): #down
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): #up
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_columns - 1 and not grid[self.row][self.col + 1].is_wall(): #right
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): #left
			self.neighbors.append(grid[self.row][self.col - 1])


	def update_neighbors_by_direction(self, grid):
		self.neighbor_by_direction = {}
		if self.row < self.total_rows - 1 : 
			self.neighbor_by_direction["down"] = grid[self.row + 1][self.col]
		else:
			self.neighbor_by_direction["down"] = None

		if self.row > 0: 
			self.neighbor_by_direction["up"] = grid[self.row - 1][self.col]
		else:
			self.neighbor_by_direction["up"] = None

		if self.col < self.total_columns - 1:
			self.neighbor_by_direction["right"] = grid[self.row][self.col + 1]
		else:
			self.neighbor_by_direction["right"] = None

		if self.col > 0: 
			self.neighbor_by_direction["left"] = grid[self.row][self.col - 1]
		else:
			self.neighbor_by_direction["left"] = None
	
	@staticmethod
	def scale_cell_imgs(width, height)-> None:
		Cell.POINT_A_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'letter-a.png')).convert_alpha(), (width, height))
		Cell.POINT_B_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'letter-b.png')).convert_alpha(), (width, height))

	

