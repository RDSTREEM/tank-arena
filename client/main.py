import pygame
from client.game import Game

WIDTH, HEIGHT = 800, 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tank Arena")
    clock = pygame.time.Clock()

    game = Game(WIDTH, HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.handle_input()
        game.update(dt)
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
