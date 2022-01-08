from cell import Cell
import pygame

GREY = (130, 127, 125)

def make_grid(rows, width) -> None:
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)


    return grid




def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
          pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

