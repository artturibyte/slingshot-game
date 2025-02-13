import pygame

class Target:
    def __init__(self, x, y, width, height, health=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health  # Initialize health
        self.color = (0, 255, 0)  # Initial color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def hit(self):
        self.health -= 1
        if self.health == 1:
            self.color = (255, 255, 0)  # Change color to yellow when health is 1
        elif self.health <= 0:
            self.color = (255, 0, 0)  # Change color to red when health is 0