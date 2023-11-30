import pygame
from settings import Settings
from background import Background
from clouds import Cloud


class ImageAnimator:
    def __init__(self, fw_game, screen):
        """Initialize the ImageAnimator with the given screen."""
        self.screen = screen
        self.settings = fw_game.settings
        self.font = pygame.font.SysFont(None, self.settings.font_size)
        self.font_height = self.font.get_height()
        self.current_image = None
        self.current_position = None
        self.is_animating = False
        self.animation_type = None
        self.image_animation_complete = False
        self.speed = 8
        self.alpha = 0
        self.end_y = None
        self.last_update = pygame.time.get_ticks()
        self.fade_duration = 1000

    def start_animation(self, image, center_position, animation_type, padding):
        self.is_animating = True
        image_path = image
        self.animation_type = animation_type

        if self.animation_type == 'fade_in':
            self.alpha = 0

        if isinstance(image, str):  # If image is a file path
            self.current_image = pygame.image.load(image_path).convert_alpha()
            
        elif isinstance(image, pygame.Surface):  # If image is a Pygame Surface
            self.current_image = image

        image_width, image_height = self.current_image.get_size()

        new_y_position = center_position[1] - image_height - 60 + padding
        
        self.current_position = [
            center_position[0] - image_width // 2,
            new_y_position
        ]
        
        if animation_type == 'slide_down':
            self.alpha = 255
            self.current_position[1] = 0 - image_height
            self.end_y = new_y_position

        elif animation_type == 'fade_in':
            self.current_image.set_alpha(self.alpha)

    def update(self):
        if self.is_animating:
            if self.animation_type == 'slide_down':
                if self.current_position[1] < self.end_y:
                    self.current_position[1] += self.speed
                    
                else:
                    self.is_animating = False
                    self.image_animation_complete = True

            elif self.animation_type == 'fade_in':
                if self.alpha < 255:
                    self.alpha += 5
                else:
                    self.is_animating = False
                    self.image_animation_complete = True
            self.current_image.set_alpha(self.alpha)

    def draw(self, display_type):
        if self.current_image and self.is_animating or display_type == 'image':
            self.screen.blit(self.current_image, self.current_position)

    def clear_image(self):
        self.current_image = None



# class ImageAnimator:
#     def __init__(self, fw_game, screen):
#         """Initialize the ImageAnimator with the given screen."""
#         self.screen = screen
#         self.settings = Settings()   
#         self.background = Background(self.screen)
#         self.clouds = fw_game.clouds      
#         font = pygame.font.SysFont(None, self.settings.font_size)
#         self.font_height = font.get_height()
#         self.current_image = None
#         self.current_position = None
#         self.is_animating = False
        

#     def start_animation(self,image, center_position):
#         self.is_animating = True
#         image_path = image
#         center_position = center_position
#         image_animations = [self.start_slide_from_top]
#         random.choice(image_animations)(image_path,center_position)

#     def start_slide_from_top(self, image_path, center_position, speed=8, background=None):
#         self.current_image = pygame.image.load(image_path)
#         self.current_position = (center_position[0] - self.current_image.get_width() // 2, 0 - self.current_image.get_height())
#         self.end_y = center_position[1] - self.font_height // 2 - 20 - self.current_image.get_height()
#         self.speed = speed
#         self.background = background
#         self.is_animating = True

#     def update(self):
#         if self.is_animating and self.current_position: 
#             if self.current_position[1] < self.end_y:
#                 self.current_position = (self.current_position[0], self.current_position[1] + self.speed)          
#             else:
#                 self.is_animating = False
#         else:
#             return
        
#     def draw(self):
#         if not self.current_image:
#             return
#         else:
#             self.screen.blit(self.current_image, self.current_position)

      