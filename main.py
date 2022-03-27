import os
from typing import Callable
import maze
import algo
import pygame
import pygame_gui
from grid import Grid, GREY
from cell import Cell
from strenum import StrEnum


# """1:1  cell size = 16px"""
# GRID_SIZE = (50, 50) #(rows, columns)
# GRID_DIMENSIONS = (800, 800) #px

# """21:9  cell size = 20px"""
# GRID_SIZE = (36, 84) #(rows, columns)
# GRID_DIMENSIONS = (1680, 720) #px



WIDTH, HEIGHT = 1291, 765
GRID_WIDTH, GRID_HEIGHT = 1280, 680
GRID_SIZE = (34, 64) #(rows, columns)
GRID_POSITION = ((WIDTH - GRID_WIDTH) / 2 , 40)


GUI_ELEMENT_OFFSET = 20
BG_COLOR = (64, 227, 206)#green
ANIMATION = True

pygame.init()
FPS = 240
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
UI_MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), "gui_theme.json")
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid, UI_MANAGER, time_delta) -> None:
    win.fill(BG_COLOR)
    grid.draw_under_grid_cells()
    grid.draw_grid_lines()
    grid.draw_over_grid_cells()
    UI_MANAGER.update(time_delta)
    
    #grid frame lines
    pygame.draw.line(win, GREY, ((grid.x - 3, grid.y)), (grid.x - 3, grid.y + grid.height), width=5)
    pygame.draw.line(win, GREY, ((grid.x + grid.width + 3, grid.y)), (grid.x + grid.width + 3, grid.y + grid.height), width=5)
    pygame.draw.line(win, GREY, ((0, grid.y - 2)), (WIDTH, grid.y - 2), width=5)
    pygame.draw.line(win, GREY, ((0, grid.y + grid.height + 2)), (WIDTH, grid.y + grid.height + 2), width=5)
    
    UI_MANAGER.draw_ui(WIN)
    pygame.display.update()


class Algorithms(StrEnum):
    ASTAR = "A* Search"
    DIJKSTRA = "Dijkstra's Algorithm"
    DFS = "Depth-first Search" 
    BFS ="Breadth-first Search" 
    GBFS = "Greedy Best-first Search"

class Mazes(StrEnum):
    RECDIV = "Recursive Division Maze"
    RANDOM_DFS = "Randomized Depth-first Search Maze"
    SPIRAL = "Spiral Maze"
 

 
def main() -> None:
    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, (GRID_WIDTH, GRID_HEIGHT), GRID_POSITION)
    
    #scales images to correct cell size
    Cell.scale_cell_imgs(grid.gap, grid.gap)
    
    draw_lambda = lambda: draw(WIN, grid, UI_MANAGER, time_delta)


    #gui elements initialization
    algo_menu = pygame_gui.elements.UIDropDownMenu(
        options_list=[algo for algo in Algorithms],
        starting_option=Algorithms.ASTAR, 
        relative_rect=pygame.Rect((grid.x,  grid.y / 2 - 15), (230, 30)), 
        manager=UI_MANAGER)
    
    visualize_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((algo_menu.get_abs_rect().x + algo_menu.get_abs_rect().width + GUI_ELEMENT_OFFSET, grid.y / 2 - 15), (100, 30)),
        text='Visualize',
        manager=UI_MANAGER,
        object_id='#visualize_button')
    
    maze_menu = pygame_gui.elements.UIDropDownMenu(
        options_list=[maze for maze in Mazes],
        starting_option=Mazes.RECDIV,
        relative_rect=pygame.Rect((visualize_button.get_abs_rect().x +visualize_button.get_abs_rect().width + GUI_ELEMENT_OFFSET,  grid.y / 2 - 15), (305, 30)), 
        manager=UI_MANAGER)
    
    generate_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((maze_menu.get_abs_rect().x + maze_menu.get_abs_rect().width + GUI_ELEMENT_OFFSET,  grid.y / 2 - 15), (100, 30)),
        text='Generate',
        manager=UI_MANAGER)
    
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH - 55,  grid.y / 2 - 15), (50, 30)),
        text='CE',
        manager=UI_MANAGER)

    # legend_lable = pygame_gui.elements.UILabel(
    #     relative_rect=pygame.Rect((grid.x, HEIGHT - 35), (100, 20)),
    #     text="Legend: ",
    #     manager=UI_MANAGER,
    #     object_id="#legend_lable")

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
            if (pygame.mouse.get_pressed()[0] and grid.mouse_on_the_grid() 
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
            elif pygame.mouse.get_pressed()[2] and grid.mouse_on_the_grid():
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_wall():
                    clicked_cell.reset()

            #drag
            if event.type == pygame.MOUSEMOTION and grid.mouse_on_the_grid() and (start_being_dragged or end_being_dragged):
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                if not grid[row][col].is_wall():
                    if start_being_dragged and not grid[row][col].is_end() and algo_visualized:
                        start.reset()
                        start = grid[row][col]
                        start.make_start()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(algo_menu, draw, grid, start, end, animation=False)
                    
                    elif end_being_dragged and not grid[row][col].is_start() and algo_visualized:
                        end.reset()
                        end = grid[row][col]
                        end.make_end()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(algo_menu, draw, grid, start, end, animation=False)
                   
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
                    run_current_algorithm(algo_menu,  draw_lambda, grid, start, end, ANIMATION)
                    algo_visualized = True

                #generate maze gui button
                if event.ui_element == generate_button:
                    grid.clear(start_end_except=True)
                    generate_current_maze(maze_menu,  draw_lambda, grid, start, end, ANIMATION)
                    algo_visualized = False
                 
                #clear the grid gui
                if event.ui_element == clear_button:
                    grid.clear(start_end_except=True)
                    algo_visualized = False
                    
                    start.reset()
                    end.reset()
                    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
                    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
                    start.make_start()
                    end.make_end()


            #visualize algorithm keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    grid.clear(start_end_except=True, barrier_except=True)
                    grid.update_neighbors_for_every_cell()
                    run_current_algorithm(algo_menu,  draw_lambda, grid, start, end, ANIMATION)
                    algo_visualized = True

                #clear the grid keyboard
                if event.key == pygame.K_c:
                    grid.clear(start_end_except=True)
                    algo_visualized = False
                    
                    start.reset()
                    end.reset()
                    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
                    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
                    start.make_start()
                    end.make_end()


                #generate maze keyboard
                if event.key == pygame.K_m:
                    grid.clear(start_end_except=True)
                    generate_current_maze(maze_menu,  draw_lambda, grid, start, end, ANIMATION)
                    algo_visualized = False

    pygame.quit()


# def set_default_position_for_points(start: list, end: list, grid: Grid):
#     start[0].reset()
#     end[0].reset()
#     start[0] = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
#     end[0] = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
#     start[0].make_start()
#     end[0].make_end()
    



def run_current_algorithm(
                        algo_menu: pygame_gui.elements.UIDropDownMenu, 
                        draw: Callable, 
                        grid: Grid, 
                        start: Cell, 
                        end: Cell, 
                        animation: bool) -> None:

    """Calls funcion that visulizes selected algorithm"""

    if algo_menu.selected_option  == Algorithms.ASTAR:
        algo.astar(draw, grid, start, end, animation) 

    elif algo_menu.selected_option  == Algorithms.DIJKSTRA:
        algo.dijkstra(draw, grid, start, end, animation)

    elif algo_menu.selected_option == Algorithms.DFS:
        algo.dfs(draw, grid, start, end, animation)

    elif algo_menu.selected_option == Algorithms.BFS:
        algo.bfs(draw, grid, start, end, animation)

    elif algo_menu.selected_option == Algorithms.GBFS:
        algo.gbfs(draw, grid, start, end, animation)
    
    else: 
        algo.astar(draw, grid, start, end, animation)


def generate_current_maze(
                        maze_menu: pygame_gui.elements.UIDropDownMenu, 
                        draw: Callable, 
                        grid: Grid, 
                        start: Cell, 
                        end: Cell, 
                        animation: bool) -> None:

    """Calls funcion that generates selected maze"""

    if maze_menu.selected_option == Mazes.RECDIV:
        maze.recursive_division_maze_gen(draw, grid, animation)

    elif maze_menu.selected_option == Mazes.RANDOM_DFS:
        maze.random_dfs_maze_gen(draw, (start, end), grid, animation)

    elif maze_menu.selected_option == Mazes.SPIRAL:
        maze.spiral_maze(draw, (start, end), grid, animation)

    else: 
        maze.recursive_division_maze_gen(draw, grid, animation)
        

if __name__ == '__main__':
    main()
