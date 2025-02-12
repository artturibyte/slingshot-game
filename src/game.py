import pygame
from ball import Ball
from slingshot import Slingshot
from target import Target

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.bird = Ball(100, 500)
        self.slingshot = Slingshot(100, 500)
        self.targets = [Target(600, 500), Target(700, 400)]
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.slingshot.stretch(0, -1)
                    case pygame.K_DOWN:
                        self.slingshot.stretch(0, 1)
                    case pygame.K_LEFT:
                        self.slingshot.stretch(-1, 0)
                    case pygame.K_RIGHT:
                        self.slingshot.stretch(1, 0)
                    case pygame.K_RETURN:
                        angle, power = self.slingshot.release()
                        self.bird.launch(angle, power)

    def update(self):
        self.bird.update()
        for target in self.targets:
            if self.bird.check_collision(target):
                self.targets.remove(target)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.slingshot.draw(self.screen)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.bird.x), int(self.bird.y)), self.bird.radius)
        for target in self.targets:
            target.draw(self.screen)
        pygame.display.flip()