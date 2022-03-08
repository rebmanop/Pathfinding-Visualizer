import os
import maze
import algo
import pygame
from grid import Grid
from cell import Cell
from enum import Enum, auto


# """1:1  cell size = 16px"""
# GRID_SIZE = (50, 50) #(rows, columns)
# GRID_DIMENSIONS = (800, 800) #px

# """21:9  cell size = 20px"""
# GRID_SIZE = (36, 84) #(rows, columns)
# GRID_DIMENSIONS = (1680, 720) #px

"""16:9  cell size = 20px""" 
GRID_SIZE = (36, 64) #(rows, columns)
GRID_DIMENSIONS = (1280, 720) #px  


ANIMATION = True


WIN = pygame.display.set_mode(GRID_DIMENSIONS)
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid) -> None:
    win.fill(pygame.Color('white'))
    grid.draw_under_grid_cells()
    grid.draw_grid_lines()
    grid.draw_over_grid_cells()
    pygame.display.update()


class CurrentAlgorithm(Enum):
    ASTAR = auto()
    DIJKSTRA = auto()
    DFS = auto() 
    BFS = auto() 
    GBFS = auto()

 
def main() -> None:
    grid = Grid(WIN, GRID_SIZE, GRID_DIMENSIONS)
    Cell.init_cell_imgs((grid.gap, grid.gap))
    current_algorithm = CurrentAlgorithm(CurrentAlgorithm.DIJKSTRA)

    #set start and end default positions
    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
    start.make_start()
    end.make_end()


    running = True
    start_being_dragged = False
    end_being_dragged = False
    algo_visualized = False


    while running:
        draw(WIN, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #if left mouse button clicked
            if pygame.mouse.get_pressed()[0]:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell != end and clicked_cell != start and not start_being_dragged and not end_being_dragged:
                    clicked_cell.make_wall()

                elif clicked_cell.is_start():
                    start_being_dragged = True 

                elif clicked_cell.is_end():
                    end_being_dragged = True


            #if right mouse button clicked
            elif pygame.mouse.get_pressed()[2]:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_wall():
                    clicked_cell.reset()

            #drag
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                if not grid[row][col].is_wall():
                    
                    if start_being_dragged and not grid[row][col].is_end() and algo_visualized:
                        start.reset()
                        start = grid[row][col]
                        start.make_start()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(current_algorithm, lambda: draw(WIN, grid), grid, start, end, animation=False)

                    
                    elif end_being_dragged and not grid[row][col].is_start() and algo_visualized:
                        end.reset()
                        end = grid[row][col]
                        end.make_end()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(current_algorithm, lambda: draw(WIN, grid), grid, start, end, animation=False)


                    
                    elif start_being_dragged and not grid[row][col].is_end():
                        start.reset()
                        start = grid[row][col]
                        start.make_start()
                
                    elif end_being_dragged and not grid[row][col].is_start():
                        end.reset()
                        end = grid[row][col]
                        end.make_end()


            #drop
            if event.type == pygame.MOUSEBUTTONUP:
                start_being_dragged = False
                end_being_dragged = False
                

            #visualize algorithm 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    grid.clear(start_end_except=True, barrier_except=True)
                    grid.update_neighbors_for_every_cell()
                    run_current_algorithm(current_algorithm, lambda: draw(WIN, grid), grid, start, end, ANIMATION)
                    algo_visualized = True

                #clear the grid
                if event.key == pygame.K_c:
                    grid.clear(start_end_except=True)
                    algo_visualized = False

                #generate recursive division maze
                if event.key == pygame.K_m:
                    grid.clear(start_end_except=True)
                    grid.update_neighbors_for_every_cell()
                    maze.recursive_division_maze_gen(lambda: draw(WIN, grid), grid, ANIMATION)
                    algo_visualized = False

                #generate random dfs maze
                if event.key == pygame.K_n:
                    grid.clear(start_end_except=True)
                    grid.update_neighbors_for_every_cell()
                    maze.random_dfs_maze_gen(lambda: draw(WIN, grid), (start, end), grid, ANIMATION)
                    algo_visualized = False

                   

    pygame.quit()


def run_current_algorithm(current_alorithm: CurrentAlgorithm, draw, grid, start, end, animation: bool):
    if current_alorithm.value == CurrentAlgorithm.ASTAR.value:
        algo.astar(draw, grid, start, end, animation)

    elif current_alorithm.value == CurrentAlgorithm.DIJKSTRA.value:
        algo.dijkstra(draw, grid, start, end, animation)

    elif current_alorithm.value == CurrentAlgorithm.DFS.value:
        algo.dfs(draw, grid, start, end, animation)

    elif current_alorithm.value == CurrentAlgorithm.BFS.value:
        algo.bfs(draw, grid, start, end, animation)

    elif current_alorithm.value == CurrentAlgorithm.GBFS.value:
        algo.gbfs(draw, grid, start, end, animation)
        
        

if __name__ == '__main__':
    main()
