import curses
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer, logoRenderer
import playerInputs
import colors


def main(stdscr):
    colors.colors(stdscr) # Initialize colors
    stdscr.bkgd(' ', colors.curses.color_pair(1))  # Set default background

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.noecho()  # Don't echo keypresses
    stdscr.timeout(1000)  # Input timeout (ms)

    logoRenderer.draw_centered_logo(stdscr)
    stdscr.refresh()
    while True:
        if stdscr.getch() != -1:  # Wait for any key press
            if stdscr.getch() == ord('q'):
                break
            elif game_cycle(stdscr) == 0:
                break


def game_cycle(stdscr):
    player_x, player_y = levelGenerator.reload_level(stdscr)  # Initialize player position

    while True:
        if level.changes:
            level.changes = False
            stdscr.clear()
            renderer.rendering_map(stdscr, player_x, player_y)  # Player is always centered
            menuRenderer.left_menu(stdscr, player_x, player_y)  # Draw the left menu
            stdscr.refresh()

            result = playerInputs.player_input(stdscr, player_x, player_y, level)
            if result is None:
                return 0
            player_x, player_y = result


curses.wrapper(main)
