from bearlibterminal import terminal
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer, logoRenderer
from Player import playerInputs, playerHp, player
from Resources import font
import sys
import time
import services


def main():
    playerHp.hp_init()
    terminal.open()
    terminal.set(
        f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: Resources/FSEX300.ttf, size={font.font_size};")

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
    player.player_y, player.player_x = levelGenerator.generate_dungeon()

    while True:
        if font.font_size < 8:
            font.font_size = 8
        elif font.font_size > 20:
            font.font_size = 20
        terminal.set(
            f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: Resources/FSEX300.ttf, size={font.font_size};")

        terminal.clear()
        time.sleep(0.005)
        if player.menu_opened is False:
            renderer.renderer(terminal, player.player_y, player.player_x)
        menuRenderer.menus(terminal, player.player_y, player.player_x)
        terminal.refresh()

        # Handle input every frame (non-blocking)
        if terminal.has_input():
            key = terminal.read()
            services.flush_input()
            result = playerInputs.player_input(terminal, key, player.player_y, player.player_x)

            if result is False:
                main_screen(terminal)
                return
            player.player_y, player.player_x = result
            playerHp.hp_update()

        # Only redraw if needed
        if level.changes:
            terminal.clear()
            renderer.renderer(terminal, player.player_y, player.player_x)
            menuRenderer.menus(terminal, player.player_y, player.player_x)
            terminal.refresh()
            level.changes = False

        if playerHp.hp <= 0:
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
