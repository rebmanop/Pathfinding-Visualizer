import pygame
from grid import Grid

class LegendCell:
    def __init__(self, win, x, y, color, frame_color, grid: Grid) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.color = color
        self.width, self.height = grid.gap, grid.gap
        self.frame_color = frame_color
        

    def draw_legend_cell(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.line(self.win, self.frame_color, (self.x, self.y), (self.x,  self.y + self.height))
        pygame.draw.line(self.win, self.frame_color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        pygame.draw.line(self.win, self.frame_color, (self.x, self.y), (self.x + self.width, self.y))
        pygame.draw.line(self.win, self.frame_color, (self.x, self.y + self.height), (self.x + self.width,  self.y + self.height))