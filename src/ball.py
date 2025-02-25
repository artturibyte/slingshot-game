import pygame
from target import Target
from utils import calculate_length
from constants import BALL_RADIUS, BALL_INITIAL_X, BALL_INITIAL_Y

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = BALL_RADIUS
        
        self.position = pygame.math.Vector2(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.bounce_damping = 0.7  # Damping factor for bounce effect
        self.launched = False  # Flag to indicate if the ball has been launched

    def update(self):
        self.position += self.velocity
        self.velocity.y += 0.05  # Gravity effect
        self.rect.center = self.position

    def check_ground_collision(self, ground_height):
        min_bounce_speed = 0.05  # Minimum required speed for a bounce effect
        if self.position.y + self.radius >= ground_height:
            self.position.y = ground_height - self.radius
            self.velocity.y = -self.velocity.y * self.bounce_damping

            # Apply damping to horizontal velocity as well
            self.velocity.x *= self.bounce_damping

            # Stop the ball if the bounce is too small
            if abs(self.velocity.x) < min_bounce_speed:
                self.velocity = pygame.math.Vector2(0, 0)

    def launch(self, angle, power):
        # Set X value to amount of power and rotate.
        self.velocity.x = power
        self.velocity.rotate_rad_ip(angle)
        self.launched = True  # Set the flag to indicate the ball has been launched

    def check_collision(self, target: Target):
        # Check collision with rectangle target
        closest_x = max(target.rect.left, min(self.position.x, target.rect.right))
        closest_y = max(target.rect.top, min(self.position.y, target.rect.bottom))
        distance = calculate_length([self.position.x, self.position.y], [closest_x, closest_y])
        
        if distance < self.radius:
            # Calculate the normal vector
            normal = pygame.math.Vector2(self.position.x - closest_x, self.position.y - closest_y).normalize()
            
            # Reflect the velocity vector
            dot_product = self.velocity.dot(normal)
            self.velocity -= 2 * dot_product * normal

            # Apply damping to the velocity
            self.velocity *= self.bounce_damping
            
            return True
        return False

    def reset(self):
        self.position.xy = BALL_INITIAL_X, BALL_INITIAL_Y
        self.velocity.xy = 0, 0
        self.launched = False  # Reset the flag when the ball is reset
        self.rect.center = self.position

    def has_stopped(self):
        return self.velocity.length() == 0