import os
import algo
import pygame
from grid import Grid
from pygame import Color

GRID_SIZE = (40, 60)
GRID_DIMENSIONS = (1200, 800)

ANIMATION = True

WIN = pygame.display.set_mode(GRID_DIMENSIONS)
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid) -> None:
    win.fill(Color('white'))
    grid.draw_cells()
    grid.draw_grid_lines()
    pygame.display.update()



def main() -> None:
    grid = Grid(WIN, GRID_SIZE, GRID_DIMENSIONS)

    start = None
    end = None

    running = True

    while running:
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if left mouse button clicked
            if pygame.mouse.get_pressed()[0]:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if not start and clicked_cell != end:
                    start = clicked_cell
                    start.make_start()

                elif not end and clicked_cell != start:
                    end = clicked_cell
                    end.make_end()

                elif clicked_cell != end and clicked_cell != start:
                    clicked_cell.make_barrier()

            # if right mouse button clicked
            elif pygame.mouse.get_pressed()[2]:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_start():
                    start = None
                    clicked_cell.reset()

                elif clicked_cell.is_end():
                    end = None
                    clicked_cell.reset()

                elif clicked_cell.is_barrier():
                    clicked_cell.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    grid.update_neighbors_for_every_cell()
                    algo.astar(lambda: draw(WIN, grid), grid, start, end, ANIMATION)

                # clear the table
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = Grid(WIN, GRID_SIZE, GRID_DIMENSIONS)

                if event.key == pygame.K_m:
                    start = grid[1][1]
                    end = None
                    grid.update_neighbors_for_every_cell()
                    algo.recursive_division_maze_gen(lambda: draw(WIN, grid), start, grid, ANIMATION)
                    start.make_start()

    pygame.quit()


if __name__ == '__main__':
    main()
