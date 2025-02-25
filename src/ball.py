from math import cos, sin
from target import Target
from utils import calculate_length

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.radius = 5  # Example radius for collision detection
        self.bounce_damping = 0.7  # Damping factor for bounce effect
        self.launched = False  # Flag to indicate if the ball has been launched

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity[1] += 0.05  # Gravity effect

    def check_ground_collision(self, ground_height):
        min_bounce_speed = 0.05  # Minimum required speed for a bounce effect
        if self.y + self.radius >= ground_height:
            self.y = ground_height - self.radius
            self.velocity[1] = -self.velocity[1] * self.bounce_damping

            # Apply damping to horizontal velocity as well
            self.velocity[0] *= self.bounce_damping

            # Stop the ball if the bounce is too small
            if abs(self.velocity[0]) < min_bounce_speed:
                self.velocity[1] = 0
                self.velocity[0] = 0

    def launch(self, angle, power):
        self.velocity[0] = power * cos(angle)
        self.velocity[1] = power * sin(angle)
        self.launched = True  # Set the flag to indicate the ball has been launched

    def check_collision(self, target: Target):
        # Check collision with rectangle target
        closest_x = max(target.rect.left, min(self.x, target.rect.x + target.rect.width))
        closest_y = max(target.rect.y, min(self.y, target.rect.y + target.rect.width))
        distance = calculate_length([self.x, self.y], [closest_x, closest_y])
        
        if distance < self.radius:
            # Calculate the normal vector
            normal_x = (self.x - closest_x) / distance
            normal_y = (self.y - closest_y) / distance
            
            # Reflect the velocity vector
            dot_product = self.velocity[0] * normal_x + self.velocity[1] * normal_y
            self.velocity[0] -= 2 * dot_product * normal_x
            self.velocity[1] -= 2 * dot_product * normal_y

            # Apply damping to the velocity
            self.velocity[0] *= self.bounce_damping
            self.velocity[1] *= self.bounce_damping 
            
            return True
        return False

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.launched = False  # Reset the flag when the ball is reset

    def has_stopped(self):
        return self.velocity[0] == 0 and self.velocity[1] == 0