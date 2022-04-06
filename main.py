import os
import maze
import algo
import cell
import pygame
import pygame_gui
from typing import Callable
from strenum import StrEnum
from grid import Grid, GREY
from legend_cell import LegendCell
from pygame_gui.core import ObjectID


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


def draw(win, grid, UI_MANAGER, time_delta, legend_cells) -> None:
    win.fill(BG_COLOR)
    grid.draw_under_grid_lines()
    grid.draw_grid_lines()
    grid.draw_over_grid_lines()
    UI_MANAGER.update(time_delta)
    grid.draw_grid_frame()

    for legend_cell in legend_cells:
        legend_cell.draw_legend_cell()
    
    UI_MANAGER.draw_ui(WIN)
    pygame.display.update()


class Algorithms(StrEnum):
    ASTAR = "A* Search"
    DIJKSTRA = "Dijkstra's Algorithm"
    DFS = "Depth-first Search" 
    BFS ="Breadth-first Search" 
    GBFS = "Greedy Best-first Search"
    BBFS = "Bidirectional BFS"

class Mazes(StrEnum):
    RECDIV = "Recursive Division Maze"
    RANDOM_DFS = "Randomized Depth-first Search Maze"
    SPIRAL = "Spiral Maze"

 
def main() -> None:
    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, (GRID_WIDTH, GRID_HEIGHT), GRID_POSITION)
    
    #scales images to correct cell size
    cell.Cell.scale_cell_imgs(grid.gap, grid.gap)
    
    draw_lambda = lambda: draw(WIN, grid, UI_MANAGER, time_delta, legend_cells)

    animation_speed = 250


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

    unvisited_cell_lable = pygame_gui.elements.UILabel(
         relative_rect=pygame.Rect((grid.x + grid.gap, HEIGHT - 35), (130, grid.gap)),
         text="-unvisited cell",
         manager=UI_MANAGER,
         object_id=ObjectID(class_id="@legend_cell_lables"))

    visited_cell_lable = pygame_gui.elements.UILabel(
         relative_rect=pygame.Rect((grid.x + 200 + grid.gap, HEIGHT - 35), (115, grid.gap)),
         text="-visited cell",
         manager=UI_MANAGER,
         object_id=ObjectID(class_id="@legend_cell_lables"))

    open_cell_lable = pygame_gui.elements.UILabel(
         relative_rect=pygame.Rect((grid.x + 400 + grid.gap, HEIGHT - 35), (90, grid.gap)),
         text="-open cell",
         manager=UI_MANAGER,
         object_id=ObjectID(class_id="@legend_cell_lables"))

    path_cell_lable = pygame_gui.elements.UILabel(
         relative_rect=pygame.Rect((grid.x + 600 + grid.gap, HEIGHT - 35), (90, grid.gap)),
         text="-path cell",
         manager=UI_MANAGER,
         object_id=ObjectID(class_id="@legend_cell_lables"))

    wall_cell_lable = pygame_gui.elements.UILabel(
         relative_rect=pygame.Rect((grid.x + 800 + grid.gap, HEIGHT - 35), (90, grid.gap)),
         text="-wall cell",
         manager=UI_MANAGER,
         object_id=ObjectID(class_id="@legend_cell_lables"))

    legend_cells = [
        LegendCell(WIN, grid.x, HEIGHT - 35, cell.UNVISITED_COLOR, GREY, grid),
        LegendCell(WIN, grid.x + 200, HEIGHT - 35, cell.VISITED_COLOR, GREY, grid),
        LegendCell(WIN, grid.x + 400, HEIGHT - 35, cell.OPEN_COLOR, GREY, grid),
        LegendCell(WIN, grid.x + 600, HEIGHT - 35, cell.PATH_COLOR, GREY, grid),
        LegendCell(WIN, grid.x + 800, HEIGHT - 35, cell.WALL_COLOR, GREY, grid)]


    speed_lable = pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((grid.x + 1000, HEIGHT - 37), (50, grid.gap + 5)),
                        text="Speed:",
                        manager=UI_MANAGER,
                        object_id=ObjectID(class_id="@legend_cell_lables"))
    

    speed_slider = pygame_gui.elements.UIHorizontalSlider(
                    start_value=animation_speed,
                    value_range=(animation_speed - animation_speed / 2, animation_speed + animation_speed / 2),
                    relative_rect=pygame.Rect((grid.x + 1050, HEIGHT - 37 ), (200, grid.gap + 5)), 
                    manager=UI_MANAGER)

    
    speed_value_lable = pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((grid.x + 1250, HEIGHT - 37), (35, grid.gap + 5)),
                        text="x",
                        manager=UI_MANAGER,
                        object_id=ObjectID(class_id="@legend_cell_lables"))
    speed_value_lable.set_text(f"{round(speed_slider.current_percentage * 100)}%")
    

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
        draw(WIN, grid, UI_MANAGER, time_delta, legend_cells)
        

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
                        run_current_algorithm(algo_menu, WIN, grid, start, end, animation=False)
                    
                    elif end_being_dragged and not grid[row][col].is_start() and algo_visualized:
                        end.reset()
                        end = grid[row][col]
                        end.make_end()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(algo_menu, WIN, grid, start, end, animation=False)
                   
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
                    draw_lambda()
                    run_current_algorithm(algo_menu, WIN, grid, start, end, ANIMATION, animation_speed)
                    algo_visualized = True

                #generate maze gui button
                if event.ui_element == generate_button:
                    grid.clear(start_end_except=True)
                    draw_lambda()
                    generate_current_maze(maze_menu, WIN, grid, ANIMATION, animation_speed)
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
                    draw_lambda()
                    run_current_algorithm(algo_menu, WIN, grid, start, end, ANIMATION, animation_speed)
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
                    draw_lambda()
                    generate_current_maze(maze_menu, WIN, grid, ANIMATION, animation_speed)
                    algo_visualized = False


            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == speed_slider:
                    animation_speed = speed_slider.current_value
                    speed_value_lable.set_text(f"{round(speed_slider.current_percentage * 100)}%")
                    

    pygame.quit()


def run_current_algorithm(
                        algo_menu: pygame_gui.elements.UIDropDownMenu, 
                        win: pygame.Surface, 
                        grid: Grid, 
                        start: cell.Cell, 
                        end: cell.Cell, 
                        animation: bool,
                        animation_speed: int = 0) -> None:
 
    """Calls function that visulizes selected algorithm"""

    if algo_menu.selected_option  == Algorithms.ASTAR:
        algo.astar(win, grid, start, end, animation, animation_speed) 

    elif algo_menu.selected_option  == Algorithms.DIJKSTRA:
        algo.dijkstra(win, grid, start, end, animation, animation_speed)

    elif algo_menu.selected_option == Algorithms.DFS:
        algo.dfs(win, grid, start, end, animation, animation_speed)

    elif algo_menu.selected_option == Algorithms.BFS:
        algo.bfs(win, grid, start, end, animation, animation_speed)

    elif algo_menu.selected_option == Algorithms.GBFS: 
        algo.gbfs(win, grid, start, end, animation, animation_speed)

    elif algo_menu.selected_option == Algorithms.BBFS:
        algo.bidirectional_bfs(win, grid, start, end, animation, animation_speed)
    
    else: 
        algo.astar(win, grid, start, end, animation, animation_speed)


def generate_current_maze(
                        maze_menu: pygame_gui.elements.UIDropDownMenu, 
                        win: pygame.Surface, 
                        grid: Grid, 
                        animation: bool,
                        animation_speed: int = 0) -> None:

    """Calls function that generates selected maze"""

    if maze_menu.selected_option == Mazes.RECDIV:
        maze.recursive_division_maze_gen(win, grid, animation, animation_speed)

    elif maze_menu.selected_option == Mazes.RANDOM_DFS:
        maze.random_dfs_maze_gen(win, grid, animation, animation_speed)

    elif maze_menu.selected_option == Mazes.SPIRAL:
        maze.spiral_maze(win, grid, animation, animation_speed)

    else: 
        maze.recursive_division_maze_gen(win, grid, animation, animation_speed)
        

if __name__ == '__main__':
    main()
