#imports

import pygame
import time
import math
import utils
from utils import scale_image, rotate_image

pygame.init()

# variables

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.85)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.85)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pygame.image.load("imgs/finish.png"), 0.75)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing")

clock = pygame.time.Clock()

# classes

class PlayerCar:
    IMG = RED_CAR

    def __init__(self, max_vel, rot_vel, start_pos):
        self.max_vel = max_vel
        self.vel = 0
        self.rot_vel = rot_vel
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = start_pos
        self.start_pos = start_pos
        self.acceleration = 0.07


        

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

    def draw(self):
        rotate_image(screen, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical_velocity = math.cos(radians) * self.vel
        horizontal_velocity = math.sin(radians) * self.vel

        self.y -= vertical_velocity
        self.x -= horizontal_velocity

    def bounce(self):
        self.vel *= -0.7
        self.move()

    def reduce_speed_forwards(self):
        self.vel = max(self.vel - self.acceleration / 1.5, 0)
        self.move()

    def reduce_speed_backwards(self):
        self.vel = min(self.vel + self.acceleration / 1.5, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y-y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0

# objects

player_car = PlayerCar(4,4, (180,200))

# methods

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_car.move_forward()
        moved = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_car.move_backward()
        moved = True

    if not moved and player_car.vel > 0:
        player_car.reduce_speed_forwards()
    if not moved and player_car.vel < 0:
        player_car.reduce_speed_backwards()

# draw


def draw():
    screen.blit(GRASS, (0, 0))
    screen.blit(TRACK, (0, 0))
    screen.blit(FINISH, FINISH_POSITION)

    player_car.draw()

    pygame.display.update()

# game

game = True

while game:
    clock.tick(60)

    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            break

    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    finish_poi = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi is not None:
        if finish_poi[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            print("finish")

pygame.quit()