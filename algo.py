from operator import ne
from cell import Cell
from grid import Grid
from queue import PriorityQueue, Queue
from utils import aborted, Heuristic
import pygame


def reconstruct_path(came_from, current) -> list[Cell]: 
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)

    #reverse the path list, so animation would be from the start cell
    path.reverse() 

    #pop start cell from the path list, so animation wouldn't redraw it 
    if len(path) != 0:
        path.pop(0) 
    
    return path


def reconstruct_path_bbfs(came_from, current) -> list[Cell]: 
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.pop() 
    
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
                # if animation:
                #     draw()


def astar(draw, grid, start, end, animation: bool) -> None:
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid.raw_grid for cell in row}
    f_score[start] = Heuristic.manhattan(start.get_pos(), end.get_pos())

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
                f_score[neighbor] = temp_g_score + Heuristic.manhattan(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

        if animation:
            draw()

        if current != start:
            current.visit()

   
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
            current.visit()



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

        if animation and not current.is_visited():
            draw()

        if current != start:
                current.visit()


def bfs(draw, grid, start, end, animation: bool)  -> None:
    queue = Queue()
    explored = {start}
    queue.put(start)
    came_from = {}
    clock = pygame.time.Clock()
    draw()
    while not queue.empty():
        clock.tick(600)
        
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
                    neighbor.draw(grid.win, True)

                
        # if animation:
        #     draw()

        if current != start:
            current.visit()
            current.draw(grid.win, True)

        
        pygame.display.update()


        


def bidirectional_bfs(draw, grid, start, end, animation: bool)  -> None:
    Qf = Queue()
    Qb = Queue()
    explored_forward = {start}
    explored_backwards = {end}
    Qf.put(start)
    Qb.put(end)
    came_from_forward = {}
    came_from_backwards = {}
        
    while not Qf.empty() and not Qb.empty():
        if aborted():
            return
        
        u = Qf.get()
        v = Qb.get()

        if u in explored_backwards:
            path: list[Cell] = reconstruct_path(came_from_forward, u) + reconstruct_path_bbfs(came_from_backwards, u)
            animate_path(draw, path, grid, animation)
            return
        
        for neighbor in u.neighbors:
            if neighbor not in explored_forward:
                explored_forward.add(neighbor)
                Qf.put(neighbor)
                came_from_forward[neighbor] = u
                if neighbor != end and neighbor != start:
                    neighbor.make_open()

        for neighbor in v.neighbors:
            if neighbor not in explored_backwards:
                explored_backwards.add(neighbor)
                Qb.put(neighbor)
                came_from_backwards[neighbor] = v
                if neighbor != end and neighbor != start:
                    neighbor.make_open()
                
        if animation:
            draw()

        if u != start and u != end:
            u.visit()
        
        if v != end and v != start:
            v.visit()
            

def gbfs(draw, grid: Grid, start, end, animation: bool):
    queue = PriorityQueue()
    visited = {start}
    came_from = {}
    count = 0
    queue.put((Heuristic.manhattan(start.get_pos(), end.get_pos()), count,start))

    while not queue.empty():
        if aborted():
            return

        current_cell = queue.get()[2]

        if current_cell != start:
            current_cell.visit()
        
        for neighbor in current_cell.neighbors:
            if neighbor not in visited:
                count += 1
                if neighbor.is_end():
                    path = [current_cell]
                    while current_cell in came_from:
                        current_cell = came_from[current_cell]
                        path.append(current_cell)
                    path.reverse() 
                    path.pop(0) 
                    animate_path(draw, path, grid, animation)
                    return

                else:
                    came_from[neighbor] = current_cell
                    visited.add(neighbor)
                    queue.put((Heuristic.manhattan(neighbor.get_pos(), end.get_pos()), count, neighbor))
                    if  neighbor != start:
                        neighbor.make_open()

          
        if animation:
            draw()



