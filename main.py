from bearlibterminal import terminal
from Player import playerHp
from Resources import font
from Screens import mainScreen


def main():
    playerHp.hp_init()
    terminal.open()
    font.font_init()
    terminal.set(
        f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: {font.font_path}, size={font.font_size};")

    terminal.refresh()
    mainScreen.main_screen(terminal)


main()
