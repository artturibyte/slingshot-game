import pygame
from math import atan2, sqrt
from target import Target

def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {file_path}: {e}")
        return None

def scale_image(image, lenght):
    """Scale an image to the specified width and height."""
    original_width, original_height = image.get_size()
    scale_factor = lenght / original_width
    return pygame.transform.scale(image, (int(lenght), int(original_height * scale_factor)))


def load_sound(file_path):
    """Load a sound from the specified file path."""
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound at {file_path}: {e}")
        return None

def calculate_angle(start_pos, end_pos):
    """Calculate the angle between two vectors."""
    delta_x = end_pos[0] - start_pos[0]
    delta_y = end_pos[1] - start_pos[1]
    return atan2(delta_y, delta_x)

def calculate_length(start_pos, end_pos):
    """Calculate the length between two points."""
    delta_x = end_pos[0] - start_pos[0]
    delta_y = end_pos[1] - start_pos[1]
    return sqrt(delta_x ** 2 + delta_y ** 2)

def create_pyramid_targets(rows: int, start_x: int, start_y: int, block_width: int, block_height: int):
    targets = []
    offset = 5 # Offset between blocks
    for row in range(rows):
        for col in range(rows - row):
            x = start_x + col * block_width + row * (block_width // 2) + col * offset
            y = start_y - row * block_height - row * offset - block_height
            targets.append(Target(x, y, block_width, block_height))
    return targets