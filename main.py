import pygame
import menu
import Dungeon.levelGenerator as levelGenerator
import Dungeon.level as levelFile

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('DungeonCrawler')
clock = pygame.time.Clock()
font = pygame.font.SysFont('courier', 36)
level_map = levelGenerator.generate_level()

# x is row, y is column
for x in range(len(level_map)):
    print("".join(level_map[x]))

menu.main_menu(screen)
text = font.render("12", 0, (0, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(text, (100, 100))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()