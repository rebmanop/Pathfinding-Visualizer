import pygame
import pygame_gui
import cell
from pygame_gui.core import ObjectID
from legend_cell import LegendCell
from grid import GREY


GUI_ELEMENT_OFFSET = 20


class GUI:
    def __init__(self, win, ui_manager, grid, algorithms, mazes, width, height, animation_speed):
        
        self.algo_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=[algo for algo in algorithms],
            starting_option=algorithms.ASTAR,
            relative_rect=pygame.Rect((grid.x, grid.y / 2 - 15), (230, 30)),
            manager=ui_manager,
        )

        self.visualize_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    self.algo_menu.get_abs_rect().x
                    + self.algo_menu.get_abs_rect().width
                    + GUI_ELEMENT_OFFSET,
                    grid.y / 2 - 15,
                ),
                (100, 30),
            ),
            text="Visualize",
            manager=ui_manager,
            object_id="#visualize_button",
        )

        self.maze_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=[maze for maze in mazes],
            starting_option=mazes.RECDIV,
            relative_rect=pygame.Rect(
                (
                    self.visualize_button.get_abs_rect().x
                    + self.visualize_button.get_abs_rect().width
                    + GUI_ELEMENT_OFFSET,
                    grid.y / 2 - 15,
                ),
                (305, 30),
            ),
            manager=ui_manager,
        )

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    self.maze_menu.get_abs_rect().x
                    + self.maze_menu.get_abs_rect().width
                    + GUI_ELEMENT_OFFSET,
                    grid.y / 2 - 15,
                ),
                (100, 30),
            ),
            text="Generate",
            manager=ui_manager,
        )

        self.clear_everything_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width - 55, grid.y / 2 - 15), (50, 30)),
            text="CE",
            manager=ui_manager,
        )

        self.unvisited_cell_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + grid.gap, height - 35), (130, grid.gap)),
            text="-unvisited cell",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.visited_cell_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 200 + grid.gap, height - 35), (115, grid.gap)),
            text="-visited cell",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.open_cell_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 400 + grid.gap, height - 35), (90, grid.gap)),
            text="-open cell",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.path_cell_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 600 + grid.gap, height - 35), (90, grid.gap)),
            text="-path cell",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.wall_cell_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 800 + grid.gap, height - 35), (90, grid.gap)),
            text="-wall cell",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.legend_cells = [
            LegendCell(win, grid.x, height - 35, cell.UNVISITED_COLOR, GREY, grid),
            LegendCell(win, grid.x + 200, height - 35, cell.VISITED_COLOR_1, GREY, grid),
            LegendCell(win, grid.x + 400, height - 35, cell.OPEN_COLOR, GREY, grid),
            LegendCell(win, grid.x + 600, height - 35, cell.PATH_COLOR, GREY, grid),
            LegendCell(win, grid.x + 800, height - 35, cell.WALL_COLOR, GREY, grid),
        ]

        self.clear_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width - 105, grid.y / 2 - 15), (50, 30)),
            text="C",
            manager=ui_manager,
        )

        self.parcel_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    self.generate_button.get_abs_rect().x
                    + self.generate_button.get_abs_rect().width
                    + GUI_ELEMENT_OFFSET,
                    grid.y / 2 - 15,
                ),
                (130, 30),
            ),
            text="Add Parcel",
            manager=ui_manager,
        )
        self.speed_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 1000, height - 37), (50, grid.gap + 5)),
            text="Speed:",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            start_value=animation_speed,
            value_range=(animation_speed - animation_speed / 2, animation_speed + animation_speed / 2,),
            relative_rect=pygame.Rect((grid.x + 1050, height - 37), (200, grid.gap + 5)),
            manager=ui_manager,
        )

        self.speed_value_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 1250, height - 37), (35, grid.gap + 5)),
            text="x",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@legend_cell_lables"),
        )

        self.speed_value_lable.set_text(f"{round(self.speed_slider.current_percentage * 100)}%")
