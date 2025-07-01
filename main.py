import pygame
import menu  # this is your menu.py file
import Dungeon.levelGenerator as levelGenerator
import Dungeon.level as levelFile

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('DungeonCrawler')
clock = pygame.time.Clock()
font = pygame.font.SysFont('courier', 36)
print(levelGenerator.generate_level())

# Show the menu first
menu.main_menu(screen)
text = font.render("12", 0, (0,0,0))  # fixed variable name

# Game loop starts after the menu exits
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # clear screen with black
    screen.blit(text, (100, 100))  # draw the text at position (100, 100)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()