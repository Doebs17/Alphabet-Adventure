import pygame
from pygame.sprite import Sprite
import random

class Cloud(Sprite):
    def __init__(self, fw_game, image_path):
        super().__init__()
        self.screen = fw_game.screen
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = float(self.rect.x)
        self.speed = random.uniform(0.2,0.25)
        self.clouds = fw_game.clouds
    
    def _move(self):
        self.x += self.speed
        if self.x > self.screen.get_width():
            self._reset_position()

    def _reset_position(self):
        self.x = random.randint(-self.rect.width * 2,-400)
        self.rect.y = random.randint(self.rect.y - 50,self.rect.y + 50)

    def update(self):
        self._move()
        self.rect.x = self.x

   

       



