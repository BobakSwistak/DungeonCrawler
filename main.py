import curses
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer, logoRenderer
from Player import playerInputs, playerHp
from Resources import colors
import sys


def main(stdscr):
    playerHp.hp_init()
    colors.colors(stdscr)  # Initialize colors
    stdscr.bkgd(' ', colors.curses.color_pair(1))  # Set default background

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.noecho()  # Don't echo keypresses
    stdscr.timeout(1000)  # Input timeout (ms)
    main_screen(stdscr)


def main_screen(stdscr):
    stdscr.clear()
    logoRenderer.draw_centered_logo(stdscr)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            sys.exit()
        elif key != -1:  # Wait for any key press
            game_cycle(stdscr)
            return


def game_cycle(stdscr):
    player_y, player_x = levelGenerator.generate_dungeon()  # Initialize player position (y, x)

    while True:
        stdscr.clear()
        renderer.renderer(stdscr, player_y, player_x)
        menuRenderer.menus(stdscr, player_y, player_x)
        stdscr.refresh()
        if level.changes:
            level.changes = False
            result = playerInputs.player_input(stdscr, player_y, player_x)
            if result is False:
                main_screen(stdscr)
                return

            player_y, player_x = result  # Update player position (y, x)
            playerHp.hp_update()

            # Only clear and refresh the screen when necessary
            stdscr.clear()
            renderer.renderer(stdscr, player_y, player_x)
            menuRenderer.menus(stdscr, player_y, player_x)
            stdscr.refresh()

        if playerHp.hp <= 0:  # Handle player death
            death_screen(stdscr)
            return


def death_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(10, 10, "game over")
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            sys.exit()


curses.wrapper(main)
