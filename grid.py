import pygame
from cell import Cell

GREY = (130, 127, 125)

class Grid:
    def __init__(self, win, rows, width):
        self.win = win 
        self.total_rows = rows
        self.width = width
        self.height = width
        self.gap = self.width // self.total_rows
        self.raw_grid = self.init_all_cells()
        self.line_color = GREY


    def init_all_cells(self) -> list:
        raw_grid = []

        for i in range(self.total_rows):
            raw_grid.append([])
            for j in range(self.total_rows):
                cell = Cell(i, j, self.gap, self.total_rows)
                raw_grid[i].append(cell)

        return raw_grid

    
    def draw_grid_lines(self) -> None:
        for i in range(self.total_rows):
            pygame.draw.line(self.win, self.line_color, (0, i * self.gap), (self.width, i * self.gap))
            for j in range(self.total_rows):
                pygame.draw.line(self.win, self.line_color, (j * self.gap, 0), (j * self.gap, self.height))


    def update_all_neighbors_for_every_cell(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.make_barrier()
                cell.update_all_neighbors(self.raw_grid)


    def update_available_neighbors_for_every_cell(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.update_available_neighbors(self.raw_grid)


    def fill_cells_with_color(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.draw(self.win)


    def get_cell(self, row, col) -> Cell:
        return self.raw_grid[row][col]
    

    def get_row_col_of_clicked_cell(self, mpos) -> tuple:
        y, x = mpos

        row = y // self.gap
        col = x // self.gap

        return row, col