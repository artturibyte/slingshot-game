import pygame
from ball import Ball
from slingshot import Slingshot
from target import Target
from time import sleep

# Constants for ball initial position
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 500

# Constants for screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Game constants
GROUND_HEIGHT = 550

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Slingshot Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot = Slingshot(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.targets = self.create_pyramid_targets(5, 600, GROUND_HEIGHT, 20, 10)
        self.running = True
        self.ball_launched = False  # Flag to track if the ball has been launched
        self.score = 0  # Initialize score

    def create_pyramid_targets(self, rows: int, start_x: int, start_y: int, width: int, height: int):
        targets = []
        offset = 5
        for row in range(rows):
            for col in range(rows - row):
                x = start_x + col * width + row * (width // 2) + col * offset
                y = start_y - row * height - row * offset - height
                targets.append(Target(x, y, width, height))
        return targets

    def start_screen(self):
        start = True
        while start:
            self.screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render("Press Enter to Start", True, BLACK)
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
        #self.start_screen()
        #sleep(0.5)
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        if pygame.event.get(pygame.QUIT): self.running = False
        keys = pygame.key.get_pressed()

        if not self.ball_launched:
            if keys[pygame.K_UP]: self.slingshot.stretch(0, -1)
            if keys[pygame.K_DOWN]: self.slingshot.stretch(0, 1)
            if keys[pygame.K_LEFT]: self.slingshot.stretch(-1, 0)
            if keys[pygame.K_RIGHT]: self.slingshot.stretch(1, 0)

            if keys[pygame.K_RETURN]:
                    angle, power = self.slingshot.release()
                    self.ball.launch(angle, power)
                    self.ball_launched = True  # Set the flag to indicate the ball has been launched
        
        if keys[pygame.K_r]:  # Check for the "R" key to reset the ball
                    self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
                    self.ball_launched = False  # Reset the flag when the ball is reset

    def update(self):
        # Update the ball's position if it has been launched
        if self.ball_launched:
            self.ball.update()

        # Check if the ball is out of bounds. Let ball roll little bit out of bounds before resetting.
        if (self.ball.x < 0 or self.ball.x > SCREEN_WIDTH + 100 or
            self.ball.y < 0 or self.ball.y > SCREEN_HEIGHT):
            sleep(0.5)
            self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
            self.ball_launched = False

        self.ball.check_ground_collision(GROUND_HEIGHT)
        if self.ball.has_stopped() and self.ball_launched:
            self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
            self.ball_launched = False

        for target in self.targets:
            if self.ball.check_collision(target):
                self.targets.remove(target)
                self.score += 1  # Increment score when a target is hit

    def draw(self):
        self.screen.fill(WHITE)
        self.slingshot.draw(self.screen)
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.circle(self.screen, RED, (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        for target in self.targets:
            target.draw(self.screen)
        
        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()