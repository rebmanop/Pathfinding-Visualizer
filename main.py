import os
import random
import maze
import algo
import cell
import pygame
import pygame_gui
from gui import GUI
from grid import Grid
from typing import Callable
from strenum import StrEnum
from legend_cell import LegendCell


WIDTH, HEIGHT = 1291, 765
GRID_WIDTH, GRID_HEIGHT = 1280, 680
GRID_SIZE = (34, 64)  # (rows, columns)
GRID_POSITION = ((WIDTH - GRID_WIDTH) / 2, (HEIGHT - GRID_HEIGHT) / 2)
ANIMATION_SPEED = 250


BG_COLOR = (64, 227, 206)  # green
ANIMATION = True


pygame.init()
FPS = 240
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
UI_MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), "gui_theme.json")
LOGO = pygame.transform.scale(pygame.image.load(os.path.join("assets\imgs", "logo.png")).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


class Algorithms(StrEnum):
    ASTAR = "A* Search"
    DIJKSTRA = "Dijkstra's Algorithm"
    DFS = "Depth-first Search"
    BFS = "Breadth-first Search"
    GBFS = "Greedy Best-first Search"
    BBFS = "Bidirectional BFS"


class Mazes(StrEnum):
    RECDIV = "Recursive Division Maze"
    RANDOM_DFS = "Randomized Depth-first Search Maze"
    SPIRAL = "Spiral Maze"
    STAIR = "Stair Pattern Maze"


def draw(
    win: pygame.surface.Surface, 
    grid: Grid, 
    ui_manager: pygame_gui.UIManager, 
    time_delta: float, 
    legend_cells: list[LegendCell],
) -> None:
    
    """Draws stuff to the screen every frame"""

    win.fill(BG_COLOR)
    grid.draw_under_grid_lines()
    grid.draw_grid_lines()
    grid.draw_over_grid_lines()
    ui_manager.update(time_delta)
    grid.draw_grid_frame()

    for legend_cell in legend_cells:
        legend_cell.draw_legend_cell()

    ui_manager.draw_ui(WIN)
    pygame.display.update()


def main() -> None:
    animation_speed = 250
   
    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, (GRID_WIDTH, GRID_HEIGHT), GRID_POSITION)
    gui = GUI(WIN, UI_MANAGER, grid, Algorithms, Mazes, WIDTH, HEIGHT, animation_speed)

    # scales images to correct cell size
    cell.Cell.scale_cell_imgs(grid.gap, grid.gap)

    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
    start.make_start()
    end.make_end()

    parcel = None

    running = True
    start_being_dragged = False
    end_being_dragged = False
    parcel_being_dragged = False
    algo_visualized = False

    while running:
        time_delta = clock.tick(FPS) / 1000.0
        draw(WIN, grid, UI_MANAGER, time_delta, gui.legend_cells)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            UI_MANAGER.process_events(event)

            # if left mouse button clicked
            if (
                pygame.mouse.get_pressed()[0]
                and grid.mouse_on_the_grid()
                and gui.algo_menu.menu_states["closed"] == gui.algo_menu.current_state
                and gui.maze_menu.menu_states["closed"] == gui.maze_menu.current_state
            ):
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_rc_of_under_mouse_cell(mpos)
                clicked_cell = grid[row][col]

                if (
                    clicked_cell != end
                    and clicked_cell != start
                    and clicked_cell != parcel
                    and not start_being_dragged
                    and not end_being_dragged
                    and not parcel_being_dragged
                ):
                    clicked_cell.make_wall()

                elif clicked_cell.is_start():
                    start_being_dragged = True

                elif clicked_cell.is_end():
                    end_being_dragged = True

                elif parcel and clicked_cell.is_parcel():
                    parcel_being_dragged = True

            # if right mouse button clicked
            elif pygame.mouse.get_pressed()[2] and grid.mouse_on_the_grid():
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_rc_of_under_mouse_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_wall():
                    clicked_cell.reset()

            # drag
            if (
                event.type == pygame.MOUSEMOTION
                and grid.mouse_on_the_grid()
                and (start_being_dragged or end_being_dragged or parcel_being_dragged)
            ):
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_rc_of_under_mouse_cell(mpos)
                if not grid[row][col].is_wall():
                    if (start_being_dragged 
                    and algo_visualized 
                    and not grid[row][col].is_end() 
                    and not grid[row][col].is_parcel()
                    ):
                        start.reset()
                        start = grid[row][col]
                        start.make_start()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(gui.algo_menu, WIN, grid, start, end, animation=False, parcel=parcel)

                    elif (end_being_dragged 
                    and algo_visualized 
                    and not grid[row][col].is_start() 
                    and not grid[row][col].is_parcel()
                    ):
                        end.reset()
                        end = grid[row][col]
                        end.make_end()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(gui.algo_menu, WIN, grid, start, end, animation=False, parcel=parcel)

                    elif (parcel_being_dragged 
                    and algo_visualized 
                    and not grid[row][col].is_start() 
                    and not grid[row][col].is_end()
                    ):
                        parcel.reset()
                        parcel = grid[row][col]
                        parcel.make_parcel()
                        grid.clear(start_end_except=True, barrier_except=True)
                        grid.update_neighbors_for_every_cell()
                        run_current_algorithm(gui.algo_menu, WIN, grid, start, end, animation=False, parcel=parcel)


                    elif (start_being_dragged and grid[row][col].is_unvisited()):
                        start.reset()
                        start = grid[row][col]
                        start.make_start()

                    elif (end_being_dragged and grid[row][col].is_unvisited()):
                        end.reset()
                        end = grid[row][col]
                        end.make_end()

                    elif (parcel and parcel_being_dragged and grid[row][col].is_unvisited()):
                        parcel.reset()
                        parcel = grid[row][col]
                        parcel.make_parcel()

            # drop
            if event.type == pygame.MOUSEBUTTONUP:
                start_being_dragged = False
                end_being_dragged = False
                parcel_being_dragged = False

            # visualize algorithm 
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gui.visualize_button:
                    grid.clear(start_end_except=True, barrier_except=True)
                    grid.update_neighbors_for_every_cell()
                    draw(WIN, grid, UI_MANAGER, time_delta, gui.legend_cells)
                    run_current_algorithm(gui.algo_menu, WIN, grid, start, end, ANIMATION, animation_speed, parcel)
                    algo_visualized = True

                # generate maze 
                if event.ui_element == gui.generate_button:
                    grid.clear(start_end_except=True)
                    draw(WIN, grid, UI_MANAGER, time_delta, gui.legend_cells)
                    generate_current_maze(gui.maze_menu, WIN, grid, ANIMATION, animation_speed)
                    algo_visualized = False

                # clear everything on the grid 
                if event.ui_element == gui.clear_everything_button:
                    grid.clear(start_end_except=True)
                    algo_visualized = False

                    # reset start and end positions
                    start.reset()
                    end.reset()
                    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
                    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
                    start.make_start()
                    end.make_end()

                # clear algo visualization and path 
                if event.ui_element == gui.clear_button:
                    grid.clear(start_end_except=True, barrier_except=True)
                    algo_visualized = False

                # add/remove parcell
                if event.ui_element == gui.parcel_button:
                    if parcel:
                        parcel.reset()
                        parcel = None
                        gui.parcel_button.set_text("Add Parcel")
                    else:
                        available_parcel_cells = [cell for row in grid.raw_grid 
                        for cell in row if not cell.is_start() and not cell.is_end()]
                        
                        parcel = random.choice(available_parcel_cells)
                        parcel.make_parcel() 
                        gui.parcel_button.set_text("Remove Parcel")


            # animation speed slider
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == gui.speed_slider:
                    animation_speed = gui.speed_slider.current_value
                    gui.speed_value_lable.set_text(f"{round(gui.speed_slider.current_percentage * 100)}%")

    pygame.quit()


def run_current_algorithm(
    algo_menu: pygame_gui.elements.UIDropDownMenu,
    win: pygame.surface.Surface,
    grid: Grid,
    start: cell.Cell,
    end: cell.Cell,
    animation: bool,
    animation_speed: int = 0,
    parcel: cell.Cell = None,
) -> None:

    """Determines which algorithm is selected and calls it's function"""

    if algo_menu.selected_option == Algorithms.ASTAR:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.astar)

    elif algo_menu.selected_option == Algorithms.DIJKSTRA:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.dijkstra)

    elif algo_menu.selected_option == Algorithms.DFS:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.dfs)

    elif algo_menu.selected_option == Algorithms.GBFS:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.gbfs)

    elif algo_menu.selected_option == Algorithms.BFS:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.bfs)

    elif algo_menu.selected_option == Algorithms.BBFS:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.bidirectional_bfs)

    else:
        run_algorithm(win, grid, start, end, animation, animation_speed, parcel, algo.astar)


def run_algorithm(
    win: pygame.surface.Surface, 
    grid: Grid, 
    start: cell.Cell, 
    end: cell.Cell, 
    animation: bool, 
    animation_speed: int, 
    parcel: cell.Cell, 
    current_algorithm: Callable,
) -> None:

    """Runs selected algorithm in one or two steps based on parcel presence"""
    
    if parcel:
        first_path_half = current_algorithm(win, grid, start, parcel, animation, animation_speed)
        cell.Cell.visited_color = cell.VISITED_COLOR_2
        second_path_half = current_algorithm(win, grid, parcel, end, animation, animation_speed)
        cell.Cell.visited_color = cell.VISITED_COLOR_1
        if first_path_half and second_path_half:
            algo.animate_path(win,  first_path_half + second_path_half, grid, animation)
    else:
        path = current_algorithm(win, grid, start, end, animation, animation_speed)
        if path:
            algo.animate_path(win, path, grid, animation)


def generate_current_maze(
    maze_menu: pygame_gui.elements.UIDropDownMenu,
    win: pygame.surface.Surface,
    grid: Grid,
    animation: bool,
    animation_speed: int = 0,
) -> None:

    """Calls maze generation function based on selected option"""

    if maze_menu.selected_option == Mazes.RECDIV:
        maze.recursive_division_maze_gen(win, grid, animation, animation_speed)

    elif maze_menu.selected_option == Mazes.RANDOM_DFS:
        maze.random_dfs_maze_gen(win, grid, animation, animation_speed)

    elif maze_menu.selected_option == Mazes.SPIRAL:
        maze.spiral_maze(win, grid, animation, animation_speed)

    elif maze_menu.selected_option == Mazes.STAIR:
        maze.stair_pattern_maze(win, grid, animation, animation_speed)

    else:
        maze.recursive_division_maze_gen(win, grid, animation, animation_speed)


if __name__ == "__main__":
    main()
