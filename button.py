import pygame.font

class Button:
    def __init__(self, fw_game, msg, center_coords):
        self.screen = fw_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 250, 70
        self.button_color = (255,182,255)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 90)

        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = center_coords

        self._prep_msg(msg)

        self.selected = False

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg,True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        pygame.draw.rect(self.screen, (140, 140, 140) , self.rect, 3)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    # def draw_easy_button(self):

