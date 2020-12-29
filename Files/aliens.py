import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite) :
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game) :
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        image = pygame.image.load('images/Alien-displeased-icon.png')
        image_scared = pygame.image.load('images/Alien-scared-icon.png')
        image_shot = pygame.image.load('images/Alien-surprised-icon.png')
        image_dead = pygame.image.load('images/Alien-dream-icon.png')
        image_mad = pygame.image.load('images/Alien-mad-icon.png')
        alien_images = [image, image_scared, image_shot, image_dead, image_mad]

        self.image = random.choice(alien_images)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def contact_edges(self):
        # checks if alien is at screen edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # moves the aliens to the right
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
