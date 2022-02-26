import pygame

def aborted() -> bool:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True


class Heuristic:
    """
    A class with basic heuristics 
    """

    @staticmethod
    def octil(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        (ty, tx) = (abs(y1 - y2), abs(x1 - x2))
        return max(ty, tx) + (2 ** 0.5 - 1) * min(ty, tx)

    @staticmethod
    def manhattan(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def chebyshev(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return max(abs(y1 - y2), abs(x1 - x2))

    @staticmethod
    def euclidean(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return ((y1 - y2) ** 2 + (x1 - x2) ** 2) ** 0.5