import os
import algo
import pygame
from grid import Grid


"""1:1  cell size = 16px"""
# GRID_SIZE = (50, 50) #(rows, columns)
# GRID_DIMENSIONS = (800, 800) #px

"""21:9  cell size = 20px"""
# GRID_SIZE = (36, 84) #(rows, columns)
# GRID_DIMENSIONS = (1680, 720) #px

"""16:9  cell size = 20px""" 
GRID_SIZE = (36, 64) #(rows, columns)
GRID_DIMENSIONS = (1280, 720) #px  


ANIMATION = False


WIN = pygame.display.set_mode(GRID_DIMENSIONS)
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid) -> None:
    win.fill(pygame.Color('white'))
    grid.draw_cells()
    grid.draw_grid_lines()
    pygame.display.update()


def main() -> None:
    grid = Grid(WIN, GRID_SIZE, GRID_DIMENSIONS)

    #set start and end default positions
    start = grid[grid.total_rows // 2][grid.total_columns // 2 - 2]
    end = grid[grid.total_rows // 2][grid.total_columns // 2 + 2]
    start.make_start()
    end.make_end()

    running = True
    start_being_dragged = False
    end_being_dragged = False

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
                    clicked_cell.make_barrier()

                elif clicked_cell.is_start():
                    start_being_dragged = True 

                elif clicked_cell.is_end():
                    end_being_dragged = True

            #if right mouse button clicked
            elif pygame.mouse.get_pressed()[2]:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid[row][col]
                if clicked_cell.is_barrier():
                    clicked_cell.reset()

            #drag
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                if not grid[row][col].is_barrier():
                    if start_being_dragged and not grid[row][col].is_end():
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
                    algo.astar(lambda: draw(WIN, grid), grid, start, end, ANIMATION)

                #clear the grid
                if event.key == pygame.K_c:
                    grid.clear(start_end_except=True)   

                #generate recursive division maze
                if event.key == pygame.K_m:
                    grid.clear()
                    start = grid[0][1]
                    end = grid[grid.total_rows - 1][grid.total_columns - 2]
                    grid.update_neighbors_for_every_cell()
                    algo.recursive_division_maze_gen(lambda: draw(WIN, grid), start, end, grid, ANIMATION)
                    start.make_start()
                    end.make_end()
                
                #generate random dfs maze
                if event.key == pygame.K_n:
                    grid.clear()
                    start = grid[0][0]
                    end = grid[grid.total_rows - 1][grid.total_columns - 1]
                    grid.update_neighbors_for_every_cell()
                    algo.random_dfs_maze_gen(lambda: draw(WIN, grid), start, grid, ANIMATION)
                    start.make_start()
                    end.make_end()
                   

    pygame.quit()


if __name__ == '__main__':
    main()
