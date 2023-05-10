import pygame
from src.scenes.menu_scene import MenuScene
from src.core.scene_manager import SceneManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    pygame.display.set_caption('Rock Paper Scissors')

    scene_manager = SceneManager()
    scene_manager.push_scene(MenuScene(screen, scene_manager))

    clock = pygame.time.Clock()

    while scene_manager.running:
        clock.tick(60)
        scene_manager.handle_events(pygame.event.get())
        scene_manager.update()
        scene_manager.render(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
