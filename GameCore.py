import pygame
import random

import conf
from Obstacle import Obstacle


class GameCore:
    def __init__(self):
        self.screen = None
        self.screen_width = conf.SCREEN_SIZE[0]
        self.screen_height = conf.SCREEN_SIZE[1]
        self.background_color = (255, 255, 255)
        self.background_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.game_is_running = True
        self.game_stopped = False

        self.skier = pygame.image.load('assets/images/skier.png')
        self.skier = pygame.transform.scale2x(self.skier)
        self.skier_rect = self.skier.get_rect()
        self.skier_rect[0] = 100
        self.skier_rect[1] = 50

        self.spawn_interval = 500
        self.spawn_time = pygame.time.get_ticks()

        self.obstacles = []

    def draw_skier(self):
        self.screen.blit(self.skier, self.skier_rect)

    def move_skier(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.skier_rect[0] -= 10
        elif keys_pressed[pygame.K_RIGHT]:
            self.skier_rect[0] += 10

        self.draw_skier()

    def draw_obstacle(self, obstacle):
        self.screen.blit(obstacle.image, obstacle.rect)

    def spawn_tree(self):
        new_obstacle = Obstacle(random.randrange(1, conf.SCREEN_SIZE[0], 20))
        self.obstacles.append(new_obstacle)
        self.draw_obstacle(new_obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
            self.draw_obstacle(obstacle)

    def border_patrol(self):
        if self.skier_rect[0] < 0:
            self.skier_rect[0] = 0
        elif self.skier_rect[0] > self.screen_width - 20:
            self.skier_rect[0] = self.screen_width - 20

    def collide_patrol(self):
        for obstacle in self.obstacles:
            if self.skier_rect.colliderect(obstacle.rect):
                self.game_stopped = True

    def draw_game_over_screen(self):
        if self.game_stopped:
            font = pygame.font.SysFont('ComicNeue-Regular', 40)
            font_color = (255, 255, 255)
            font_position = ((conf.SCREEN_SIZE[0] / 2 - 90), conf.SCREEN_SIZE[1] / 2 - 30)
            self.screen.fill((55, 55, 55), self.background_rect)
            self.screen.blit(font.render('GAME OVER', True, font_color), font_position)

    def run_game(self):
        pygame.init()
        pygame.display.set_caption("pySki")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.screen.fill(self.background_color, self.background_rect)
        clock = pygame.time.Clock()
        self.game_is_running = True

        while self.game_is_running:
            clock.tick(30)
            self.screen.fill(self.background_color, self.background_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_is_running = False

            current_time = pygame.time.get_ticks()
            if current_time > self.spawn_time:
                self.spawn_tree()
                self.spawn_time += self.spawn_interval

            if not self.game_stopped:
                self.move_skier()
                self.move_obstacles()
                self.border_patrol()
                self.collide_patrol()
            else:
                self.draw_game_over_screen()

            pygame.display.flip()
