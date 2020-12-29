# Stores all settings of the game

import sys
import pygame


class Settings():
    # holds all game settings
    def __init__(self):
        # Initializing game settings
        # 1. Screen
        self.screen_width = pygame.display.Info().current_w - 80
        self.screen_height = pygame.display.Info().current_h - 80
        self.bg_color = (51, 51, 153) # (57, 167, 232) sky blue (0, 0, 0) black

        # 2. Bullet
        self.bullet_width = 3
        self.bullet_height = 12
        self.bullet_color = (255, 102, 0) # best pick red or green

        self.bullets_allowed = 5

        # 3. Ship
        self.ships_available = 2

        # how quickly game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # speed settings that change throughout the game
        self.ship_speed = 2.5
        self.bullet_speed = 2
        self.alien_speed = 1.5
        self.fleet_drop_speed = 10

        # scoring points
        self.alien_points = 50

        # fleet_direction positive moves right and negative values move left
        self.fleet_direction = 1

    def increase_speed(self):
        # increase game speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # increases points for aliens with increasing speed. made it full integers as score should be int
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)