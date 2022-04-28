from typing import Type
import pygame
from cell import Cell
from grid import Grid
from utils import aborted, Heuristic
from queue import PriorityQueue, Queue

PATH_ANIMATION_SPEED = 100


def reconstruct_path(came_from: dict, current: Cell) -> list[Cell]:
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)

    # reverse the path list, so animation would be from the start cell
    path.reverse()

    # pop start cell from the path list, so animation wouldn't redraw it
    if len(path) != 0:
        path.pop(0)

    return path


def reconstruct_path_bbfs(came_from: dict, current: Cell) -> list[Cell]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.pop()

    return path


def can_redraw(cell: Cell) -> bool:
    if not cell.is_path() and not cell.is_end() and not cell.is_start() and not cell.is_parcel():
        return True
    else:
        return False


def animate_path(
    win: pygame.surface.Surface, path: list[Cell], grid: Grid, animation: bool
) -> None:
    reset_opened_cells(grid, win, animation)
    clock = pygame.time.Clock()
    for cell in path:
        if aborted():
            return
        if not cell.is_end() and not cell.is_start() and not cell.is_parcel():
            cell.make_path()
        if animation:
            cell.draw(win, animation)
            pygame.display.update()
            clock.tick(PATH_ANIMATION_SPEED)


def reset_opened_cells(grid: Grid, win: pygame.surface.Surface, animation: bool):
    for row in grid.raw_grid:
        for cell in row:
            if cell.is_open():
                cell.reset()
                cell.draw(win, animation)


def astar(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
) -> list[Cell]:
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    f_score[start] = Heuristic.manhattan(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    clock = pygame.time.Clock()

    while not open_set.empty():
        cells_to_redraw = []
        if aborted():
            return

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, current)
            return path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + Heuristic.manhattan(
                    neighbor.get_pos(), end.get_pos()
                )

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end and can_redraw(neighbor):
                        neighbor.make_open()
                        cells_to_redraw.append(neighbor)

        if current != start and can_redraw(current):
            current.visit()
            cells_to_redraw.append(current)

        if animation:
            for cell in cells_to_redraw:
                cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)




def dijkstra(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
) -> list[Cell]:
    
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    open_set_hash = {start}
    distance = {cell: float("inf") for row in grid.raw_grid for cell in row}
    distance[start] = 0
    came_from = {}
    clock = pygame.time.Clock()

    while not open_set.empty():
        cells_to_redraw = []

        if aborted():
            return

        current: Cell = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, current)
            return path

        for neighbor in current.neighbors:
            alt_distance = distance[current] + 1
            if alt_distance < distance[neighbor]:
                distance[neighbor] = alt_distance
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((alt_distance, count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end and can_redraw(neighbor):
                        neighbor.make_open() 
                        cells_to_redraw.append(neighbor)

        if current != start and can_redraw(current):
            current.visit()
            cells_to_redraw.append(current)

        if animation:
            for cell in cells_to_redraw:
                cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)


def dfs(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
) -> list[Cell]:
    marked = {cell: False for row in grid.raw_grid for cell in row}
    stack = [start]
    came_from = {}
    clock = pygame.time.Clock()
    while len(stack) > 0:

        if aborted():
            return

        current = stack.pop()

        if current == end:
            path = reconstruct_path(came_from, current)
            return path

        if not marked[current]:
            marked[current] = True
            for neighbor in current.neighbors:
                if not marked[neighbor]:
                    stack.append(neighbor)
                    came_from[neighbor] = current
                    if current != start and not current.is_visited() and animation and can_redraw(current):
                        current.make_open()
                        current.draw(win, animation)
                        pygame.display.update()

        if current != start and not current.is_visited() and animation and can_redraw(current):
            current.visit()
            current.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)

        if current != start and can_redraw(current):
            current.visit()


def bfs(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
) -> list[Cell]:
    queue = Queue()
    explored = {start}
    queue.put(start)
    came_from = {}
    clock = pygame.time.Clock()
    while not queue.empty():
        cells_to_redraw = []

        if aborted():
            return

        current = queue.get()

        if current == end:
            path = reconstruct_path(came_from, current)
            return path

        for neighbor in current.neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                queue.put(neighbor)
                came_from[neighbor] = current
                if neighbor != end and can_redraw(neighbor):
                    neighbor.make_open()
                    cells_to_redraw.append(neighbor)

        if current != start and can_redraw(current):
            current.visit()
            cells_to_redraw.append(current)

        if animation:
            for cell in cells_to_redraw:
                cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)


def bidirectional_bfs(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
) -> list[Cell]:
    Qf = Queue()
    Qb = Queue()
    explored_forward = {start}
    explored_backwards = {end}
    Qf.put(start)
    Qb.put(end)
    came_from_forward = {}
    came_from_backwards = {}
    clock = pygame.time.Clock()

    while not Qf.empty() and not Qb.empty():

        cells_to_redraw = []
        if aborted():
            return

        u = Qf.get()
        v = Qb.get()

        if u in explored_backwards:
            path = reconstruct_path(came_from_forward, u) + reconstruct_path_bbfs(came_from_backwards, u)
            return path

        for neighbor in u.neighbors:
            if neighbor not in explored_forward:
                explored_forward.add(neighbor)
                Qf.put(neighbor)
                came_from_forward[neighbor] = u
                if neighbor != end and neighbor != start and can_redraw(neighbor):
                    neighbor.make_open()
                    cells_to_redraw.append(neighbor)

        for neighbor in v.neighbors:
            if neighbor not in explored_backwards:
                explored_backwards.add(neighbor)
                Qb.put(neighbor)
                came_from_backwards[neighbor] = v
                if neighbor != end and neighbor != start and can_redraw(neighbor):
                    neighbor.make_open()
                    cells_to_redraw.append(neighbor)

        if u != start and u != end and can_redraw(u):
            u.visit()
            cells_to_redraw.append(u)

        if v != end and v != start and can_redraw(v):
            v.visit()
            cells_to_redraw.append(v)

        if animation:
            for cell in cells_to_redraw:
                cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)


def gbfs(
    win: pygame.surface.Surface,
    grid: Grid,
    start: Cell,
    end: Cell,
    animation: bool,
    speed: int = 0,
)-> list[Cell]:

    queue = PriorityQueue()
    visited = {start}
    came_from = {}
    count = 0
    queue.put((Heuristic.manhattan(start.get_pos(), end.get_pos()), count, start))
    clock = pygame.time.Clock()
    while not queue.empty():
        cells_to_redraw = []

        if aborted():
            return

        current_cell = queue.get()[2]

        if current_cell != start and can_redraw(current_cell):
            current_cell.visit()
            cells_to_redraw.append(current_cell)

        for neighbor in current_cell.neighbors:
            if neighbor not in visited:
                count += 1
                if neighbor.is_end() or neighbor.is_parcel():
                    path = [current_cell]
                    while current_cell in came_from:
                        current_cell = came_from[current_cell]
                        path.append(current_cell)
                    path.reverse()
                    path.pop(0)
                    return path

                else:
                    came_from[neighbor] = current_cell
                    visited.add(neighbor)
                    queue.put((Heuristic.manhattan(neighbor.get_pos(), end.get_pos()), count, neighbor))
                    if neighbor != start and can_redraw(neighbor):
                        neighbor.make_open()
                        cells_to_redraw.append(neighbor)

        if animation:
            for cell in cells_to_redraw:
                cell.draw(win, animation)
            pygame.display.update()
            clock.tick(speed)