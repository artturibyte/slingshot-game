import pygame
import math

class Slingshot:
    def __init__(self, x: int, y: int):
        self.x_origin = x
        self.y_origin = y
        self.stretch_x = 0
        self.stretch_y = 0

    def stretch(self, dx, dy):
        self.stretch_x += dx
        self.stretch_y += dy

    def release(self):
        angle = math.atan2(self.stretch_y, self.stretch_x)
        power = math.sqrt(self.stretch_x ** 2 + self.stretch_y ** 2) / 30
        self.stretch_x = 0
        self.stretch_y = 0
        return angle, power

    def draw(self, screen):
        # Draw the slingshot line
        pygame.draw.line(screen, (0, 0, 0), (self.x_origin, self.y_origin), (self.x_origin + self.stretch_x, self.y_origin + self.stretch_y), 1)
        
        # Draw the arrowhead
        angle = math.atan2(self.stretch_y, self.stretch_x)
        arrow_length = 5
        offset = 10  # Offset to draw the arrowhead further away
        end_x = self.x_origin + self.stretch_x + offset * math.cos(angle)
        end_y = self.y_origin + self.stretch_y + offset * math.sin(angle)
        left_x = end_x - arrow_length * math.cos(angle - math.pi / 6)
        left_y = end_y - arrow_length * math.sin(angle - math.pi / 6)
        right_x = end_x - arrow_length * math.cos(angle + math.pi / 6)
        right_y = end_y - arrow_length * math.sin(angle + math.pi / 6)
        pygame.draw.polygon(screen, (0, 0, 0), [(end_x, end_y), (left_x, left_y), (right_x, right_y)])