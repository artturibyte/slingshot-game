import pygame
from ball import Ball
from slingshot import Slingshot
from time import sleep
from database import create_connection, create_table, insert_highscore, get_highscores
from utils import create_pyramid_targets
from text_item import TextItem
from constants import *
from enum import Enum
import math


class GameState(Enum):
    STORE = 1
    RUNNING = 2
    GAMEOVER = 3
    EXIT = 4

class Game:
    def __init__(self, startup_ball_count: int = 10):
        pygame.init()
        self.game_state: GameState = GameState.RUNNING
        pygame.display.set_caption("Slingshot Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ball: Ball = Ball()
        self.slingshot: Slingshot = Slingshot(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.targets = pygame.sprite.Group()
        self.score = 0  # Initialize score
        self.startupBallCount = startup_ball_count
        self.ball_count: int  # Initialize ball count
        self.level: int = 1
        self.measure_system_enable = False

        # Initialize database
        self.conn = create_connection(DATABASE)
        create_table(self.conn)

        # Load cloud images
        self.cloud1 = pygame.image.load('assets/Cloud1.png').convert_alpha()
        self.cloud2 = pygame.image.load('assets/Cloud2.png').convert_alpha()
        self.cloud3 = pygame.image.load('assets/Cloud3.png').convert_alpha()
        self.cloud4 = pygame.image.load('assets/Cloud4.png').convert_alpha()

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

        self.game_state = GameState.GAMEOVER
        while self.game_state == GameState.GAMEOVER:
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
            self.screen.blit(highscore_text, (350, 250))
            for i, highscore in enumerate(highscores):
                highscore_text = highscore_font.render(f"{i + 1}. {highscore[0]}: {highscore[1]}", True, BLACK)
                self.screen.blit(highscore_text, (350, 280 + i * 30))

            pygame.display.flip()
            sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = GameState.RUNNING

    def get_nickname(self):
        """Prompt the user to enter their nickname for hiscore."""
        pygame.event.clear()
        nickname = ""
        input_active = True
        font = pygame.font.Font(None, 34)
        max_length = 12  # Optional: limit nickname length

        while input_active and self.game_state != GameState.EXIT:
            self.screen.fill(WHITE)
            prompt_text = font.render("Enter your nickname for hiscore:", True, BLACK)
            prompt_text2 = font.render("(can be stuck, try to press r)", True, BLACK)
            self.screen.blit(prompt_text, (250, 250))
            self.screen.blit(prompt_text2, (250, 270))
            nickname_text = font.render(nickname, True, BLACK)
            self.screen.blit(nickname_text, (250, 350))
            pygame.display.flip()     
            for event in pygame.event.get():      
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        # Only add printable characters and limit length
                        if event.unicode.isprintable() and len(nickname) < max_length:
                            nickname += event.unicode
        return nickname
    
    def create_level_1(self):
        # Add two separate pyramids
        self.targets.add(*create_pyramid_targets(5, 600, GROUND_HEIGHT))
        self.targets.add(*create_pyramid_targets(3, 400, GROUND_HEIGHT))

    def create_level_2(self):
        # Add two pyramids top of each other
        self.targets.add(*create_pyramid_targets(5, 600, GROUND_HEIGHT))
        self.targets.add(*create_pyramid_targets(5, 600, GROUND_HEIGHT - 100))

    def reset_game(self):
        pygame.event.clear()
        self.ball.reset()
        self.slingshot.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        # reset score
        self.score = 0 
        # reset ballcount
        self.ball_count = self.startupBallCount

        self.targets.empty()
        self.create_level_1()

    def draw_trajectory(self):
        angle, power = self.slingshot.get_angle_and_power()
        start_x, start_y = self.slingshot.bucket_pos

        for t in range(0, 200, 5):

            x = start_x + power * t * math.cos(-angle) 
            y = start_y + power * t * math.sin(angle) + 0.025 * t ** 2

            if y > GROUND_HEIGHT:
                break  # Stop drawing if the trajectory goes below the ground

            pygame.draw.circle(self.screen, RED, (int(x), int(y)), 2)
        
    def run(self):
        while not self.game_state == GameState.EXIT:
            #self.start_screen()
            self.reset_game()
            while self.game_state == GameState.RUNNING:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
            self.game_over_screen()
        pygame.quit()

    def store_screen(self):
        pygame.event.clear()
        self.game_state = GameState.STORE
        self.draw()
        store_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Set transparency (0-255) for store screen
        store_surface.set_alpha(128)  
        
        def draw_overlay():
            # draw dark overlay for store.
            self.screen.blit(store_surface, (0, 0))
        
        def flash_text(text_item: TextItem):
            # Flash the item text
            item = store_item_font.render(text_item.text, True, WHITE)
            self.screen.blit(item, text_item.position)
            pygame.display.flip()
            pygame.time.delay(100)  # Flash duration
            return store_item_font.render(text_item.text, True, text_item.color)

        # Init store texts
        font = pygame.font.Font(None, 74)
        
        text = font.render("Store", True, BLACK)
        
        store_item_font = pygame.font.Font(None, 36)
        item1_text = TextItem("1. Extra Ball: -5 points", (350, 200), BLACK)
        item2_text = TextItem("2. MachineControlSystem3000: -30 points", (350, 250), BLACK)

        item1 = store_item_font.render(item1_text.text, True, item1_text.color)
        item2 = store_item_font.render(item2_text.text, True, item2_text.color)

        # Draw the store overlay
        draw_overlay()

        while self.game_state == GameState.STORE and self.game_state != GameState.EXIT:
            # Display title
            self.screen.blit(text, (450, 50))
            # Display store items
            self.screen.blit(item1, item1_text.position)
            self.screen.blit(item2, item2_text.position)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.score > - 10:
                        self.ball_count += 1
                        self.score -= 5
                        # Update scores & ball count and draw the overlay again
                        self.draw()
                        draw_overlay()
                        item1 = flash_text(item1_text)
                    elif event.key == pygame.K_2 and self.score - 30 > - 10:
                        self.measure_system_enable = True
                        self.score -= 30
                        # Update scores & ball count and draw the overlay again
                        self.draw()
                        draw_overlay()
                        item2 = flash_text(item2_text)
                    elif event.key == pygame.K_s  or event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.RUNNING
                        pygame.event.clear()
                        sleep(0.1)

        pygame.event.clear()


    def handle_events(self):
        if pygame.event.get(pygame.QUIT): 
            self.game_state = GameState.EXIT
            exit()
            
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

            if keys[pygame.K_SPACE]:
                angle, power = self.slingshot.release()
                self.ball.launch(angle, power)
                self.slingshot.ball_launched = True  # Set the flag to indicate the ball has been launched
                pygame.event.clear()

        if self.slingshot.ball_launched:
            if keys[pygame.K_r]:  # Check for the "R" key to reset the ball
                self.reset_ball()

        if keys[pygame.K_s]:  # Check for the "S" key to open the store
            self.store_screen()

    def reset_ball(self):
        self.ball.reset()
        self.slingshot.reset(BALL_INITIAL_X, BALL_INITIAL_Y)
        self.slingshot.ball_launched = False
        self.ball_count -= 1  # Decrement ball_count when the ball is reset

    def update(self):
        if self.ball_count == 0:
            sleep(2)
            self.game_state = GameState.GAMEOVER

        # Update the ball's position if it has been launched
        if self.slingshot.ball_launched:
            self.ball.update()
        
        # update level if all targets cleared
        if len(self.targets) == 0 and self.level == 1:
            self.create_level_2()
            self.level += 1
        
        if len(self.targets) == 0 and self.level == 2:
            self.score += self.ball_count
            sleep(2)
            self.game_state = GameState.GAMEOVER

        # Check if the ball is out of bounds. Let ball roll little bit out of bounds before resetting.
        if (self.ball.position.x < 0 or self.ball.position.x > SCREEN_WIDTH + 100 or
            self.ball.position.y < 0 or self.ball.position.y > SCREEN_HEIGHT):
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

        self.targets.update()

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds
        self.screen.blit(self.cloud1, (100, 150))
        self.screen.blit(self.cloud2, (400, 250))
        self.screen.blit(self.cloud3, (600, 200))
        self.screen.blit(self.cloud4, (800, 250))
        
        
        # Draw the ground as a filled rectangle
        pygame.draw.rect(self.screen, BROWN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        pygame.draw.circle(self.screen, RED, (int(self.ball.position.x), int(self.ball.position.y)), self.ball.radius)
        self.targets.draw(self.screen)
        self.slingshot.draw(self.screen)

        if not self.slingshot.ball_launched and self.measure_system_enable:
            self.draw_trajectory()
        
        # SCORE:
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        # BALLS left:
        ball_count_text = font.render(f"Balls: {self.ball_count}", True, BLACK)
        self.screen.blit(ball_count_text, (10, 50))
        # LEVEL:
        level_text = font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))  # Adjust the position as needed

        if self.game_state == GameState.RUNNING:
            store_text = font.render("Press 'S' to open the store", True, BLACK)
            self.screen.blit(store_text, (350, 20))

            if not self.slingshot.ball_launched:
                launch_text = font.render("Press SPACE to launch!", True, BLACK)
                self.screen.blit(launch_text, (320, 200))
            else:
                # Display instructions for restarting and opening the store
                restart_text = font.render("Press 'R' to reset the ball", True, BLACK)
                self.screen.blit(restart_text, (350, 50))

        pygame.display.flip()