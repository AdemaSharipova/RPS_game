import os

import pygame
import random


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, mass=1):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        # ACCELERATION: [0,0] could be changed
        self.acceleration = [1, 1]
        self.mass = mass

    def keep_within_bounds(self, width, height):
        # Method to keep object within the bounds
        if self.rect.x < 0:
            self.rect.x = 0
            self.velocity[0] = abs(self.velocity[0])
        elif self.rect.x + self.rect.width > width:
            self.rect.x = width - self.rect.width
            self.velocity[0] = -abs(self.velocity[0])

        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity[1] = abs(self.velocity[1])
        elif self.rect.y + self.rect.height > height:
            self.rect.y = height - self.rect.height
            self.velocity[1] = -abs(self.velocity[1])

        self.velocity[0] = max(min(self.velocity[0], 1), -1)
        self.velocity[1] = max(min(self.velocity[1], 1), -1)

    def update(self, width, height):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.acceleration = [0, 0]
        self.keep_within_bounds(width, height)


class Rock(GameObject):
    WIDTH = 50
    HEIGHT = 50
    IMAGE = os.path.join('assets', 'images', 'rock.png')

    def __init__(self, x, y):
        super().__init__(x, y, Rock.WIDTH, Rock.HEIGHT, self.IMAGE)


class Paper(GameObject):
    WIDTH = 50
    HEIGHT = 50
    IMAGE = os.path.join('assets', 'images', 'paper.png')

    def __init__(self, x, y):
        super().__init__(x, y, Paper.WIDTH, Paper.HEIGHT, self.IMAGE)


class Scissors(GameObject):
    WIDTH = 50
    HEIGHT = 50
    IMAGE = os.path.join('assets', 'images', 'scissors.png')

    def __init__(self, x, y):
        super().__init__(x, y, Scissors.WIDTH, Scissors.HEIGHT, self.IMAGE)
