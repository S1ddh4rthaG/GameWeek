from terrain_generation import generate_terrain
from display import *
from config import *
from elements import Object, Player

pygame.init()
pygame.display.set_caption("Infinite World")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)


def set_terrain():
    global objects
    terrain = generate_terrain(num_squares)
    for i in range(num_squares):
        for j in range(num_squares):
            if not terrain[i][j] is None:
                o = Object()
                o.x = (i + 0.5) * square_size - world_size / 2
                o.y = (j + 0.5) * square_size - world_size / 2
                o.sprite = pygame.image.load(terrain[i][j].sprite_path)
                o.map_sprite = pygame.image.load(terrain[i][j].map_sprite_path)
                objects.append(o)
    pass


objects = list()  # this list contains all elements of the game

set_terrain()
p = Player()
objects.append(p)

c = pygame.time.Clock()  # used to track time in milliseconds
running = True
map_toggle = True  # decides whether the map is shown or not
grid_toggle = True  # decides whether grid is shown or not
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                map_toggle = not map_toggle
            elif event.key == pygame.K_g:
                grid_toggle = not grid_toggle
        p.__process_event__(event, objects)

    p.__process_input__()
    dt = c.tick(max_frame_rate)

    for o in objects:
        o.step(dt)

    render(objects, map_toggle, grid_toggle, p)

    pass
