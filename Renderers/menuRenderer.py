import curses
import Dungeon.level as level
import Renderers.renderer as renderer

text = "by Bobak Świstak"
menu_offset = renderer.master_offset + level.view_width


def left_menu(stdscr, player_y, player_x):
    # Display player position (y, x)
    stdscr.addstr(0, 0, f"Player Position: ({player_y}, {player_x})")

    height, width = stdscr.getmaxyx()

    # Draw author text at the bottom right
    stdscr.addstr(height - 1, width - 2 - len(text), text, curses.color_pair(1))
