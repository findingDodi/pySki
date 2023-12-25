import random
import pygame
import os
import conf


class Obstacle:

    def __init__(self, pos_x):
        possible_obstacles = os.listdir('assets/images/obstacles')
        self.image = pygame.image.load('assets/images/obstacles/{}'.format(random.choice(possible_obstacles)))
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = pos_x
        self.rect[1] = conf.SCREEN_SIZE[1] + 1

    def move(self):
        self.rect[1] -= 2
