import random
from grid import Grid
from copy import deepcopy
from utils import aborted


class RoomCoordinates:
    def __init__(self, grid: Grid):
        self.top = 1
        self.bottom = grid.total_rows - 2
        self.left = 1
        self.right = grid.total_columns - 2 


def random_dfs_maze_gen(draw, points: tuple, grid, animation) -> None:    
    grid.make_all_cells_barrier()
    points[0].make_start()
    points[1].make_end()
    start = grid[0][0]
    visited_set = {start}
    stack = [start]

    while len(stack) > 0:
        if aborted():
            return

        current = stack.pop()
        neighbors =  [neighbor for neighbor in current.neighbors if neighbor not in visited_set]


        if len(neighbors) > 0:
            random_index = random.randint(0, len(neighbors) - 1)
            for neighbor in neighbors:
                visited_set.add(neighbor)
                
                if neighbor != neighbors[random_index]:
                    stack.append(neighbor)
                    
            
            stack.append(neighbors[random_index])
            if not current.is_unvisited() and not current.is_start() and not current.is_end():
                current.reset()

        if animation:
            draw()
        

def recursive_division_maze_gen(draw, grid: Grid, animation: bool) -> None:
    coordinates = RoomCoordinates(grid)
    draw_outside_border(draw, grid, animation)
    recursive_division(draw, grid, coordinates, animation)


def recursive_division(draw, grid: Grid, coordinates: RoomCoordinates, animation: bool) -> None:

    if (coordinates.bottom - coordinates.top) < (coordinates.right - coordinates.left):
        horizontal = False
    elif (coordinates.bottom - coordinates.top) > (coordinates.right - coordinates.left):
        horizontal = True
    else:
        horizontal = random.choice([True, False])

    available_idxes = get_available_indxes(grid, coordinates, horizontal)
    
    if len(available_idxes) == 0:
        horizontal = not horizontal
        available_idxes = get_available_indxes(grid, coordinates, horizontal)

        if len(available_idxes) == 0:
            return


    if len(available_idxes) == 1:
        wall_idx = available_idxes.pop()    
    else:
        wall_idx = available_idxes[len(available_idxes) // 2 ]


    build_wall(draw, grid, horizontal, wall_idx, coordinates, animation)
    carve_path(draw, grid, horizontal, wall_idx, coordinates, animation)
    
    if horizontal:
        coordinates_copy = deepcopy(coordinates)
        coordinates.top = wall_idx + 1
        recursive_division(draw, grid, coordinates, animation)

        coordinates_copy.bottom = wall_idx - 1 
        recursive_division(draw, grid, coordinates_copy, animation)

    else:
        coordinates_copy = deepcopy(coordinates)
        coordinates.left = wall_idx + 1 
        recursive_division(draw, grid, coordinates, animation)

        coordinates_copy.right = wall_idx - 1
        recursive_division(draw, grid, coordinates_copy, animation)


def get_available_indxes(grid: Grid, coordinates: RoomCoordinates, horizontal: bool) -> list:
    """returns list of valid wall indexes, so future wall wouldn't block exit out of the room 
        and wouldn't spawn rigth next to existing wall"""
    
    available_idxes = []
    if horizontal:
        for i in range(coordinates.top + 1, coordinates.bottom):
            if not grid[i][coordinates.left - 1].is_unvisited() and not grid[i][coordinates.right + 1].is_unvisited():
                available_idxes.append(i)
 
    else:
        for j in range(coordinates.left + 1, coordinates.right):
            if not grid[coordinates.top - 1][j].is_unvisited() and not grid[coordinates.bottom + 1][j].is_unvisited():
                available_idxes.append(j)

    return available_idxes
    
 
def build_wall(draw, grid: Grid, horizontal: bool, index: int, coordinates: RoomCoordinates, animation: bool) -> None:
    if horizontal:
        for j in range(coordinates.left, coordinates.right + 1):
            if not grid[index][j].is_start() and not grid[index][j].is_end():
                grid[index][j].make_wall()
            if aborted():
                return
            if animation:
                draw()
    
    else:
        for i in range(coordinates.top, coordinates.bottom + 1):
            if not grid[i][index].is_start() and not grid[i][index].is_end():
                grid[i][index].make_wall()
            if aborted():
                return
            if animation:
                draw()
            

def carve_path(draw, grid: Grid, horizontal: bool, index: int, coordinates: RoomCoordinates, animation: bool) -> None:
    if horizontal :    
        rand_idx = random.randint(coordinates.left, coordinates.right)
        if not grid[index][rand_idx].is_start() and not grid[index][rand_idx].is_end():
            grid[index][rand_idx].reset()
        if animation:
            draw()

    else:
        rand_idx = random.randint(coordinates.top, coordinates.bottom)
        if not grid[rand_idx][index].is_start() and not grid[rand_idx][index].is_end():
            grid[rand_idx][index].reset()
        if animation:
            draw()
 

def draw_outside_border(draw, grid: Grid, animation: bool) -> None:
    for cell in grid[0]:  # top border
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            draw()

    for i in range(grid.total_rows): #right border
        if not grid[i][grid.total_columns - 1].is_start() and not grid[i][grid.total_columns - 1].is_end():
            grid[i][grid.total_columns - 1].make_wall() 
        if animation:
            draw()

    bottom_border = grid[grid.total_rows - 1][:] #bottom border
    bottom_border.reverse()
    for cell in bottom_border:  
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            draw()

    left_border = [grid[i][0] for i in range(grid.total_rows)] #left border
    left_border.reverse()
    for cell in left_border:
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            draw()     



