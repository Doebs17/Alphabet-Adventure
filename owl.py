import pygame

class Owl:

    def __init__(self, fw_game):
        self.screen = fw_game.screen
        self.settings = fw_game.settings
        self.screen_rect = fw_game.screen.get_rect()

        # Load the owl images and get their rects
        self.image_eyes_open = pygame.image.load('images/owl_eyes_Open.png')
        self.image_eyes_closed = pygame.image.load('images/owl_eyes_Closed.png')  # Assuming you named the other image this way
        self.rect = self.image_eyes_open.get_rect()

        # Positioning the owl on the screen
        self.rect.x = 140
        self.rect.y = 600

        # Initialize counter for blinking and set the current image to eyes_open
        self.blink_counter = 0
        self.current_image = self.image_eyes_open

    def update(self):
        """Update the owl's blinking state"""
        self.blink_counter += 1

        # Every 100 frames, blink the owl for 5 frames by closing its eyes
        if self.blink_counter % 100 < 5:
            self.current_image = self.image_eyes_closed
        else:
            self.current_image = self.image_eyes_open

        # Reset the counter to avoid potential overflow
        if self.blink_counter > 500:
            self.blink_counter = 0

    def draw(self):
        """Draw the current state of the owl on the screen"""
        self.screen.blit(self.current_image, self.rect)