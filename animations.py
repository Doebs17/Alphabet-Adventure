import os
import pygame
import random

class Animation:
    def __init__(self,fw_game, screen, directory_path, duration_per_frame, image_animator, padding):
        self.screen = screen
        self.animation_text_position = fw_game.animation_text_position
        self.frames = self._load_frames(directory_path)
        self.current_frame_index = 0
        self.current_frame = self.frames[self.current_frame_index]
        self.duration_per_frame = duration_per_frame
        self.last_update = pygame.time.get_ticks()
        self.is_playing = False
        self.image_animator = image_animator
        self.animation_types =fw_game.image_animations
        self.image_padding = padding

    def _load_frames(self, directory_path):
        frames = []
        for file_name in sorted(os.listdir(directory_path)):
            if file_name.endswith('.png'):
                image_path = os.path.join(directory_path, file_name)
                frames.append(pygame.image.load(image_path).convert_alpha())
        return frames

    def update(self):
        if not self.image_animator.is_animating and self.is_playing and not self.image_animator.image_animation_complete:
            random_image_animation = random.choice(self.animation_types)
            self.image_animator.start_animation(self.current_frame, self.animation_text_position, random_image_animation, self.image_padding ) 
            self.image_animator.initial_animation_complete = False
        elif self.is_playing:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.duration_per_frame:
                self.current_frame_index += 1
                if self.current_frame_index >= len(self.frames):
                    self.current_frame_index = 0  

                self.current_frame = self.frames[self.current_frame_index]
                self.last_update = now
             
    def draw(self, position):
        if not self.image_animator.is_animating and self.current_frame and not self.image_animator.initial_animation_complete:
            self.screen.blit(self.current_frame, position)

    def start(self):
        self.is_playing = True

    def stop(self, image_padding = 0):
        self.is_playing = False
        self.current_frame_index = 0
        self.current_frame = self.frames[self.current_frame_index]
        # self.current_frame_index = 0

    def draw_last_frame(self, image_padding):
        # Get the position where the last frame should be draw
        image_height = self.current_frame.get_height()
        new_y_position = self.animation_text_position[1] - image_height - 60 + image_padding
        position = (self.animation_text_position[0] - self.current_frame.get_width() // 2, new_y_position)
        # Blit the last frame onto the screen at the desired position
        self.screen.blit(self.current_frame, position)
