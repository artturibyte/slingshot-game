from math import cos, sin

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.radius = 15  # Example radius for collision detection

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #self.velocity[1] += 0.5  # Gravity effect

    def launch(self, angle, power):
        self.velocity[0] = power * cos(angle)
        self.velocity[1] = power * sin(angle)

    def check_collision(self, target):
        distance = ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5
        return distance < self.radius + target.radius

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]