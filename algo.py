from grid import Grid
from queue import PriorityQueue, Queue
from utils import aborted, Heuristic


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
            current_cell.make_closed()
        
        for neighbor in current_cell.neighbors:
            if neighbor not in visited:
                count += 1
                if neighbor.is_end():
                    path = []
                    path.append(current_cell)
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


