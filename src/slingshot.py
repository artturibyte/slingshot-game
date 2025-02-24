import pygame
import math
from utils import load_image, scale_image, calculate_length, calculate_angle

BLACK = (0, 0, 0)

class Slingshot:
    def __init__(self, x: int, y: int, max_length: int = 100):
        self.bucket_x = x
        self.bucket_y = y
        self.vector_x = 0
        self.vector_y = 0
        self.max_length = max_length
        self.ball_launched = False

        # Base coordinates
        self.base_x = self.bucket_x + 80
        self.base_y = self.bucket_y + 80

        self.boom_lenght = calculate_length([self.base_x, self.base_y], [self.bucket_x, self.bucket_y])

        # Load images
        self.slingshot_line_image = scale_image(load_image('assets/arm.png'), self.boom_lenght)
        self.excavator_image = scale_image(load_image('assets/excavator.png'), 120)

    def stretch(self, dx, dy):
        new_vector_x = self.vector_x + dx
        new_vector_y = self.vector_y + dy
        length = math.sqrt(new_vector_x ** 2 + new_vector_y ** 2)
        
        if length <= self.max_length:
            self.vector_x = new_vector_x
            self.vector_y = new_vector_y

    def release(self):
        angle = math.atan2(self.vector_y, self.vector_x)
        power = math.sqrt(self.vector_x ** 2 + self.vector_y ** 2) / 20 # divide by 20 to reduce the power
        self.vector_x = 0
        self.vector_y = 0
        return angle, power
    
    def reset(self, bucket_x, bucket_y):
        self.bucket_x = bucket_x
        self.bucket_y = bucket_y
        self.ball_launched = False

    def draw(self, screen):
        # Draw the excavator-like arm system
        angle = math.atan2(self.vector_y, self.vector_x)

        line_angle = calculate_angle([self.base_x, self.base_y], [self.bucket_x, self.bucket_y])

        if self.ball_launched:
            if line_angle < -0.1:
                new_angle = line_angle + 0.05
                self.bucket_x = self.base_x + self.boom_lenght * math.cos(new_angle)
                self.bucket_y = self.base_y + self.boom_lenght * math.sin(new_angle)
        

        # Rotate the image to match the angle of the slingshot line
        rotated_image = pygame.transform.rotate(self.slingshot_line_image, -math.degrees(line_angle))
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = ((self.base_x + self.bucket_x) // 2, (self.base_y + self.bucket_y) // 2)
        
        screen.blit(self.excavator_image, (self.base_x - 80, self.base_y - 60))
        screen.blit(rotated_image, rotated_rect.topleft)
        
        # Draw vector
        pygame.draw.line(screen, BLACK, (self.bucket_x, self.bucket_y), (self.bucket_x + self.vector_x, self.bucket_y + self.vector_y), 1)

        # Draw the arrowhead
        arrow_length = 5
        offset = 10  # Offset to draw the arrowhead further away
        end_x = self.bucket_x + self.vector_x + offset * math.cos(angle)
        end_y = self.bucket_y + self.vector_y + offset * math.sin(angle)
        left_x = end_x - arrow_length * math.cos(angle - math.pi / 6)
        left_y = end_y - arrow_length * math.sin(angle - math.pi / 6)
        right_x = end_x - arrow_length * math.cos(angle + math.pi / 6)
        right_y = end_y - arrow_length * math.sin(angle + math.pi / 6)
        pygame.draw.polygon(screen, BLACK, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])