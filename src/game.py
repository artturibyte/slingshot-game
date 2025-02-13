import pygame
from ball import Ball
from slingshot import Slingshot
from target import Target

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Slingshot Game")
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.ball = Ball(100, 500)
        self.slingshot = Slingshot(100, 500)
        self.targets = [Target(600, 500), Target(700, 400)]
        self.running = True
        self.ball_launched = False  # Flag to track if the ball has been launched
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self.score = 0  # Initialize score

    def start_screen(self):
        start = True
        while start:
            self.screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 74)
            text = font.render("Press Enter to Start", True, (0, 0, 0))
            self.screen.blit(text, (250, 250))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start = False

    def run(self):
        self.start_screen()
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
                if event.key in self.key_states and not self.ball_launched:
                    self.key_states[event.key] = True
                elif event.key == pygame.K_RETURN and not self.ball_launched:
                    angle, power = self.slingshot.release()
                    self.ball.launch(angle, power)
                    self.ball_launched = True  # Set the flag to indicate the ball has been launched
                elif event.key == pygame.K_r:  # Check for the "R" key to reset the ball
                    self.ball.reset(100, 500)
                    self.ball_launched = False  # Reset the flag when the ball is reset

            elif event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

    def update(self):
        if not self.ball_launched:
            if self.key_states[pygame.K_UP]:
                self.slingshot.stretch(0, -1)
            if self.key_states[pygame.K_DOWN]:
                self.slingshot.stretch(0, 1)
            if self.key_states[pygame.K_LEFT]:
                self.slingshot.stretch(-1, 0)
            if self.key_states[pygame.K_RIGHT]:
                self.slingshot.stretch(1, 0)

        self.ball.update()
        if self.ball.has_stopped() and self.ball_launched:
            self.ball.reset(100, 500)
            self.ball_launched = False

        for target in self.targets:
            if self.ball.check_collision(target):
                self.targets.remove(target)
                self.score += 1  # Increment score when a target is hit

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.slingshot.draw(self.screen)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        for target in self.targets:
            target.draw(self.screen)
        
        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()