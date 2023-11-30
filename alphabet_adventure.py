import os
import sys
import pygame
from settings import Settings
from text_animator import TextAnimator
from image_animator import ImageAnimator
from background import Background
from clouds import Cloud
from animations import Animation
import random
from button import Button
from banner import Banner

class Alphabet_Adventure():

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(5)
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(0.5)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        center_x, center_y = self.screen.get_rect().center
        pygame.display.set_caption("Ayla's First Words")
        self.screen_width = self.screen.get_width()   
        self.settings = Settings()
        font = pygame.font.SysFont(self.settings.font, self.settings.font_size)
        self.font_height = font.get_height()
        
        self.background = Background(self.screen)
        self.background.draw_gradient_background() 
        
        self.clouds = pygame.sprite.Group()
        self._create_sky()
        self._update_clouds()

        self.play_button = Button(self, "Play",(center_x,center_y))
        self.banner_two = Banner(self, "Alphabet Adventure", (center_x,center_y - 175))
        self.banner_one = Banner(self, "Ayla's", (center_x,center_y - 200 - self.banner_two.height))
        
        self.eyes_open_path = Alphabet_Adventure.resource_path('images/owl_eyes_Open.png')
        self.eyes_closed_path = Alphabet_Adventure.resource_path('images/owl_eyes_Closed.png')
        self.image_eyes_open = pygame.image.load(self.eyes_open_path)
        self.image_eyes_closed = pygame.image.load(self.eyes_closed_path)  # Assuming you named the other image this way
        self.owl_rect = self.image_eyes_open.get_rect()
        self.owl_rect.x = 140
        self.owl_rect.y = 600
        self.blink_counter = 0
        self.owl_current_image = self.image_eyes_open
        
        pygame.display.flip()

        self.word_info  = None
        self.current_display_type = None
        self.animation_text_position = (800,700)
        
        self.piano_sounds_folder = Alphabet_Adventure.resource_path("Audio/Keys")
        self.piano_sounds = [pygame.mixer.Sound(os.path.join(self.piano_sounds_folder, f))\
            for f in os.listdir(self.piano_sounds_folder)] 

        self.text_animator = TextAnimator(self, self.screen)
        self.image_animator = ImageAnimator(self, self.screen)
        self.image_animations = ['slide_down','fade_in']  

        self.directions_playing = False
        self.game_active = False
        self.voice_played = False
        self.sound_played = False
        self.sound_playing = False
        self.image_animation_played = False
        self.processing_key = False
        self.animation_end_image = False

        self.sound_duration = 0
        self.start_time = 0

        self.words_dictionary = {
            pygame.K_a: {"word": "Ayla", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/A_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/A_applause.wav"),"image_padding": int(+230), "end_condition": "continue_animation" },
            pygame.K_b: {"word": "Bee", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/B_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/B_Buzz.wav"),"image_padding": int(-20), "end_condition": "stop_animation" },
            pygame.K_c: {"word": "Cat", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/C_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/C_Meow.wav"),"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_d: {"word": "Daddy", "display_type": "image", "path":Alphabet_Adventure.resource_path("Images\Daddy.png") ,"voice": Alphabet_Adventure.resource_path("Audio/D_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/D_daddy.mp3"), "image_padding": int(-30),"end_condition": None },
            pygame.K_e: {"word": "Elephant", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/E_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/E_Elephant.wav"),"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_f: {"word": "Frog", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/F_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/F_frog.mp3"),"image_padding": int(-20),"end_condition": "stop_animation"},
            pygame.K_g: {"word": "Giraffe", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/G_Audio.mp3"), "sound":None,"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_h: {"word": "Horse", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/H_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/H_horse.wav"),"image_padding": int(+100),"end_condition": "continue_animation"},
            pygame.K_i: {"word": "Ice cream", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/I_Audio.mp3"), "sound":None,"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_j: {"word": "Jellyfish", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/J_Audio.mp3"), "sound":None,"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_k: {"word": "Kitten", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/K_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/K_kitten.mp3"),"image_padding": int(-20),"end_condition": "stop_animation"},
            pygame.K_l: {"word": "Lion", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/L_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/L_lion.wav"),"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_m: {"word": "Mommy", "display_type": "image", "path":Alphabet_Adventure.resource_path("Images\Mommy.png") ,"voice": Alphabet_Adventure.resource_path("Audio/M_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/M_mommy.mp3"), "image_padding": int(-30),"end_condition": None},
            pygame.K_n: {"word": "Nurse", "display_type": "image", "path":Alphabet_Adventure.resource_path("Images\\Nurse.png") ,"voice": Alphabet_Adventure.resource_path("Audio/N_Audio.mp3"), "sound":None, "image_padding": int(-30),"end_condition": None},
            pygame.K_o: {"word": "Owl", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/O_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/O_owl.wav"),"image_padding": int(+10),"end_condition": "stop_animation"},
            pygame.K_p: {"word": "Pig", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/P_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/P_pig.mp3"),"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_q: {"word": "Quack", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/Q_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/Q_quack.wav"),"image_padding": int(+60),"end_condition": "stop_animation"},
            pygame.K_r: {"word": "Robot", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/R_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/R_robot.wav"),"image_padding": int(-20),"end_condition": "stop_animation"},
            pygame.K_s: {"word": "Sheep", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/S_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/S_sheep.wav"),"image_padding": int(-20),"end_condition": "continue_animation"},
            pygame.K_t: {"word": "Tree", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/T_Audio.mp3"), "sound":None, "image_padding": int(55),"end_condition": "continue_animation" },
            pygame.K_u: {"word": "Unicorn", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/U_Audio.mp3"), "sound":None,"image_padding": int(+200),"end_condition": "continue_animation"},
            pygame.K_v: {"word": "Violin", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/V_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/V_violin.wav"),"image_padding": int(-20),"end_condition": "stop_animation"},
            pygame.K_w: {"word": "Wolf", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/W_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/W_wolf.wav"),"image_padding": int(+30),"end_condition": "stop_animation"},
            pygame.K_x: {"word": "X-ray", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/X_Audio.mp3"), "sound":None,"image_padding": int(-40),"end_condition": "continue_animation"},
            pygame.K_y: {"word": "Yacht", "display_type": "animation", "voice": Alphabet_Adventure.resource_path("Audio/Y_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/Y_yacht.wav"),"image_padding": int(+70),"end_condition": "continue_animation"},
            pygame.K_z: {"word": "Zebra","display_type":"image", "path": Alphabet_Adventure.resource_path("Images/zebraT.png"), "voice": Alphabet_Adventure.resource_path("Audio/Z_Audio.mp3"), "sound":Alphabet_Adventure.resource_path("Audio/Sounds/Z_zebra.mp3"),"image_padding": int(-10),"end_condition": None},
        }

        self.Ayla_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\\Ayla"), 100, self.image_animator, self.words_dictionary[pygame.K_a]["image_padding"])
        self.bee_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\\Bee"), 100, self.image_animator, self.words_dictionary[pygame.K_b]["image_padding"])
        self.cat_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Cat"), 100, self.image_animator, self.words_dictionary[pygame.K_c]["image_padding"])
        self.elephant_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Elephant"), 100, self.image_animator, self.words_dictionary[pygame.K_e]["image_padding"])
        self.frog_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Frog"), 100, self.image_animator,self.words_dictionary[pygame.K_f]["image_padding"])
        self.giraffe_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Giraffe"), 100, self.image_animator,self.words_dictionary[pygame.K_g]["image_padding"])
        self.horse_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Horse"), 100, self.image_animator,self.words_dictionary[pygame.K_h]["image_padding"])
        self.ice_cream_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Ice_cream"), 100, self.image_animator,self.words_dictionary[pygame.K_i]["image_padding"])
        self.jellyfish_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Jellyfish"), 100, self.image_animator,self.words_dictionary[pygame.K_j]["image_padding"])
        self.kitten_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Kitten"), 100, self.image_animator,self.words_dictionary[pygame.K_k]["image_padding"])
        self.lion_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Lion"), 100, self.image_animator,self.words_dictionary[pygame.K_l]["image_padding"])
        self.owl_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Owl"), 100, self.image_animator,self.words_dictionary[pygame.K_o]["image_padding"])
        self.pig_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Pig"), 100, self.image_animator,self.words_dictionary[pygame.K_p]["image_padding"])
        self.quack_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Quack"), 100, self.image_animator,self.words_dictionary[pygame.K_q]["image_padding"])
        self.robot_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Robot"), 100, self.image_animator,self.words_dictionary[pygame.K_r]["image_padding"])
        self.sheep_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Sheep"), 100, self.image_animator,self.words_dictionary[pygame.K_s]["image_padding"])
        self.tree_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Tree"), 100, self.image_animator,self.words_dictionary[pygame.K_t]["image_padding"])
        self.unicorn_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\\Unicorn"), 100, self.image_animator,self.words_dictionary[pygame.K_u]["image_padding"])
        self.violin_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Violin"), 100, self.image_animator,self.words_dictionary[pygame.K_v]["image_padding"])
        self.wolf_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Wolf"), 100, self.image_animator,self.words_dictionary[pygame.K_w]["image_padding"])
        self.x_ray_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\X-ray"), 100, self.image_animator,self.words_dictionary[pygame.K_x]["image_padding"])
        self.yacht_animation = Animation(self,self.screen, Alphabet_Adventure.resource_path("Images\Yacht"), 100, self.image_animator,self.words_dictionary[pygame.K_y]["image_padding"])   
        
        self.Ayla_animation.name = 'Ayla'
        self.bee_animation.name = 'Bee'
        self.cat_animation.name = 'Cat'
        self.elephant_animation.name = 'Elephant'
        self.frog_animation.name = 'Frog'
        self.giraffe_animation.name = 'Giraffe'
        self.horse_animation.name = 'Horse'
        self.ice_cream_animation.name = 'Ice cream'
        self.jellyfish_animation.name = 'Jellyfish'
        self.kitten_animation.name = 'Kitten'
        self.lion_animation.name = 'Lion'
        self.owl_animation.name = 'Owl'
        self.pig_animation.name = 'Pig'
        self.quack_animation.name = 'Quack'
        self.robot_animation.name = 'Robot'
        self.sheep_animation.name = 'Sheep'
        self.tree_animation.name = 'Tree'
        self.unicorn_animation.name = 'Unicorn'
        self.violin_animation.name = 'Violin'
        self.wolf_animation.name = 'Wolf'
        self.yacht_animation.name = 'Yacht'
        self.x_ray_animation.name = 'X-ray'
        
        self.animations = [self.Ayla_animation,self.tree_animation, self.cat_animation,self.bee_animation, \
            self.elephant_animation,self.frog_animation,self.giraffe_animation,self.horse_animation, \
            self.ice_cream_animation,self.jellyfish_animation,self.kitten_animation,self.lion_animation, \
            self.owl_animation, self.pig_animation, self.quack_animation,self.robot_animation,self.sheep_animation,\
            self.unicorn_animation,self.violin_animation, self.wolf_animation, self.x_ray_animation, self.yacht_animation]
        
        self.current_animation = None

    def run_game(self):
        """Start the main loop for the game"""

        while True:
            self._check_events()
            if self.game_active:
                self._check_voice_complete()
                self._check_sound_complete()
                self._check_directions_complete()
                self._check_processing_complete() 
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.game_active:
                    if 'a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z' or event.key == pygame.K_ESCAPE:
                        if event.unicode.isalpha():
                            self._play_random_piano_sound()           
                        if not self.processing_key:
                            self._check_keydown_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
         
    def _check_keydown_events(self,event): 
           
        if not self.directions_playing and event.key in self.words_dictionary and not self.processing_key:
            self.processing_key = True
            if self.word_info:
                self.stop_animation_for_word(self.current_word)
            self._clear_animation_vars()    
            self.word_info  = self.words_dictionary[event.key]
            self.current_word = self.word_info['word']
            self._run_voice()
            self.text_animator.start_animation(self.word_info['word'], self.animation_text_position)
            self.voice_played = False

    def _check_play_button(self, mouse_pos):
        button_clicked =  self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            self._clear_animation_vars()               
            self.game_active = True
            pygame.mouse.set_visible(False)
            self._run_Directions()
    
    def _clear_animation_vars(self):
        self.image_animator.current_image = None
        self.image_animator.image_animation_complete = False
        self.image_animation_played  = False
        self.current_display_type = None
        self.text_animator.current_text = None 
        self.text_animator.alpha = 0
        self.text_animator.draw_underline = False
        self.voice_played = False
        self.sound_played = False
        self.current_animation = None
        self.animation_end_image = False
        
    def _check_voice_complete(self):
        if not pygame.mixer.get_busy() and self.word_info:
            if self.word_info['display_type'] == 'image' and not self.image_animator.is_animating and not self.voice_played:
                self.current_display_type = 'image'
                image = pygame.image.load(self.word_info['path']).convert_alpha()
                new_position = (self.animation_text_position[0], self.animation_text_position[1])
                random_image_animation = random.choice(self.image_animations)
                self.image_animator.start_animation(image, new_position,random_image_animation,self.word_info['image_padding'] )
                self.voice_played = True
            elif self.word_info['display_type'] == 'animation' and not self.image_animation_played :
                # Call the appropriate animation based on the word_info['path'] or some other mechanism
                self.current_display_type = 'animation'
                self.start_animation_for_word(self.word_info['word'])
                self.voice_played = True
                self.image_animation_played  = True
            elif not self.image_animator.is_animating and self.voice_played and not self.sound_played and self.word_info['sound']:
                # Play the sound once the image or animation finishes
                self._run_sound()
                self.sound_played  = True

    def _check_sound_complete(self):
        if self.processing_key and self.sound_playing:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000.0
            if elapsed_time >= self.sound_duration:
                self.processing_key = False
                self.sound_playing = False
                if self.word_info["end_condition"] == "stop_animation":
                    self.stop_animation_for_word(self.current_word)

    # checks for the end of the image animation when there's no sound
    def _check_processing_complete(self):
        if self.word_info and (self.word_info.get('sound') is None):
            if self.image_animator.image_animation_complete:
                self.processing_key = False

    def _play_random_piano_sound(self):
        random.choice(self.piano_sounds).play()

    def _create_sky(self):
        cloud_list = [
            Alphabet_Adventure.resource_path('images/cloud1.png'),
            Alphabet_Adventure.resource_path('images/cloud2.png'),
            Alphabet_Adventure.resource_path('images/cloud3.png'),
            Alphabet_Adventure.resource_path('images/cloud4.png')
        ]

        random_cloud = random.choice(cloud_list)
        cloud = Cloud(self,random_cloud)
        cloud_width = cloud.image.get_rect().width
        cloud_height = cloud.image.get_rect().height
        current_x, current_y = 0,0

        while current_y < 450: ########Fix this to use animation_text_position
            while current_x < self.screen_width + cloud_width //2:
                y_variation = random.randint(-50, 40)
                adjusted_y = max(0, current_y + y_variation)  # Ensure y_position is not below 0
                self._create_clouds(current_x + random.randint(-100, 100), adjusted_y)
                current_x += cloud_width * 2
            current_x = 0
            current_y += cloud_height 

    def _create_clouds(self, x_position, y_position):
        cloud_list = [
            Alphabet_Adventure.resource_path('images/cloud1.png'),
            Alphabet_Adventure.resource_path('images/cloud2.png'),
            Alphabet_Adventure.resource_path('images/cloud3.png'),
            Alphabet_Adventure.resource_path('images/cloud4.png')
        ]

        random_cloud = random.choice(cloud_list)
        new_cloud = Cloud(self,random_cloud)
        new_cloud.x = x_position
        new_cloud.rect.x = x_position
        new_cloud.rect.y = y_position
        self.clouds.add(new_cloud)

    def _update_clouds(self):
        self.clouds.update()
        self.clouds.draw(self.screen)

    def _update_owl(self):
        """Update the owl's blinking state"""
        self.blink_counter += 1

        # Every 100 frames, blink the owl for 5 frames by closing its eyes
        if self.blink_counter % 100 < 5:
            self.owl_current_image = self.image_eyes_closed
        else:
            self.owl_current_image = self.image_eyes_open

        # Reset the counter to avoid potential overflow
        if self.blink_counter > 500:
            self.blink_counter = 0

    def _draw_owl(self):
        """Draw the current state of the owl on the screen"""
        self.screen.blit(self.owl_current_image, self.owl_rect)

    def _run_voice(self):
        voice_path = self.word_info["voice"]
        voice = pygame.mixer.Sound(voice_path)
        channel = pygame.mixer.Channel(1)  # Use a specific channel
        if channel :
            channel.play(voice)
        else:
            print("No available channels to play sound")

    def _run_Directions(self):
        directions_path = Alphabet_Adventure.resource_path("audio\\Directions.mp3")
        voice = pygame.mixer.Sound(directions_path)
        channel = pygame.mixer.Channel(2)  # Use a specific channel
        if channel :
            channel.play(voice)
        else:
            print("No available channels to play sound")
        self.directions_playing = True

    def _check_directions_complete(self):
        # Get the channel 2 object
        channel_2 = pygame.mixer.Channel(2)

        # Check if the channel is busy
        if not channel_2.get_busy():
            # Channel 2 is not playing anything, directions have finished
            self.directions_playing = False

    def start_animation_for_word(self, word):
        for animation in self.animations:
            if animation.name == word:  # Assume each animation has a 'name' attribute
                animation.start()
                self.current_animation = animation

    def _update_animations(self):
        for animation in self.animations:
            if animation.is_playing:
                first_frame = animation.frames[0]
                animation.update()
                image_height = first_frame.get_height()
                new_y_position = self.animation_text_position[1] - image_height - 60 + self.word_info['image_padding']
                animation.draw((self.animation_text_position[0] - first_frame.get_width() // 2, new_y_position))
            elif self.animation_end_image and animation == self.current_animation:
                animation.draw_last_frame(self.word_info['image_padding'])

    def stop_animation_for_word(self, word):
        for animation in self.animations:
            if animation.name == word:
                animation.stop(self.word_info['image_padding'])
                self.animation_end_image = True

    def _run_sound(self):     
        sound_path = self.word_info ["sound"]
        sound = pygame.mixer.Sound(sound_path)
        self.sound_duration = sound.get_length()
        channel = pygame.mixer.Channel(1) 
        if channel:
            channel.play(sound)  
            self.start_time = pygame.time.get_ticks()
            self.sound_playing = True
        else:
            print("No available channels to play sound")
       
    def _update_screen(self):
        self.background.draw_gradient_background()
        self._update_clouds()
        self.text_animator.update()
        self.text_animator.draw()
        self.image_animator.update()
        self.image_animator.draw(self.current_display_type)
        if self.word_info:
            self._update_animations()
        self._update_owl()
        self._draw_owl()

        if not self.game_active:
            self.play_button.draw_button()
            self.banner_one.draw_banner()
            self.banner_two.draw_banner()
        
        pygame.display.flip()

if __name__ == '__main__':
    fw = Alphabet_Adventure()
    fw.run_game()


