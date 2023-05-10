import pygame.mixer

def play_background_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)