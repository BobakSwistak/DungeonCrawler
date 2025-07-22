import curses
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer, logoRenderer
import playerInputs
from Resources import colors
import sys


def main(stdscr):
    colors.colors(stdscr)  # Initialize colors
    stdscr.bkgd(' ', colors.curses.color_pair(1))  # Set default background

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.noecho()  # Don't echo keypresses
    stdscr.timeout(1000)  # Input timeout (ms)

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
    player_y, player_x = levelGenerator.reload_level()  # Initialize player position (y, x)

    while True:
        if level.changes:
            level.changes = False
            stdscr.clear()
            renderer.rendering_map(stdscr, player_y, player_x)  # Player is always centered (y, x)
            menuRenderer.left_menu(stdscr, player_y, player_x)  # Draw the left menu (y, x)
            stdscr.refresh()

            result = playerInputs.player_input(stdscr, player_y, player_x)
            player_y, player_x = result  # Update player position (y, x)


curses.wrapper(main)
