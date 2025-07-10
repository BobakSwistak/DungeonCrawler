import pygame_menu
import renderer
import Dungeon.levelGenerator as levelGenerator
import Dungeon.level as levelFile

startTheGame = False

myTheme = pygame_menu.Theme(
    background_color=(0, 0, 0),
    title_background_color=(0, 0, 0),
    title_font_color=(255, 255, 255),
    widget_font_color=(255, 255, 255),
    selection_color=(255, 255, 255),
    title_font_size=36,
    widget_font_size=56
)


def main_menu(surface):
    menu = pygame_menu.Menu(' ', 600, 440, theme=myTheme)
    menu.add.button('Play', startTheGameFunc)
    menu.add.button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


def startTheGameFunc():
    global startTheGame
    startTheGame = True
    levelFile.level = levelGenerator.generate_level()
