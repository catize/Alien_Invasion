import pygame.font
from pygame.sprite import Group
from ship import Ship
import json

class Scoreboard:
    # class to report scoring info of game
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring info
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 30)

        # initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # turn score into rendered image
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # initializes high score for image rendering
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # center high score in screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # initializes level for image rendering
        level_str = 'Level: ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        # position level beneath score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # initialized ships for image rendering up top
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        # check if there is new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.save_new_high_score()
            self.prep_high_score()

    def save_new_high_score(self):
        with open('highscore.json', 'w') as file :
            json.dump(self.stats.high_score, file)
        return self.stats.high_score

    def show_score(self):
        # draw score, high_score, level and ships on screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)