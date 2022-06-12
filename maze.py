import random
import pygame
from grid import Grid
from copy import deepcopy
from utils import aborted
from itertools import cycle


class RoomCoordinates:
    def __init__(self, grid: Grid):
        self.top = 1
        self.bottom = grid.total_rows - 2
        self.left = 1
        self.right = grid.total_columns - 2


def random_dfs_maze_gen(
    win: pygame.surface.Surface, 
    grid: Grid, 
    animation: bool, 
    speed: int = 0
) -> None:
    
    grid.update_neighbors_for_every_cell()
    grid.make_all_cells_wall(start_end_except=True)
    grid.draw_over_grid_lines()
    pygame.display.update()
    start_maze_cell = grid[0][0]
    visited_set = {start_maze_cell}
    stack = [start_maze_cell]
    clock = pygame.time.Clock()

    while len(stack) > 0:
        if aborted():
            return

        current = stack.pop()
        neighbors = [neighbor for neighbor in current.neighbors if neighbor not in visited_set]

        if len(neighbors) > 0:
            random_index = random.randint(0, len(neighbors) - 1)
            for neighbor in neighbors:
                visited_set.add(neighbor)

                if neighbor != neighbors[random_index]:
                    stack.append(neighbor)

            stack.append(neighbors[random_index])
            if (
                not current.is_unvisited()
                and not current.is_start()
                and not current.is_end()
                and not current.is_parcel()
            ):
                current.reset()
                if animation:
                    current.draw(win, animation)
                    pygame.display.update()
                    clock.tick(speed)


def recursive_division_maze_gen(
    win: pygame.surface.Surface, 
    grid: Grid, 
    animation: bool, 
    speed: int = 0
) -> None:
    
    grid.update_neighbors_for_every_cell()
    coordinates = RoomCoordinates(grid)
    draw_outside_border(win, grid, animation, speed)
    recursive_division(win, grid, coordinates, animation, speed)


def recursive_division(
    win: pygame.surface.Surface,
    grid: Grid,
    coordinates: RoomCoordinates,
    animation: bool,
    speed: int = 0,
) -> None:

    if (coordinates.bottom - coordinates.top) < (coordinates.right - coordinates.left):
        horizontal = False
    elif (coordinates.bottom - coordinates.top) > (
        coordinates.right - coordinates.left
    ):
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
        wall_idx = available_idxes[len(available_idxes) // 2]

    build_wall(win, grid, horizontal, wall_idx, coordinates, animation, speed)
    carve_path(win, grid, horizontal, wall_idx, coordinates, animation)

    if horizontal:
        coordinates_copy = deepcopy(coordinates)
        coordinates.top = wall_idx + 1
        recursive_division(win, grid, coordinates, animation, speed)

        coordinates_copy.bottom = wall_idx - 1
        recursive_division(win, grid, coordinates_copy, animation, speed)

    else:
        coordinates_copy = deepcopy(coordinates)
        coordinates.left = wall_idx + 1
        recursive_division(win, grid, coordinates, animation, speed)

        coordinates_copy.right = wall_idx - 1
        recursive_division(win, grid, coordinates_copy, animation, speed)


def get_available_indxes(grid: Grid, coordinates: RoomCoordinates, horizontal: bool) -> list[int]:
    
    """Returns list of valid wall indexes, so future wall wouldn't block exit out of the room
    and wouldn't spawn rigth next to existing wall"""

    available_idxes = []
    if horizontal:
        for i in range(coordinates.top + 1, coordinates.bottom):
            if (
                not grid[i][coordinates.left - 1].is_unvisited()
                and not grid[i][coordinates.right + 1].is_unvisited()
            ):
                available_idxes.append(i)

    else:
        for j in range(coordinates.left + 1, coordinates.right):
            if (
                not grid[coordinates.top - 1][j].is_unvisited()
                and not grid[coordinates.bottom + 1][j].is_unvisited()
            ):
                available_idxes.append(j)

    return available_idxes


def build_wall(
    win: pygame.surface.Surface,
    grid: Grid,
    horizontal: bool,
    index: int,
    coordinates: RoomCoordinates,
    animation: bool,
    speed: int = 0,
) -> None:
    
    """Draws randomly located wall"""

    clock = pygame.time.Clock()

    if horizontal:
        for j in range(coordinates.left, coordinates.right + 1):
            if not grid[index][j].is_start() and not grid[index][j].is_end() and not grid[index][j].is_parcel():
                grid[index][j].make_wall()
            if aborted():
                return
            if animation:
                grid[index][j].draw(win)
                pygame.display.update()
                clock.tick(speed)

    else:
        for i in range(coordinates.top, coordinates.bottom + 1):
            if not grid[i][index].is_start() and not grid[i][index].is_end() and not grid[i][index].is_parcel():
                grid[i][index].make_wall()
            if aborted():
                return
            if animation:
                grid[i][index].draw(win)
                pygame.display.update()
                clock.tick(speed)


def carve_path(
    win: pygame.surface.Surface,
    grid: Grid,
    horizontal: bool,
    index: int,
    coordinates: RoomCoordinates,
    animation: bool,
) -> None:

    """Carves path in randomly located wall"""

    if horizontal:
        rand_idx = random.randint(coordinates.left, coordinates.right)
        if not grid[index][rand_idx].is_start() and not grid[index][rand_idx].is_end() and not grid[index][rand_idx].is_parcel():
            grid[index][rand_idx].reset()
        if animation:
            grid[index][rand_idx].draw(win, animation)
            pygame.display.update()

    else:
        rand_idx = random.randint(coordinates.top, coordinates.bottom)
        if not grid[rand_idx][index].is_start() and not grid[rand_idx][index].is_end() and not grid[rand_idx][index].is_parcel():
            grid[rand_idx][index].reset()
        if animation:
            grid[rand_idx][index].draw(win, animation)
            pygame.display.update()


def draw_outside_border(
    win: pygame.surface.Surface, 
    grid: Grid, 
    animation: bool, 
    speed: int = 0
) -> None:
    
    """Changing color of border cells to wall color"""

    clock = pygame.time.Clock()

    for cell in grid[0]:  # top border
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            cell.draw(win)
            pygame.display.update()
            clock.tick(speed)

    for i in range(grid.total_rows):  # right border
        if (
            not grid[i][grid.total_columns - 1].is_start()
            and not grid[i][grid.total_columns - 1].is_end()
        ):
            grid[i][grid.total_columns - 1].make_wall()
        if animation:
            grid[i][grid.total_columns - 1].draw(win)
            pygame.display.update()
            clock.tick(speed)

    bottom_border = grid[grid.total_rows - 1][:]  # bottom border
    bottom_border.reverse()
    for cell in bottom_border:
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            cell.draw(win)
            pygame.display.update()
            clock.tick(speed)

    left_border = [grid[i][0] for i in range(grid.total_rows)]  # left border
    left_border.reverse()
    for cell in left_border:
        if not cell.is_start() and not cell.is_end():
            cell.make_wall()
        if animation:
            cell.draw(win)
            pygame.display.update()
            clock.tick(speed)


def spiral_maze(
    win: pygame.surface.Surface, 
    grid: Grid, 
    animation: bool, 
    speed: int = 0
) -> None:
    
    grid.update_neighbors_by_direction_for_every_cell()
    grid.make_all_cells_wall(start_end_except=True)
    grid.draw_over_grid_lines()
    current = grid[0][0]
    directions = cycle(["right", "down", "left", "up"])
    if not current.is_start() and not current.is_end():
        current.reset()
    if animation:
        current.draw(win, animation)
        pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        direction = next(directions)

        if current.neighbor_by_direction[direction].is_unvisited():
            current.neighbor_by_direction[next(directions)].make_wall()
            break

        neighbor = None

        while True:

            if aborted():
                return

            current = current.neighbor_by_direction[direction]

            if not current.is_start() and not current.is_end() and not current.is_parcel():
                current.reset()

            neighbor = current.neighbor_by_direction[direction]

            if animation:
                current.draw(win, animation)
                pygame.display.update()
                clock.tick(speed)

            if (
                neighbor.neighbor_by_direction[direction] != None
                and neighbor.neighbor_by_direction[direction].is_unvisited()
            ):
                break
            elif neighbor.neighbor_by_direction[direction] == None:
                break

    for _ in range(max(grid.total_rows, grid.total_columns)):
        i = random.randrange(1, grid.total_rows - 1)
        j = random.randrange(1, grid.total_columns - 1)
        if not grid[i][j].is_start() and not grid[i][j].is_end() and not grid[i][j].is_parcel():
            grid[random.randrange(1, grid.total_rows - 1)][
                random.randrange(1, grid.total_columns - 1)
            ].reset()

    if (
        not grid[grid.total_rows - 1][1].is_start()
        and not grid[grid.total_rows - 1][1].is_end()
    ):
        grid[grid.total_rows - 1][1].reset()

    if (
        not grid[grid.total_rows - 1][grid.total_columns - 2].is_start()
        and not grid[grid.total_rows - 1][grid.total_columns - 2].is_end()
    ):
        grid[grid.total_rows - 1][grid.total_columns - 2].reset()

    grid.draw_over_grid_lines()


def stair_pattern_maze(
    win: pygame.surface.Surface, 
    grid: Grid, 
    animation: bool, 
    speed: int = 0
) -> None:
    grid.update_neighbors_by_direction_for_every_cell()
    grid.draw_over_grid_lines()

    row = grid.total_rows - 1
    col = 0

    current_cell = grid[row][col]

    direction_flag = True

    clock = pygame.time.Clock()

    while (col != grid.total_columns - 2):
        
        if aborted():
            return
        
        if direction_flag:
            row -= 1
        else: 
            row += 1

        col += 1
        
        if row == 0:
            direction_flag = False
        elif row == grid.total_rows - 1 and col != 0:
            direction_flag = True
        
        current_cell = grid[row][col]
        current_cell.make_wall()

        if animation:
            current_cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)

        
    

    


