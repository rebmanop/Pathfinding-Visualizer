import pygame
from queue import PriorityQueue
import random


def heuristic(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw) -> None: 
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        
    path.reverse()
    path.pop(0)
    return path


def animate_path(draw, path):
    
    for cell in path:
        cell.make_path()
        draw()
        pygame.time.wait(10)

    
def astar(draw, grid, start, end) -> None:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            path = reconstruct_path(came_from, current, draw)
            animate_path(draw, path)
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

        draw()

        if current != start:
            current.make_closed()

   

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0
    came_from = {}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        
        if current == end:
            path = reconstruct_path(came_from, current, draw)
            animate_path(draw, path)
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

        draw()

        if current != start:
            current.make_closed()



def dfs(draw, grid, start, end):
    marked = {spot: False for row in grid for spot in row}
    stack = [start]
    while len(stack) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        if current == end:
            return

        current = stack.pop()
        if not marked[current]:
            marked[current] = True
            for neighbor in current.neighbors:
                if not marked[neighbor]:
                    stack.append(neighbor)

        
        draw()

        if current != start:
                current.make_closed()


"""
def generate_maze_dfs(draw, grid, start, end):
    marked = {spot: False for row in grid for spot in row}
    stack = [start]
    visited_nodes_set = set()
    while len(stack) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        
        current = stack.pop()
        random.shuffle(current.neighbors)
        random_index = random.randint(0, len(current.neighbors) - 1)
        if current 
                if not marked[neighbor]:


        
        
        draw()

"""