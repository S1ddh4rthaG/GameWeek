from config import *
from display import get_mouse_coordinates
import math


class Object:  # This is the base class for all elements in the game
    x = 0
    y = 0  # co-ordinates in absolute space
    v = 0  # magnitude of velocity vector
    theta = 0  # angle made with positive x-axis
    w = 0  # angular velocity
    is_valid = True
    sprite = None  # image to display at the location of the object
    map_sprite = None

    def step(self, dt):  # moves the object in one frame
        v_x = math.cos(math.radians(self.theta)) * self.v
        v_y = math.sin(math.radians(self.theta)) * self.v
        self.x += v_x * dt
        self.y += v_y * dt
        self.theta += self.w * dt
        self.theta %= 360


class Fireball(Object):  # shot by player using mouse
    velocity = 1
    sprite = pygame.image.load("./assets/bullet.png")
    timer = 1000

    def __init__(self, source, target_x, target_y):
        self.v = self.velocity
        self.x = source.x
        self.y = source.y
        self.theta = math.degrees(math.atan2(target_y - source.y, target_x - source.x))


class Player(Object):  # controlled by player
    max_v = 0.4  # running velocity
    max_w = 0.1  # turning angular velocity
    sprite = pygame.image.load("./assets/player.png")
    map_sprite = pygame.image.load("./assets/dot_green.png")

    def __process_event__(self, e, objs):  # processes keystrokes
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = get_mouse_coordinates()
            objs.append(Fireball(self, x, y))
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_j:
                number = 16
                for i in range(number):
                    p = math.radians(360*i/number)
                    x = self.x + math.cos(p)
                    y = self.y + math.sin(p)
                    objs.append(Fireball(self, x, y))

    def __process_input__(self):  # makes state of player reflect state of keyboard
        key_list = pygame.key.get_pressed()
        up = 1 if key_list[pygame.K_w] else 0
        down = 1 if key_list[pygame.K_s] else 0
        left = 1 if key_list[pygame.K_a] else 0
        right = 1 if key_list[pygame.K_d] else 0
        var = up << 3 | down << 2 | left << 1 | right
        if var == 0b0000 or var == 0b1111 or var == 0b0011 or var == 0b1100:
            self.v = 0
        else:
            self.v = self.max_v
            if var == 0b1000 or var == 0b1011:
                self.theta = 90
            elif var == 0b0100 or var == 0b0111:
                self.theta = 270
            elif var == 0b0010 or var == 0b1110:
                self.theta = 180
            elif var == 0b0001 or var == 0b1101:
                self.theta = 0
            elif var == 0b1010:
                self.theta = 135
            elif var == 0b1001:
                self.theta = 45
            elif var == 0b0110:
                self.theta = 225
            elif var == 0b0101:
                self.theta = 315
