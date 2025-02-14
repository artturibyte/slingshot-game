import pygame
from ball import Ball
from slingshot import Slingshot
from target import Target
from time import sleep
from typing import List

# Constants for ball initial position
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 500

# Constants for screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Game constants
GROUND_HEIGHT = 550

# Constants for colors
SKY_BLUE = (52, 158, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Slingshot Game")
        self.exit_game = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot = Slingshot(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.targets: List[Target]
        self.running = True
        self.ball_launched = False  # Flag to track if the ball has been launched
        self.score = 0  # Initialize score
        self.ball_count = 5  # Initialize ball count 

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

    def game_over_screen(self):
        game_over = True
        while game_over:
            pygame.event.clear()
            self.screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, BLACK)
            self.screen.blit(text, (350, 250))
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (350, 350))
            restart_text = font.render("Press Enter to Restart", True, BLACK)
            self.screen.blit(restart_text, (250, 450))
            pygame.display.flip()
            sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_RETURN:
                        game_over = False

    def reset_game(self):
        self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.ball_launched = False
        self.score = 0
        self.ball_count = 5
        self.targets = self.create_pyramid_targets(5, 600, GROUND_HEIGHT, 20, 10) + self.create_pyramid_targets(3, 500, GROUND_HEIGHT, 20, 10)
        self.running = True

    def run(self):
        while not self.exit_game:
            #self.start_screen()
            self.reset_game()
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
            self.game_over_screen()
        pygame.quit()

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

        if self.ball_launched:
            if keys[pygame.K_r]:  # Check for the "R" key to reset the ball
                self.reset_ball()
    
    def reset_ball(self):
        self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.ball_launched = False
        self.ball_count -= 1  # Decrement ball_count when the ball is reset

    def update(self):
        if self.ball_count == 0:
            self.running = False

        # Update the ball's position if it has been launched
        if self.ball_launched:
            self.ball.update()

        # Check if the ball is out of bounds. Let ball roll little bit out of bounds before resetting.
        if (self.ball.x < 0 or self.ball.x > SCREEN_WIDTH + 100 or
            self.ball.y < 0 or self.ball.y > SCREEN_HEIGHT):
            sleep(0.5)
            self.reset_ball()
        
        self.ball.check_ground_collision(GROUND_HEIGHT)

        if self.ball.has_stopped() and self.ball_launched:
            self.reset_ball()

        for target in self.targets:
            if self.ball.check_collision(target):
                target.hit()  # Reduce target health
                self.score += 1  # Increment score when a target is hit
                if target.health <= 0:
                    self.targets.remove(target)

    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.slingshot.draw(self.screen)
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.circle(self.screen, RED, (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        for target in self.targets:
            target.draw(self.screen)
        
        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw the ball_count
        ball_count_text = font.render(f"Balls: {self.ball_count}", True, BLACK)
        self.screen.blit(ball_count_text, (10, 50))
        
        pygame.display.flip()