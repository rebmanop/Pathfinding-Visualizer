import random
import pygame
from grid import Grid
from copy import deepcopy
from queue import PriorityQueue, Queue

def aborted() -> bool:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True


def reconstruct_path(came_from, current) -> list: 
    path = []
    
    while current in came_from:
        current = came_from[current]
        path.append(current)

    #reverse the path list, so animation would be from the start cell
    path.reverse() 

    #pop start cell from the path list, so animation wouldn't redraw it 
    path.pop(0) 
    
    return path


def animate_path(draw, path, grid, animation: bool) -> None:
    reset_opened_cells(draw, grid, animation)

    for cell in path:
        if aborted():
            return
        cell.make_path()
        if animation:
            draw()
        #pygame.time.wait(10)


def reset_opened_cells(draw, grid, animation: bool):
    for row in grid.raw_grid: 
        for cell in row:
            if cell.is_open():
                cell.reset()
                if animation:
                    draw()


def heuristic(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def astar(draw, grid, start, end, animation: bool) -> None:
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        if aborted():
            return

        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            path = reconstruct_path(came_from, current)
            animate_path(draw, path, grid, animation)
            return

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

        if animation:
            draw()

        if current != start:
            current.make_closed()

   
def dijkstra(draw, grid, start, end, animation: bool) -> None:
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    open_set_hash = {start}
    distance = {cell: float("inf") for row in grid.raw_grid for cell in row}
    distance[start] = 0
    came_from = {}

    while not open_set.empty():
        if aborted():
            return


        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        
        if current == end:
            path = reconstruct_path(came_from, current)
            animate_path(draw, path, grid, animation)
            return
        

        for neighbor in current.neighbors:
            alt_distance = distance[current] + 1
            if alt_distance < distance[neighbor]:
                distance[neighbor] = alt_distance
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((alt_distance, count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()
        
        if animation:
            draw()

        if current != start:
            current.make_closed()


def dfs(draw, grid, start, end, animation) -> None:
    marked = {cell: False for row in grid.raw_grid for cell in row}
    stack = [start]
    came_from = {}
    while len(stack) > 0:
        if aborted():
            return

        current = stack.pop()
        
        if current == end:
            path = reconstruct_path(came_from, current)
            animate_path(draw, path, grid, animation)
            return

        if not marked[current]:
            marked[current] = True
            for neighbor in current.neighbors:
                if not marked[neighbor]:
                    stack.append(neighbor)
                    came_from[neighbor] = current
                    if current != start:
                        current.make_open()

        if animation:
            draw()

        if current != start:
                current.make_closed()


def bfs(draw, grid, start, end, animation: bool)  -> None:
    queue = Queue()
    explored = {start}
    queue.put(start)
    came_from = {}
        
    while not queue.empty():
        if aborted():
            return
        
        current = queue.get()
        
        if current == end:
            path: list = reconstruct_path(came_from, current)
            animate_path(draw, path, grid, animation)
            return
        
        for neighbor in current.neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                queue.put(neighbor)
                came_from[neighbor] = current
                if neighbor != end:
                    neighbor.make_open()
                
        if animation:
            draw()

        if current != start:
            current.make_closed()

    