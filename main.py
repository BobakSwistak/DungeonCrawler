from bearlibterminal import terminal
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer, logoRenderer
from Player import playerInputs, playerHp, player
from Resources import colors
import sys


def main():
    playerHp.hp_init()
    terminal.open()
    terminal.set("window: size=140x50, cellsize=auto, title='BearLibTerminal Example'; font: default")

    terminal.refresh()

    main_screen(terminal)


def main_screen(terminal):
    terminal.clear()
    logoRenderer.draw_centered_logo(terminal)
    terminal.refresh()

    while True:
        key = terminal.read()
        if key == ord('q'):
            sys.exit()
        elif key != -1:  # Wait for any key press
            game_cycle(terminal)
            return


def game_cycle(terminal):
    player.player_y, player.player_x = levelGenerator.generate_dungeon()  # Initialize player position (y, x)

    while True:
        terminal.clear()
        if player.menu_opened is False:
            renderer.renderer(terminal, player.player_y, player.player_x)
        menuRenderer.menus(terminal, player.player_y, player.player_x)
        terminal.refresh()
        if level.changes:
            level.changes = False
            result = playerInputs.player_input(terminal, player.player_y, player.player_x)
            if result is False:
                main_screen(terminal)
                return

            player.player_y, player.player_x = result  # Update player position (y, x)
            playerHp.hp_update()

            # Only clear and refresh the screen when necessary
            terminal.clear()
            renderer.renderer(terminal, player.player_y, player.player_x)
            menuRenderer.menus(terminal, player.player_y, player.player_x)
            terminal.refresh()

        if playerHp.hp <= 0:  # Handle player death
            death(terminal)
            return


def death(terminal):
    terminal.clear()
    logoRenderer.death_screen(terminal)
    while True:
        key = terminal.read()
        if key == ord('q'):
            sys.exit()
        elif key != -1:  # Wait for any key press
            playerHp.hp_init()
            menuRenderer.clear_log()

            game_cycle(terminal)
            return


main()
