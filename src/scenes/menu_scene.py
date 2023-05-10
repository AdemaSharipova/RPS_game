import os
import pygame.font

from src.scenes.scene_interface import SceneInterface as Scene
from src.scenes.game_scene import GameScene
from utils import colors
from utils.helpers import play_background_music


class MenuScene(Scene):
    """
    Inherited from Scene Interface with methods handle events, update, render.
    MenuScene is the first scene at this game.
    """

    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 36)
        screen_width, screen_height = screen.get_size()
        backgr_image_path = os.path.join('assets', 'images', 'background_image2.png')
        self.background_image = pygame.image.load(backgr_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

        self.start_button = pygame.Rect(
            (screen_width - 200) // 2,
            (screen_height - 50) // 2 - 70,
            200, 50
        )

        self.quit_button = pygame.Rect(
            (screen.get_width() - 200) // 2,
            (screen.get_height() - 50) // 2 ,
            200, 50
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.scene_manager.push_scene(GameScene(screen=self.screen, scene_manager=self.scene_manager))
                elif self.quit_button.collidepoint(event.pos):
                    self.scene_manager.running = False

    def update(self): ...

    def render(self, screen):
        screen.fill(colors.WHITE)
        screen.blit(self.background_image, (0, 0))

        # button rendering:
        self.render_button(screen, self.start_button, "Start Game")
        self.render_button(screen, self.quit_button, "Quit")

        pygame.display.flip()

    def render_button(self, screen, button, text):
        """
        Separate method for rendering button to not repeat the code
        """
        pygame.draw.rect(screen, colors.LIGHT_BLUE, button, border_radius=5)
        button_text = self.font.render(text, True, colors.BLACK)
        text_width, text_height = button_text.get_size()
        text_x = button.x + (button.width - text_width) // 2
        text_y = button.y + (button.height - text_height) // 2
        screen.blit(button_text, (text_x, text_y))




