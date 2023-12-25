import pygame


class Skier:

    def __init__(self):
        self.image = pygame.image.load('assets/images/skier.png')
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = 100
        self.rect[1] = 100

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.rect[0] -= 10
        elif keys_pressed[pygame.K_RIGHT]:
            self.rect[0] += 10
