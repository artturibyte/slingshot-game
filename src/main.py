import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Slingshot Game")
    
    game = Game(screen)
    game.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update()
        game.draw()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()