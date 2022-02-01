import random
from this import d
import pygame
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
            path: list = reconstruct_path(came_from, current)
            animate_path(draw, path, grid)
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
            path: list = reconstruct_path(came_from, current)
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


def dfs(draw, grid, start, end) -> None:
    marked = {cell: False for row in grid.raw_grid for cell in row}
    stack = [start]
    came_from = {}
    while len(stack) > 0:
        if aborted():
            return

        current = stack.pop()
        
        if current == end:
            path: list = reconstruct_path(came_from, current)
            animate_path(draw, path, grid)
            return

        if not marked[current]:
            marked[current] = True
            for neighbor in current.neighbors:
                if not marked[neighbor]:
                    stack.append(neighbor)
                    came_from[neighbor] = current
                    if current != start:
                        current.make_open()

        
        draw()

        if current != start:
                current.make_closed()


def random_dfs_maze_gen(draw, start, grid) -> None:    
    grid.make_all_cells_barrier()
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
            if not current.is_reset():
                current.reset()
           
        draw()
        

def bfs(draw, grid, start, end):
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
            animate_path(draw, path, grid)
            return
        
        for neighbor in current.neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                queue.put(neighbor)
                came_from[neighbor] = current
                if neighbor != end:
                    neighbor.make_open()
                
        
        draw()

        if current != start:
            current.make_closed()


def recursive_division_maze_gen(draw, start, grid, animation):
    _ = start
    
    top = 0
    buttom = grid.total_rows - 1
    left = 0
    right = grid.total_rows - 1 

    recursive_division(draw, grid, buttom, top, left, right, animation)


def recursive_division(draw, grid, buttom, top, left, right, animation):

    if (buttom - top) < 2 or (right - left) < 2:
        return

    horizontal = random.choice([True, False])


    wall_idx = random.randint(top + 1, buttom - 1) if horizontal else random.randint(left + 1, right - 1)
    build_wall(draw, grid, horizontal, wall_idx, buttom, top, left, right, animation)
    carve_path(draw, grid, horizontal, wall_idx, buttom, top, left, right, animation)
    
    if horizontal:
        recursive_division(draw, grid, buttom, wall_idx + 1, left, right, animation)
        recursive_division(draw, grid, wall_idx - 1, top, left, right,  animation)

    else:
        recursive_division(draw, grid, buttom, top, wall_idx + 1, right,  animation)
        recursive_division(draw, grid, buttom, top, left, wall_idx - 1,  animation)
    
 
def build_wall(draw, grid, horizontal: bool, index,  buttom, top, left, right, animation: bool):
    if horizontal:
        for j in range(left, right + 1):
            grid[index][j].make_barrier()
            if animation:
                draw()
    
    else:
        for i in range(top, buttom + 1):
            grid[i][index].make_barrier()
            if animation:
                draw()
            

def carve_path(draw, grid, horizontal: bool, index,  buttom, top, left, right, animation: bool):
    if horizontal :
        if ((left - 1 >= 0) and grid[index][left - 1].is_reset()) and ((right + 1) <= (grid.total_rows - 1) and grid[index][right + 1].is_reset()):
            grid[index][left].reset()
            grid[index][right].reset()
        
        elif (left - 1 >= 0) and grid[index][left - 1].is_reset():
            grid[index][left].reset()

        elif (right + 1) <= (grid.total_rows - 1) and grid[index][right + 1].is_reset():
            grid[index][right].reset()

        else:
            rand_idx = random.randint(left, right)
            grid[index][rand_idx].reset()
            
        if animation:
            draw()

    else:
        if ((buttom + 1) <= (grid.total_rows - 1) and grid[buttom + 1][index].is_reset()) and ((top - 1) >= 0 and grid[top - 1][index].is_reset()):
            grid[buttom][index].reset()
            grid[top][index].reset()

        elif (top - 1) >= 0 and grid[top - 1][index].is_reset():
            grid[top][index].reset()

        elif (buttom + 1) <= (grid.total_rows - 1) and grid[buttom + 1][index].is_reset():
            grid[buttom][index].reset()

        else:
            rand_idx = random.randint(top, buttom)
            grid[rand_idx][index].reset()
        
        if animation:
            draw()
 

def draw_border(draw, grid):
    for i, row in enumerate(grid.raw_grid):
        for j, cell in enumerate(row):
            if aborted():
                return
            if i == 0 or i == grid.total_rows - 1 or j == 0 or j == grid.total_rows - 1:
                cell.make_barrier()
                draw()
