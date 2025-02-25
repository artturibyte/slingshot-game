import pygame
import math
from utils import load_image, scale_image, calculate_length, calculate_angle
from constants import BLACK

class Slingshot:
    def __init__(self, x: int, y: int, max_length: int = 100):
        self.bucket_pos = pygame.math.Vector2(x, y)
        self.vector = pygame.math.Vector2(0, 0)
        self.max_length = max_length
        self.ball_launched = False

        # Base coordinates
        self.base_pos = pygame.math.Vector2(self.bucket_pos.x + 80, self.bucket_pos.y + 80)

        self.boom_length = calculate_length([self.base_pos.x, self.base_pos.y], [self.bucket_pos.x, self.bucket_pos.y])

        # Load images
        self.slingshot_line_image = scale_image(load_image('assets/arm.png'), self.boom_length)
        self.excavator_image = scale_image(load_image('assets/excavator.png'), 120)

    def stretch(self, dx, dy):
        new_vector = self.vector + pygame.math.Vector2(dx, dy)
        if new_vector.length() <= self.max_length:
            self.vector = new_vector

    def release(self):
        angle = math.atan2(self.vector.y, self.vector.x)
        power = self.vector.length() / 20  # divide by 20 to reduce the power
        self.vector = pygame.math.Vector2(0, 0)
        return angle, power
    
    def reset(self, bucket_x, bucket_y):
        self.bucket_pos = pygame.math.Vector2(bucket_x, bucket_y)
        self.ball_launched = False

    def draw(self, screen):
        # Draw the excavator-like arm system
        angle = math.atan2(self.vector.y, self.vector.x)

        line_angle = calculate_angle([self.base_pos.x, self.base_pos.y], [self.bucket_pos.x, self.bucket_pos.y])

        if self.ball_launched:
            if line_angle < -0.1:
                new_angle = line_angle + 0.05
                self.bucket_pos.x = self.base_pos.x + self.boom_length * math.cos(new_angle)
                self.bucket_pos.y = self.base_pos.y + self.boom_length * math.sin(new_angle)
        
        # Rotate the image to match the angle of the slingshot line
        rotated_image = pygame.transform.rotate(self.slingshot_line_image, -math.degrees(line_angle))
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = ((self.base_pos.x + self.bucket_pos.x) // 2, (self.base_pos.y + self.bucket_pos.y) // 2)
        
        screen.blit(self.excavator_image, (self.base_pos.x - 80, self.base_pos.y - 60))
        screen.blit(rotated_image, rotated_rect.topleft)
        
        # Draw vector
        pygame.draw.line(screen, BLACK, (self.bucket_pos.x, self.bucket_pos.y), (self.bucket_pos.x + self.vector.x, self.bucket_pos.y + self.vector.y), 1)

        # Draw the arrowhead
        arrow_length = 5
        offset = 10  # Offset to draw the arrowhead further away
        end_pos = self.bucket_pos + self.vector + pygame.math.Vector2(offset * math.cos(angle), offset * math.sin(angle))
        left_pos = end_pos - pygame.math.Vector2(arrow_length * math.cos(angle - math.pi / 6), arrow_length * math.sin(angle - math.pi / 6))
        right_pos = end_pos - pygame.math.Vector2(arrow_length * math.cos(angle + math.pi / 6), arrow_length * math.sin(angle + math.pi / 6))
        pygame.draw.polygon(screen, BLACK, [end_pos, left_pos, right_pos])