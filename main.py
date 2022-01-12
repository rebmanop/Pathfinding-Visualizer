import pygame
import os
from grid import draw_grid, make_grid
from algo import astar, dijkstra, dfs, generate_maze_dfs


WHITE = (255, 255, 255)
ROWS = 50
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) 
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'logo.png')).convert_alpha(), (35, 35))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.display.set_icon(LOGO)


def draw(win, grid, rows, width) -> None:
    win.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_row_col_of_clicked_cell(pos, rows, width) -> tuple:
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width, rows):
    grid = make_grid(rows, width)

    start = None
    end = None

    running = True

    while running:
        draw(win, grid, ROWS, WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

     
            if pygame.mouse.get_pressed()[0]: #left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_of_clicked_cell(pos, rows, width)
                clicked_cell = grid[row][col]

                if not start and  clicked_cell != end:
                    start =  clicked_cell
                    start.make_start()

                elif not end and  clicked_cell != start:
                    end =  clicked_cell
                    end.make_end()

                elif  clicked_cell != end and  clicked_cell != start:
                     clicked_cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]: #right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_of_clicked_cell(pos, rows, width)
                clicked_cell = grid[row][col]
                
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
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)


                if event.key == pygame.K_m:
                    start = grid[0][0]
                    end = None
                    
                    for row in grid:
                        for cell in row:
                            cell.make_barrier()

                    for row in grid:
                        for cell in row:
                            cell.update_maze_gen_neighbors(grid)

                    generate_maze_dfs(lambda: draw(win, grid, ROWS, WIDTH), start)

                    start.make_start()

                   
 

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH, ROWS)
