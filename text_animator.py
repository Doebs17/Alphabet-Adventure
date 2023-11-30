import pygame
from settings import Settings
import random
import math

class TextAnimator:
    def __init__(self, fw_game, screen):
        self.screen = screen
        self.settings = Settings()
        self.clouds = fw_game.clouds  
        self.font = pygame.font.SysFont(self.settings.font, self.settings.font_size)
        self.text_color = (255, 255, 255)
        self.is_animating = False
        self.current_animation = None
        self.current_text = ""
        self.draw_underline = False
        self.centered_position = (0, 0)
        self.text_end_x = fw_game.animation_text_position[0]
        self.alpha = 0

    def start_animation(self, text, centered_position):
        self.draw_underline = True
        self.is_animating = True
        self.current_text = text
        self.centered_position = centered_position
        self.original_y = centered_position[1]
        self.alpha = 0  
        self.current_animation = random.choice([self.fade_in, self.slide_in_from_left, self.bounce]) 

    def update(self):
        if self.is_animating and self.current_animation:
            self.current_animation()

    def draw(self):
        if not self.current_text:
            return
        if self.current_text == 'Ice cream':
            self.font = pygame.font.SysFont(self.settings.font, 120)
        text_surface = self.font.render(self.current_text, True, self.text_color)
        text_surface.set_alpha(self.alpha)
        
        text_width, text_height = self.font.size(self.current_text)
        starting_x = self.centered_position[0] - text_width // 2
        starting_y = self.centered_position[1] - text_height // 2
        
        self.screen.blit(text_surface, (starting_x, starting_y))
        # and not self.is_animating
        if self.draw_underline:
            char_width, _ = self.font.size(self.current_text[0])
            underline_start_pos = (starting_x, starting_y + text_height - 20)
            underline_end_pos = (starting_x + char_width, starting_y + text_height - 20)
            pygame.draw.line(self.screen, self.text_color, underline_start_pos, underline_end_pos, 8)

    def fade_in(self):
        alpha_step = 255 / (800 / 10)
        self.alpha += alpha_step
        if self.alpha >= 255:
            self.is_animating = False

    def slide_in_from_left(self):
        start_x = -self.font.size(self.current_text)[0]
        if self.alpha == 0:  # First time the method runs for the current animation   
            self.centered_position = (start_x, self.centered_position[1])
            self.alpha = 255  # We set alpha to 255 since we're not fading in
        
        step = (self.text_end_x - start_x) / (1000 / 10)
        
        new_x = self.centered_position[0] + step
        self.centered_position = (new_x, self.centered_position[1])
        
        if new_x >= self.text_end_x:
            self.centered_position = (self.text_end_x, self.centered_position[1])
            self.is_animating = False

    def bounce(self):
        self.alpha = 255
        bounce_distance = 50  # The maximum distance the text will bounce (adjust as needed)
        bounce_speed = 0.1    # The speed of the bounce (adjust as needed)

        # Increment the bounce counter
        if not hasattr(self, 'bounce_counter'):
            self.bounce_counter = 0

        self.bounce_counter += bounce_speed

        # Calculate the y-offset using the sine function for the bounce effect
        y_offset = bounce_distance * math.sin(self.bounce_counter)

        # The centered_position's y-coordinate is adjusted by the y_offset
        self.centered_position = (self.centered_position[0], self.original_y + y_offset)

        # Stop the animation after one full bounce cycle
        if self.bounce_counter >= 2 * math.pi:
            self.is_animating = False
            self.centered_position = (self.centered_position[0], self.original_y)
            del self.bounce_counter