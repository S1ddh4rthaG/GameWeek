from config import *


def render(objects, map_toggle, grid_toggle, p):
    clearscreen()
    display(objects)
    update_window(p.x, p.y)
    if grid_toggle:
        diplay_gridlines()
    if map_toggle:
        map(objects, 0.1, 2, 40, 40)
    pygame.display.update()


screen = pygame.display.set_mode((width, height))

x_start = 0
y_start = 0


def map(objs, map_scale, expansion_scale, x, y):  # shows minimap
    global x_start
    global y_start
    dot_r = pygame.image.load("assets/dot_red.png")
    dot_g = pygame.image.load("assets/dot_green.png")
    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect((x, y), (map_scale * width * expansion_scale, map_scale * height * expansion_scale)),
                     1)
    pygame.draw.rect(screen, (100, 100, 100),
                     pygame.Rect((x + map_scale * (expansion_scale - 1) * width / 2,
                                  y + map_scale * (expansion_scale - 1) * height / 2),
                                 (map_scale * width, map_scale * height)), 1)
    for o in objs:
        x_ = o.x - x_start + (expansion_scale - 1) * width / 2
        y_ = o.y - y_start + (expansion_scale - 1) * height / 2
        if 0 <= x_ <= expansion_scale * width and 0 <= y_ <= expansion_scale * height:
            x__ = map_scale * x_
            y__ = map_scale * y_
            dot = o.map_sprite
            if dot is None:
                continue
            screen.blit(dot, (
                x + x__ - dot.get_rect().width / 2, y + map_scale * height * 2 - y__ - dot.get_rect().height / 2))


def update_window(x, y):
    global x_start
    global y_start
    dw = (width - movable_width) / 2
    dh = (height - movable_height) / 2
    if x_start <= x - movable_width - dw:
        x_start = x - movable_width - dw
    elif x_start >= x - dw:
        x_start = x - dw
    if y_start <= y - movable_height - dh:
        y_start = y - movable_height - dh
    elif y_start >= y - dh:
        y_start = y - dh


def display(objects):
    for t in objects:
        if t.is_valid:
            img = pygame.transform.rotate(t.sprite, -90 + t.theta)
            rect = img.get_rect()
            _X = transform_x(t.x) - (rect.width / 2)
            _Y = transform_y(t.y) - (rect.height / 2)
            screen.blit(img, (_X, _Y))


def clearscreen():
    screen.fill((0, 0, 0))


def transform_x(x):
    global x_start
    return x - x_start


def transform_y(y):
    global y_start
    return height - y + y_start


def diplay_gridlines():
    lim = int(world_size / square_size)
    for i in range(lim + 1):
        pygame.draw.line(screen, (0, 200, 0),
                         (transform_x(i * square_size - world_size / 2), transform_y(-world_size / 2)),
                         (transform_x(i * square_size - world_size / 2), transform_y(world_size / 2)))
        pygame.draw.line(screen, (0, 200, 0),
                         (transform_x(-world_size / 2), transform_y(i * square_size - world_size / 2)),
                         (transform_x(world_size / 2), transform_y(i * square_size - world_size / 2)),
                         )


def get_mouse_coordinates():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    m_x = mouse_x + x_start
    m_y = y_start+height-mouse_y
    return m_x, m_y
