import sys

from Renderers import logoRenderer, menuRenderer
from Player import playerHp


def death(terminal):
    terminal.clear()
    logoRenderer.death_screen(terminal)
    terminal.refresh()
    while True:

        key = terminal.read()
        if key == terminal.TK_Q:
            sys.exit()

        elif key != -1:  # Wait for any key press
            playerHp.hp_init()
            menuRenderer.clear_log()
