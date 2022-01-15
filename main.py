import os
import algo
import pygame
from grid import Grid
from pygame import Color


ROWS = 50
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) 
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid) -> None:
    win.fill(Color('white'))
    grid.fill_cells_with_color()
    grid.draw_grid_lines()
    pygame.display.update()


def main(win, width, rows):
    grid = Grid(win, rows, width)

    start = None
    end = None

    running = True

    while running:
        draw(win, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

     
            if pygame.mouse.get_pressed()[0]: #left mouse button clicked
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid.get_cell(row, col)
                
                if not start  and  clicked_cell != end:
                    start =  clicked_cell
                    start.make_start()

                elif not end  and  clicked_cell != start:
                    end =  clicked_cell
                    end.make_end()    

                elif clicked_cell != end  and  clicked_cell != start:
                    clicked_cell.make_barrier()
               

            elif pygame.mouse.get_pressed()[2]: #right mouse button clicked
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_row_col_of_clicked_cell(mpos)
                clicked_cell = grid.get_cell(row, col)
                
                if  clicked_cell.is_start():
                    start = None
                    clicked_cell.reset()
          
                elif  clicked_cell.is_end():
                    end = None
                    clicked_cell.reset()

                elif clicked_cell.is_barrier():
                    clicked_cell.reset()
                
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE and start and end:
                    grid.update_available_neighbors_for_every_cell()
                    algo.astar(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_c: #clear the table
                    start = None
                    end = None
                    grid = Grid(win, rows, width)


                if event.key == pygame.K_m:
                    start = grid.get_cell(row=0, col=0)
                    end = None
                    grid.update_all_neighbors_for_every_cell()
                    algo.generate_maze_dfs(lambda: draw(win, grid), start)
                    start.make_start()

                   
 

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH, ROWS)
