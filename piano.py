import pygame
import os
import random

class Piano:
    def __init__(self):
        self.piano_sounds_folder = "audio/Keys"
        self.piano_sounds = [pygame.mixer.Sound(os.path.join(self.piano_sounds_folder, f))\
            for f in os.listdir(self.piano_sounds_folder)] 
        
    def play_random_piano_sound(self):
        random.choice(self.piano_sounds).play()
