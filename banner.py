import pygame.font
from button import Button

class Banner:
    def __init__(self, fw_game, msg, position):
        self.screen = fw_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 275, 100
        self.text_color = (255,182,255)
        self.font = pygame.font.SysFont('Cooper Black', 140)
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Initial text rendering
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()

        # Border thickness
        border_thickness = 2  # You can adjust this value

        # Create a surface for the bordered text
        bordered_surface = pygame.Surface((self.msg_image_rect.width + border_thickness * 2, 
                                           self.msg_image_rect.height + border_thickness * 2), pygame.SRCALPHA)

        # Render the border (white text) around the original position
        border_color = (140, 140, 140)  # Black border
        for dx in [-border_thickness, 0, border_thickness]:
            for dy in [-border_thickness, 0, border_thickness]:
                if dx != 0 or dy != 0:
                    border_render = self.font.render(msg, True, border_color)
                    bordered_surface.blit(border_render, (dx + border_thickness, dy + border_thickness))

        # Blit the original text on top
        bordered_surface.blit(self.msg_image, (border_thickness, border_thickness))

        # Update msg_image and its rect to be the bordered surface
        self.msg_image = bordered_surface
        self.msg_image_rect = bordered_surface.get_rect()
        self.msg_image_rect.center = (self.rect.x, self.rect.y)

    def draw_banner(self):
        # Blit the bordered text surface onto the screen
        self.screen.blit(self.msg_image, self.msg_image_rect)