import pygame
import random

import conf
from Obstacle import Obstacle
from Skier import Skier


class GameCore:
    def __init__(self):
        self.screen = None
        self.screen_width = conf.SCREEN_SIZE[0]
        self.screen_height = conf.SCREEN_SIZE[1]
        self.background_color = (255, 255, 255)
        self.background_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.game_is_running = True
        self.game_stopped = False

        self.skier = Skier()
        self.obstacles = []

        self.spawn_interval = 500
        self.spawn_time = pygame.time.get_ticks()

    def draw_skier(self):
        self.screen.blit(self.skier.image, self.skier.rect)

    def draw_obstacle(self, obstacle):
        self.screen.blit(obstacle.image, obstacle.rect)

    def spawn_obstacle(self):
        new_obstacle = Obstacle(random.randrange(1, conf.SCREEN_SIZE[0], 20))
        self.obstacles.append(new_obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
            self.draw_obstacle(obstacle)

    def border_patrol(self):
        if self.skier.rect[0] < 0:
            self.skier.rect[0] = 0
        elif self.skier.rect[0] > self.screen_width - 20:
            self.skier.rect[0] = self.screen_width - 20

    def collide_patrol(self):
        for obstacle in self.obstacles:
            if self.skier.rect.colliderect(obstacle.rect):
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
                self.spawn_obstacle()
                self.spawn_time += self.spawn_interval

            if not self.game_stopped:
                self.skier.move()
                self.move_obstacles()
                self.border_patrol()
                self.collide_patrol()
                self.draw_skier()
            else:
                self.draw_game_over_screen()

            pygame.display.flip()
