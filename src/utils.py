import pygame
from math import atan2

def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {file_path}: {e}")
        return None

def load_sound(file_path):
    """Load a sound from the specified file path."""
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound at {file_path}: {e}")
        return None

def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(value, max_value))

def calculate_angle(start_pos, end_pos):
    """Calculate the angle between two positions."""
    delta_x = end_pos[0] - start_pos[0]
    delta_y = end_pos[1] - start_pos[1]
    return atan2(delta_y, delta_x)