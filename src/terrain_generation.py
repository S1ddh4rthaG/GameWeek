# returns an n*n matrix
import random


class Cell:
    sprite_path = ""
    type = 0

    def __init__(self, sprite_path, type):
        self.sprite_path = sprite_path
        self.type = type


def generate_terrain(n):
    terrain = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            terrain[i][j] = None

    for t in range(int(n * n / 100)):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if terrain[i][j] is not None:
            continue
        terrain[i][j] = Cell("./assets/bush.png", "bush")

    return terrain
