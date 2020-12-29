# Definition of game
# Run this file to start game

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from aliens import Alien


class AlienInvasion:
    # overall class to manage game assets and resources
    def __init__(self):
        # Initializes game
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # replace to ((0,0), pygame.FULLSCREEN) for fullscreen gaming
        # activate for full screen gaming
        # self.settings.screen_height = self.screen.get_rect().height
        # self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("   (-(-_(-_-)_-)-)  Alien Invasion (-(-_(-_-)_-)-)   ")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play", 0, 50)
        self.quit_button = Button(self, "Quit", 0, 110)

    def run_game(self):
        # start the main loop for the game
        while True:
            # checks for events over mousepad or keyboard
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # checks if user wants to exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # checks for movement start
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # checks for movement stop
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_keydown_events(self, event):
        # responds to keydown events
        if event.key == pygame.K_RIGHT:
            # moves ship to right at keydown
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # moves ship to left at keydown
            self.ship.moving_left = True
        elif event.key == pygame.K_q :
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # responds to keyup events
        if event.key == pygame.K_RIGHT :
            # stops movement to right at keyup
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT :
            # stops movement to left at keyup
            self.ship.moving_left = False
        elif event.key == pygame.K_q :
            sys.exit()

    def _check_play_button(self, mouse_pos):
        # starts game when player presses play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset speed settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats._get_high_score()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_high_score()
            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        # starts game when player presses play
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            sys.exit()

    def _fire_bullet(self):
        # creates a bullet and adds it to group of bullets for amount of bullets allowed
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # updates the bullets
        self.bullets.update()
        # get rid of bullets that disappear from the screen
        for bullet in self.bullets.copy() :
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        # print(len(self.bullets)) # checks if bullets are being removed from copy of list
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # check for bullets that hit an alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # count aliens shot
        if collisions:
            for aliens in collisions.values():
                self.stats.counter_aliens_shot += 1
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # when there are no more aliens, remaining bullets are distroyed and new fleet is initialized
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        # create a fleet of aliens
        # calculates number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine number of rows that fit the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        # create a row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # creates an alien and places it in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 50 + (2 * alien_height * row_number)
        self.aliens.add(alien)

    def _contact_fleet_edges(self):
        # respond to edge contact  of fleet
        for alien in self.aliens.sprites():
            if alien.contact_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # changes the fleet direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        # updates alien position in fleet after movement
        self.aliens.update()
        # checks if alien touches screen edge and drops alien one row
        self._contact_fleet_edges()
        self._check_alien_ship_collisions()
        self._check_aliens_buttom()

    def _check_alien_ship_collisions(self):
        # checks if alien hit the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            # print(f"Ship hit!! {self.aliens} {self.ship}")

    def _ship_hit(self):
        # responds to ship being hit by alien
        # decrement the number of ships available
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # get rid of any bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else:
            self.sb.check_high_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_buttom(self):
        # checks for aliens if they hit bottom of screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            # is the same as if ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        # redraw screen during each pass of loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            #bullet.draw.rect(self.screen, self.settings.bullet_color, self.b_rect)
        self.aliens.draw(self.screen)
        # draw score information
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()


        # shows most recent screen
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()