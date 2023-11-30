import pygame

class Background:
    def __init__(self, screen):
        self.bg_color_top = (173, 216, 230)  # Light sky blue color for the top
        self.bg_color_bottom = (100, 149, 237)
        self.screen = screen

    def draw_gradient_background(self):
        """Draws a vertical gradient from top color to bottom color."""
        for y in range(self.screen.get_height()):
            # Interpolate between the two colors based on y position
            blend_factor = 1 - (y / self.screen.get_height())  # Adjusted blend_factor
            r = self.bg_color_top[0] + blend_factor * (self.bg_color_bottom[0] - self.bg_color_top[0])
            g = self.bg_color_top[1] + blend_factor * (self.bg_color_bottom[1] - self.bg_color_top[1])
            b = self.bg_color_top[2] + blend_factor * (self.bg_color_bottom[2] - self.bg_color_top[2])
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (0, y), (self.screen.get_width(), y))