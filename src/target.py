import pygame
from constants import TARGET_WIDTH, TARGET_HEIGHT

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, health=2):
        super().__init__()
        self.image = pygame.Surface((TARGET_WIDTH, TARGET_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health  # Initialize health
        self.update_color()

    def update_color(self):
        if self.health == 2:
            self.image.fill((0, 255, 0))  # Green
        elif self.health == 1:
            self.image.fill((255, 255, 0))  # Yellow
        elif self.health <= 0:
            self.image.fill((255, 0, 0))  # Red

    def update(self):
        # This method can be used to update the sprite's state
        pass

    def hit(self):
        self.health -= 1
        self.update_color()