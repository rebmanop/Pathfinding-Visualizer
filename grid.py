import pygame
from cell import Cell


GREY = (130, 127, 125)

class Grid:
    def __init__(self, win, grid_size, grid_dimensions, grid_position):
        self.win = win 
        self.grid_size = grid_size
        self.total_rows, self.total_columns = grid_size
        self.width, self.height  = grid_dimensions
        self.gap = self.width // self.total_columns
        self.line_color = GREY
        self.grid_position = grid_position
        self.x, self.y = self.grid_position
        self.raw_grid  = self.init_cells()
        


    def init_cells(self):
        raw_grid = []

        for i in range(self.total_rows):
            raw_grid.append([])
            for j in range(self.total_columns):
                raw_grid[i].append(Cell(i, j, self.gap, self.grid_size, self.grid_position))

        return raw_grid
        

    def draw_grid_lines(self) -> None:
        for i in range(self.total_rows + 1):
            pygame.draw.line(self.win, self.line_color, (self.x, self.y + i * self.gap), (self.x + self.width, self.y + i * self.gap))
            for j in range(self.total_columns + 1):
                pygame.draw.line(self.win, self.line_color, (self.x + j * self.gap, self.y), (self.x + j * self.gap, self.y + self.height))


    def update_neighbors_for_every_cell(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.update_neighbors(self.raw_grid)

    def update_neighbors_by_direction_for_every_cell(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.update_neighbors_by_direction(self.raw_grid)


    def draw_under_grid_cells(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                if not cell.is_wall():
                    cell.draw(self.win)

    def draw_over_grid_cells(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                if cell.is_wall(): 
                    cell.draw(self.win)


    def get_cell(self, row: int, col: int) -> Cell:
        return self.raw_grid[row][col]
    

    def get_row_col_of_clicked_cell(self, mpos) -> tuple:
        x, y = mpos

        row =  (y - self.y) // self.gap
        col = (x - self.x) // self.gap
        
        return int(row), int(col) 
    
    
    def clear(self, start_end_except = False, barrier_except = False) -> None:
        """clears the grid with an optional exclusion"""
        if start_end_except == True and barrier_except == True:       
            for row in self.raw_grid:
                for  cell in row:
                    if not cell.is_start() and not cell.is_end() and not cell.is_wall(): 
                        cell.reset()

        elif start_end_except == True:
            for row in self.raw_grid:
                for  cell in row:
                    if not cell.is_start() and not cell.is_end(): 
                        cell.reset()

        else:
            for row in self.raw_grid:
                for  cell in row: 
                        cell.reset()




    def make_all_cells_wall(self) -> None:
        for row in self.raw_grid:
            for cell in row:
                cell.make_wall()


    def mouse_on_the_grid(self) -> bool:
        mpos = pygame.mouse.get_pos()
        if (mpos[0] > self.x and mpos[0] < (self.x + self.width) 
        and mpos[1] > self.y and mpos[1] < (self.y + self.height)):
            return True
        else:
            return False


    def __getitem__(self, row):
        return self.raw_grid[row]


