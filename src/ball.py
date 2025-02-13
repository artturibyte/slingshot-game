from math import cos, sin
from target import Target

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.radius = 15  # Example radius for collision detection
        self.bounce_damping = 0.7  # Damping factor for bounce effect

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity[1] += 0.01  # Gravity effect

        # Check collision with ground
        if self.y + self.radius >= 600:  # Assuming the ground is at y = 600
            self.y = 600 - self.radius
            self.velocity[1] = -self.velocity[1] * self.bounce_damping

            # Apply damping to horizontal velocity as well
            self.velocity[0] *= self.bounce_damping

            # Stop the ball if the bounce is too small
            if abs(self.velocity[1]) < 0.1:
                self.velocity[1] = 0
                self.velocity[0] = 0

    def launch(self, angle, power):
        self.velocity[0] = power * cos(angle)
        self.velocity[1] = power * sin(angle)

    def check_collision(self, target: Target):
        # Check collision with rectangle target
        closest_x = max(target.x, min(self.x, target.x + target.width))
        closest_y = max(target.y, min(self.y, target.y + target.height))
        distance = ((self.x - closest_x) ** 2 + (self.y - closest_y) ** 2) ** 0.5
        return distance < self.radius

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]