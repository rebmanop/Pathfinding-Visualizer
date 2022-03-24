import os
import maze
import algo
import pygame
import pygame_gui
from grid import Grid
from cell import Cell
from enum import Enum
from pygame_gui.core import ObjectID


# """1:1  cell size = 16px"""
# GRID_SIZE = (50, 50) #(rows, columns)
# GRID_DIMENSIONS = (800, 800) #px

# """21:9  cell size = 20px"""
# GRID_SIZE = (36, 84) #(rows, columns)
# GRID_DIMENSIONS = (1680, 720) #px

"""16:9  cell size = 20px""" 

GRID_SIZE = (36, 64) #(rows, columns)
GRID_DIMENSIONS = (1280, 720) #px
GRID_POSITION = (0, 40)

WIDTH, HEIGHT = 1280, 760
WINDOW_DIMENSIONS = (WIDTH, HEIGHT) #px  


BG_COLOR = (134, 232, 255)#blue sky
ANIMATION = True

pygame.init()
FPS = 240
WIN = pygame.display.set_mode(WINDOW_DIMENSIONS)
UI_MANAGER = pygame_gui.UIManager(WINDOW_DIMENSIONS, "gui_theme.json")
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid, ui_manager, time_delta) -> None:
    win.fill(BG_COLOR)
    grid.draw_under_grid_cells()
    grid.draw_grid_lines()
    grid.draw_over_grid_cells()
    ui_manager.update(time_delta)
    ui_manager.draw_ui(WIN)
    pygame.display.update()


def mouse_on_the_grid() -> bool:
    mpos = pygame.mouse.get_pos()
    if (mpos[0] > GRID_POSITION[0] and mpos[0] < (GRID_POSITION[0] + GRID_DIMENSIONS[0]) 
    and mpos[1] > GRID_POSITION[1] and mpos[1] < (GRID_POSITION[1] + GRID_DIMENSIONS[1])):
        return True
    else:
        return False


class Algorithms(Enum):
    ASTAR = "A* Search"
    DIJKSTRA = "Dijkstra's Algorithm"
    DFS = "Depth-first Search" 
    BFS ="Breadth-first Search" 
    GBFS = "Greedy Best-first Search"

class Mazes(Enum):
    RECDIV = "Recursive Division Maze"
    RANDOM_DFS = "Randomized Depth-first Search Maze"
    SPIRAL = "Spiral Maze"

 
def main() -> None:
    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, GRID_DIMENSIONS, GRID_POSITION)
    Cell.init_cell_imgs((grid.gap, grid.gap))
    

    visualize_button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((5 + 230 + 20, 11), (100, 30)),
                        text='Visualize',
                        manager=UI_MANAGER,
                        object_id=ObjectID(object_id='#visualize_button'))



    generate_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((5 + 250 + 20 + 100 + 305 + 20, 11), (100, 30)),
                    text='Generate',
                    manager=UI_MANAGER)

    clear_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((WIDTH - 55, 11), (50, 30)),
                    text='CE',
                    manager=UI_MANAGER)



    algo_menu = pygame_gui.elements.UIDropDownMenu(
    [Algorithms.ASTAR.value, Algorithms.DIJKSTRA.value, Algorithms.DFS.value, Algorithms.BFS.value, Algorithms.GBFS.value],
    Algorithms.ASTAR.value, pygame.Rect((5,  11), (230, 30)), 
    UI_MANAGER)
    
    maze_menu = pygame_gui.elements.UIDropDownMenu(
        [Mazes.RECDIV.value, Mazes.RANDOM_DFS.value, Mazes.SPIRAL.value],
        Mazes.RECDIV.value,
        pygame.Rect((5 + 250 + 20 + 100,  11), (305, 30)), 
        UI_MANAGER)
    
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
        time_delta = clock.tick(FPS)/1000.0
        draw(WIN, grid, UI_MANAGER, time_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            UI_MANAGER.process_events(event)


                        
            #if left mouse button clicked
            if (pygame.mouse.get_pressed()[0] and mouse_on_the_grid() 
            and algo_menu.menu_states["closed"] == algo_menu.current_state and maze_menu.menu_states["closed"] == maze_menu.current_state):
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
            elif pygame.mouse.get_pressed()[2] and mouse_on_the_grid():
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_wall():
                    clicked_cell.reset()

            #drag
            if event.type == pygame.MOUSEMOTION and mouse_on_the_grid() and (start_being_dragged or end_being_dragged):
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                if not grid[row][col].is_wall():
                    if start_being_dragged and not grid[row][col].is_end() and algo_visualized:
                        start.reset()
                        start = grid[row][col]
                        start.make_start()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(algo_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, animation=False)
                    
                    elif end_being_dragged and not grid[row][col].is_start() and algo_visualized:
                        end.reset()
                        end = grid[row][col]
                        end.make_end()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(algo_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, animation=False)
                   
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
                
            #visualize algorithm gui button
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == visualize_button:
                    grid.clear(start_end_except=True, barrier_except=True)
                    grid.update_neighbors_for_every_cell()
                    run_current_algorithm(algo_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, ANIMATION)
                    algo_visualized = True

                #generate maze gui button
                if event.ui_element == generate_button:
                    grid.clear(start_end_except=True)
                    generate_current_maze(maze_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, ANIMATION)
                    algo_visualized = False
                 
                #clear the grid gui
                if event.ui_element == clear_button:
                    grid.clear(start_end_except=True)
                    algo_visualized = False


            #visualize algorithm keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    grid.clear(start_end_except=True, barrier_except=True)
                    grid.update_neighbors_for_every_cell()
                    run_current_algorithm(algo_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, ANIMATION)
                    algo_visualized = True

                #clear the grid keyboard
                if event.key == pygame.K_c:
                    grid.clear(start_end_except=True)
                    algo_visualized = False

                #generate maze keyboard
                if event.key == pygame.K_m:
                    grid.clear(start_end_except=True)
                    generate_current_maze(maze_menu, lambda: draw(WIN, grid, UI_MANAGER, time_delta), grid, start, end, ANIMATION)
                    algo_visualized = False



                   

    pygame.quit()


def run_current_algorithm(algo_menu, draw, grid, start, end, animation: bool) -> None:
    if algo_menu.selected_option  == Algorithms.ASTAR.value:
        algo.astar(draw, grid, start, end, animation)

    elif algo_menu.selected_option  == Algorithms.DIJKSTRA.value:
        algo.dijkstra(draw, grid, start, end, animation)

    elif algo_menu.selected_option  == Algorithms.DFS.value:
        algo.dfs(draw, grid, start, end, animation)

    elif algo_menu.selected_option  == Algorithms.BFS.value:
        algo.bfs(draw, grid, start, end, animation)

    elif algo_menu.selected_option  == Algorithms.GBFS.value:
        algo.gbfs(draw, grid, start, end, animation)
    
    else: 
        algo.astar(draw, grid, start, end, animation)


def generate_current_maze(maze_menu, draw, grid, start, end, animation: bool) -> None:
    if maze_menu.selected_option  == Mazes.RECDIV.value:
        maze.recursive_division_maze_gen(draw, grid, animation)

    elif maze_menu.selected_option  == Mazes.RANDOM_DFS.value:
        maze.random_dfs_maze_gen(draw, (start, end), grid, animation)

    elif maze_menu.selected_option  == Mazes.SPIRAL.value:
        maze.spiral_maze(draw, (start, end), grid, animation)

    else: 
        maze.recursive_division_maze_gen(draw, grid, animation)

        

if __name__ == '__main__':
    main()
