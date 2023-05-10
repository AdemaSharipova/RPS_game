import math
import os

import pygame
import random
import itertools
import pygame.mixer

from utils import colors
from src.core.game_objects import Rock, Paper, Scissors
from src.scenes.winner_scene import WinnerScene
from src.scenes.scene_interface import SceneInterface as Scene
from utils.helpers import play_background_music


class GameScene(Scene):
    def __init__(self, screen, scene_manager):
        self.scene_manager = scene_manager
        self.screen = screen
        # LayeredUpdates - gives an ability to draw object in order and updating all sprites
        self.game_object_group = pygame.sprite.LayeredUpdates()
        # object_counts for defining the winning type of object
        self.object_counts = {Rock: 0, Paper: 0, Scissors: 0}
        num_game_objects = 20
        self.generate_random_game_objects(num_game_objects)
        music_path = os.path.join('assets', 'songs', 'game_music.mp3')
        play_background_music(music_path)

        # backgr_img = os.path.join('assets', 'images', 'backgroung_game.png')
        # screen_width, screen_height = screen.get_size()
        # self.background_image = pygame.image.load(backgr_img)
        # self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

    def handle_events(self, events):
        # Press Escape => menu scene
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.pop_scene()

    def update(self):
        # updates all objects
        self.game_object_group.update(self.screen.get_width(), self.screen.get_height())

        # itertools.combinations() - for creating pairs of sprites
        for obj1, obj2 in itertools.combinations(self.game_object_group.sprites(), 2):
            if pygame.sprite.collide_rect(obj1, obj2):
                self.handle_collision(obj1, obj2)

        # define if all the objects in the screen are the same type
        if self.all_objects_same_type():

            # Stop all music
            pygame.mixer.music.stop()

            # deleting all objects
            self.game_object_group.empty()

            # Define the type of winning object
            winner = None

            for obj_class, count in self.object_counts.items():
                if count > 0:
                    winner = obj_class
                    break

            winner_obj = winner(0, 0)
            self.scene_manager.push_scene(WinnerScene(scene_manager=self.scene_manager, screen=self.screen, winner_object=winner_obj))

    def generate_random_game_objects(self, num_game_objects):
        object_classes = [Rock, Paper, Scissors]
        for _ in range(num_game_objects):
            # Random choose of object
            obj_class = random.choice(object_classes)
            screen_width, screen_height = self.screen.get_size()
            # Random chose of coordinates
            x, y = random.randint(50, screen_width - 50), random.randint(50, screen_height-50)
            obj = obj_class(x, y)
            self.game_object_group.add(obj)
            # Count number of each type of object
            self.object_counts[obj_class] += 1

    # When they collide, the loser turns to the winner
    def handle_collision(self, obj1, obj2):
        if isinstance(obj1, Rock) and isinstance(obj2, Scissors):
            self.transform_object(obj2, Rock)
        elif isinstance(obj1, Rock) and isinstance(obj2, Paper):
            self.transform_object(obj1, Paper)
        elif isinstance(obj1, Paper) and isinstance(obj2, Scissors):
            self.transform_object(obj1, Scissors)
        elif isinstance(obj1, Paper) and isinstance(obj2, Rock):
            self.transform_object(obj2, Paper)
        elif isinstance(obj1, Scissors) and isinstance(obj2, Rock):
            self.transform_object(obj1, Rock)
        elif isinstance(obj1, Scissors) and isinstance(obj2, Paper):
            self.transform_object(obj2, Scissors)

        # Calculate the new velocities after the collision
        new_velocity_obj1, new_velocity_obj2 = self.calculate_collision_velocity(obj1, obj2)
        obj1.velocity = new_velocity_obj1
        obj2.velocity = new_velocity_obj2

        # Reflects the movement of two objects based on their angle of collision.
        # Calculates the angle between the centers of obj1 and obj2 using the math.atan2() function
        # obj2.rect.centery - obj1.rect.centery:
        # Calculates the vertical distance between the centers of the two objects and the other one the horizontal
        angle = math.atan2(obj2.rect.centery - obj1.rect.centery, obj2.rect.centerx - obj1.rect.centerx)

        # Opposite direction
        obj1.velocity[0] += -math.cos(angle)
        obj1.velocity[1] += -math.sin(angle)
        obj2.velocity[0] += math.cos(angle)
        obj2.velocity[1] += math.sin(angle)

    def all_objects_same_type(self):
        self.object_counts = {
            Rock: 0,
            Paper: 0,
            Scissors: 0,
        }

        for obj in self.game_object_group.sprites():
            self.object_counts[type(obj)] += 1

        # if number of two types of objects == 0 => return True
        return (self.object_counts[Rock] == 0 and self.object_counts[Paper] == 0) or (
                self.object_counts[Rock] == 0 and self.object_counts[Scissors] == 0) or (
                self.object_counts[Paper] == 0 and self.object_counts[Scissors] == 0)

    def transform_object(self, obj, new_class):
        # Changing the object to the winning one
        obj.__class__ = new_class
        obj.image = pygame.image.load(new_class.IMAGE)
        obj.image = pygame.transform.scale(obj.image, (new_class.WIDTH, new_class.HEIGHT))
        obj.rect.width = new_class.WIDTH
        obj.rect.height = new_class.HEIGHT

    def calculate_collision_velocity(self, obj1, obj2):
        # Calculate the new velocities after the collision based on the objects' masses and velocities
        mass_sum = obj1.mass + obj2.mass
        new_velocity_obj1 = [
            (obj1.velocity[0] * (obj1.mass - obj2.mass) + 2 * obj2.mass * obj2.velocity[0]) / mass_sum,
            (obj1.velocity[1] * (obj1.mass - obj2.mass) + 2 * obj2.mass * obj2.velocity[1]) / mass_sum,
        ]
        new_velocity_obj2 = [
            (obj2.velocity[0] * (obj2.mass - obj1.mass) + 2 * obj1.mass * obj1.velocity[0]) / mass_sum,
            (obj2.velocity[1] * (obj2.mass - obj1.mass) + 2 * obj1.mass * obj1.velocity[1]) / mass_sum,
        ]

        return new_velocity_obj1, new_velocity_obj2

    def render(self, screen):
        screen.fill(colors.WHITE)
        # screen.blit(self.background_image, (0, 0))
        for obj in self.game_object_group.sprites():
            screen.blit(obj.image, obj.rect)
        pygame.display.flip()


