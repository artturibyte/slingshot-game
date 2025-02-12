import pygame
import math

class Slingshot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stretch_x = 0
        self.stretch_y = 0

    def stretch(self, dx, dy):
        self.stretch_x += dx
        self.stretch_y += dy

    def release(self):
        angle = math.atan2(self.stretch_y, self.stretch_x)
        power = math.sqrt(self.stretch_x ** 2 + self.stretch_y ** 2)
        self.stretch_x = 0
        self.stretch_y = 0
        return angle, power

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x + self.stretch_x, self.y + self.stretch_y), 5)