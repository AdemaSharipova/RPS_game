import os

import pygame
from src.scenes.scene_interface import SceneInterface as Scene
from utils import colors
from utils.helpers import play_background_music


class WinnerScene(Scene):
    def __init__(self, screen, scene_manager, winner_object):
        self.scene_manager = scene_manager
        self.screen = screen
        self.winner_object = winner_object
        music_path = os.path.join('assets', 'songs', 'win_music.mp3')
        play_background_music(music_path)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.pop_scene()

    def update(self):
        pass

    def render(self, screen):
        screen.fill(colors.WHITE)
        winner_image = pygame.transform.scale(self.winner_object.image, (300, 300))
        screen_width, screen_height = screen.get_size()
        image_width, image_height = winner_image.get_size()
        screen.blit(winner_image, ((screen_width - image_width) // 2, (screen_height - image_height) // 2))

        font = pygame.font.Font(None, 72)
        text = font.render('Winner', True, colors.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, 100)
        screen.blit(text, text_rect)

        pygame.display.flip()

