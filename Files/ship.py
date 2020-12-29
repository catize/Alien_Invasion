# creates the starship

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # manages the ship
    def __init__(self, ai_game):
        # initializes ship and starting position
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # loads image
        self.image = pygame.image.load('images/Millenium-Falcon-02-icon.png')
        self.rect = self.image.get_rect()

        # start the game at midbottom
        self.rect.midbottom = self.screen_rect.midbottom

        # stores a decimal number for ship horizontal position
        self.x = float(self.rect.x)

        # movement flag to get continuous movement when flag True
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        # updates ship's position based on movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect from self.x
        self.rect.x = self.x

    def blitme(self):
        # draws ship at current location
        self.screen.blit(self.image, self.rect)

