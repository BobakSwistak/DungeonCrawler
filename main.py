import curses
import Dungeon.level as level
import Dungeon.levelGenerator as levelGenerator
import renderer
import playerInputs
import colors


def main(stdscr):
    colors.Colors(stdscr)
    stdscr.bkgd(' ', colors.curses.color_pair(1))  # Set default background

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.noecho()  # Don't echo keypresses
    stdscr.timeout(1000)  # Input timeout (ms)

    player_x, player_y = levelGenerator.reload_level(stdscr)  # Initialize player position

    while True:
        if level.changes:
            level.changes = False
            stdscr.clear()  # Clear the screen for fresh rendering
            renderer.rendering_map(stdscr)  # Draw the dungeon map
            stdscr.addstr(player_y, player_x, '@', curses.color_pair(4))  # Draw the player
            stdscr.refresh()  # Update the display

            # Handle player input and movement
            result = playerInputs.player_input(stdscr, player_x, player_y, level)
            if result is None:
                break  # Exit loop if 'q' is pressed
            player_x, player_y = result  # Update player position


curses.wrapper(main)
