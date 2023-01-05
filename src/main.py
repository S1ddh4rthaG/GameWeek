import random

import pygame
import math

# import random

pygame.init()

height = 720
width = 1200
max_frame_rate = 60
movable_width = 800
movable_height = 500

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Infinite World")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)


class Object:
    x = 0
    y = 0
    v = 0
    theta = 0
    w = 0
    is_valid = True
    sprite = None

    def step(self, dt):
        v_x = math.cos(math.radians(self.theta)) * self.v
        v_y = math.sin(math.radians(self.theta)) * self.v
        self.x += v_x * dt
        self.y += v_y * dt
        self.theta += self.w * dt


class Bullet(Object):
    velocity = 1
    sprite = pygame.image.load("./assets/bullet.png")
    timer = 1000

    def __init__(self, source):
        self.v = self.velocity
        self.x = source.x
        self.y = source.y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        m_x = mouse_x + x_start
        m_y = height - mouse_y + y_start
        self.theta = math.degrees(math.atan2(m_y - source.y, m_x - source.x))


class Player(Object):
    max_v = 0.4
    max_w = 0.1
    sprite = pygame.image.load("./assets/player.png")

    def __process_event__(self, e, objs):
        if e.type == pygame.MOUSEBUTTONDOWN:
            objs.append(Bullet(self))

    def __process_input__(self):
        key_list = pygame.key.get_pressed()
        if key_list[pygame.K_w] and key_list[pygame.K_s]:
            self.v = 0
        elif key_list[pygame.K_w]:
            self.v = self.max_v
        elif key_list[pygame.K_s]:
            self.v = -self.max_v
        else:
            self.v = 0
        if key_list[pygame.K_a] and key_list[pygame.K_d]:
            self.w = 0
        elif key_list[pygame.K_a]:
            self.w = self.max_w
        elif key_list[pygame.K_d]:
            self.w = -self.max_w
        else:
            self.w = 0


x_start = 0
y_start = 0


def map(objs, map_scale, expansion_scale, x, y):
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
        if type(o) == Bullet:
            continue
        x_ = o.x - x_start + (expansion_scale - 1) * width / 2
        y_ = o.y - y_start + (expansion_scale - 1) * height / 2
        if 0 <= x_ <= expansion_scale * width and 0 <= y_ <= expansion_scale * height or True:
            x__ = map_scale * x_
            y__ = map_scale * y_
            dot = dot_g if type(o) == Player else dot_r
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


def display(objs):
    for t in objs:
        if t.is_valid:
            r_x = t.x - x_start
            r_y = height - t.y + y_start
            img = pygame.transform.rotate(t.sprite, -90 + t.theta)
            rect = img.get_rect()
            _X = r_x - (rect.width / 2)
            _Y = r_y - (rect.height / 2)
            screen.blit(img, (_X, _Y))


objects = list()

for i in range(1000):
    o = Object()
    o.sprite = pygame.image.load("./assets/object.png")
    o.x = (random.random() - 0.5) * width * 10
    o.y = (random.random() - 0.5) * height * 10
    objects.append(o)

p = Player()
p.x = width / 2
p.y = height / 2
objects.append(p)
c = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        p.__process_event__(event, objects)

    p.__process_input__()

    dt = c.tick(max_frame_rate)

    screen.fill((0, 0, 0))
    for o in objects:
        o.step(dt)
    update_window(p.x, p.y)
    display(objects)
    map(objects, 0.1, 2, 40, 40)
    pygame.display.update()

    pass