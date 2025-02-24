import pygame
from ball import Ball
from slingshot import Slingshot
from target import Target
from time import sleep
from typing import List
from database import create_connection, create_table, insert_highscore, get_highscores
from utils import create_pyramid_targets
from utils import create_pyramid_targets

# Constants for ball initial position
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 445

# Constants for screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Game constants
GROUND_HEIGHT = 550
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 10

# Constants for colors
SKY_BLUE = (52, 158, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

DATABASE = "highscores.db"

class Game:
    def __init__(self, startup_ball_count: int = 5):
        pygame.init()
        pygame.display.set_caption("Slingshot Game")
        self.exit_game = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ball: Ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot: Slingshot = Slingshot(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.targets: List[Target]
        self.running = True
        self.score = 0  # Initialize score
        self.startupBallCount = startup_ball_count
        self.ball_count: int = 5  # Initialize ball count 

        # Initialize database
        self.conn = create_connection(DATABASE)
        create_table(self.conn)

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
        # Prompt the user for their nickname
        nickname = self.get_nickname()

        # Save the current score to the database
        insert_highscore(self.conn, nickname, self.score)

        # Get the top 5 high scores
        highscores = get_highscores(self.conn)

        game_over = True
        while game_over and not self.exit_game:
            pygame.event.clear()
            self.screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render(f"Game Over! Score: {self.score}", True, BLACK)
            self.screen.blit(text, (250, 50))
            restart_text = font.render("Press Enter to Restart", True, BLACK)
            self.screen.blit(restart_text, (250, 150))

            # Display high scores
            highscore_font = pygame.font.Font(None, 36)
            highscore_text = highscore_font.render("High Scores:", True, BLACK)
            self.screen.blit(highscore_text, (350, 300))
            for i, highscore in enumerate(highscores):
                highscore_text = highscore_font.render(f"{i + 1}. {highscore[0]}: {highscore[1]}", True, BLACK)
                self.screen.blit(highscore_text, (350, 340 + i * 30))

            pygame.display.flip()
            sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False

    def get_nickname(self):
        """Prompt the user to enter their nickname for hiscore."""
        pygame.event.clear()
        nickname = ""
        input_active = True
        font = pygame.font.Font(None, 34)
        
        while input_active and not self.exit_game:
            self.screen.fill(WHITE)
            prompt_text = font.render("Enter your nickname for hiscore:", True, BLACK)
            self.screen.blit(prompt_text, (250, 250))
            nickname_text = font.render(nickname, True, BLACK)
            self.screen.blit(nickname_text, (250, 350))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        nickname += event.unicode
        return nickname

    def reset_game(self):
        pygame.event.clear()
        self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.score = 0 # reset score
        self.ball_count = self.startupBallCount
        # creating two pyramids, side by side
        self.targets = create_pyramid_targets(5, 600, GROUND_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT) + create_pyramid_targets(3, 500, GROUND_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.running = True

    def run(self):
        while not self.exit_game:
            #self.start_screen()
            self.reset_game()
            while self.running and not self.exit_game:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
            self.game_over_screen()
        pygame.quit()

    def handle_events(self):
        if pygame.event.get(pygame.QUIT): 
            self.running = False
            self.exit_game = True
            self.exit_game = True
        
        keys = pygame.key.get_pressed()

        if not self.slingshot.ball_launched:
            if keys[pygame.K_UP]: 
                self.slingshot.stretch(0, -1)
            if keys[pygame.K_DOWN]: 
                self.slingshot.stretch(0, 1)
            if keys[pygame.K_LEFT]: 
                self.slingshot.stretch(-1, 0)
            if keys[pygame.K_RIGHT]: 
                self.slingshot.stretch(1, 0)

            if keys[pygame.K_RETURN]:
                angle, power = self.slingshot.release()
                self.ball.launch(angle, power)
                self.slingshot.ball_launched = True  # Set the flag to indicate the ball has been launched

        if self.slingshot.ball_launched:
            if keys[pygame.K_r]:  # Check for the "R" key to reset the ball
                self.reset_ball()

    def reset_ball(self):
        self.ball.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot.ball_launched = False
        self.ball_count -= 1  # Decrement ball_count when the ball is reset

    def update(self):
        if self.ball_count == 0:
            self.running = False

        # Update the ball's position if it has been launched
        if self.slingshot.ball_launched:
            self.ball.update()

        # Check if the ball is out of bounds. Let ball roll little bit out of bounds before resetting.
        if (self.ball.x < 0 or self.ball.x > SCREEN_WIDTH + 100 or
            self.ball.y < 0 or self.ball.y > SCREEN_HEIGHT):
            sleep(0.5)
            self.reset_ball()
        
        self.ball.check_ground_collision(GROUND_HEIGHT)

        if self.ball.has_stopped() and self.slingshot.ball_launched:
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