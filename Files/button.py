# create a play button
import pygame.font

class Button:
    def __init__(self, ai_game, msg, offset_centerx = 0, offset_centery = 0):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # sets the button dimensions
        self.width, self.height = 100, 40
        self.button_color = (0, 255, 0) # (102, 102, 153)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 30)

        # build buttons rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx + offset_centerx
        self.rect.centery = self.screen_rect.centery + offset_centery

        # prep msg for button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # turn msg into rendered image and center text on button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # draw blank button and then draw msg
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

