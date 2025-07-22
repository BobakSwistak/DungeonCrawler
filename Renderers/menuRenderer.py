import curses
import Dungeon.level as level
import Renderers.renderer as renderer
from Resources import texts

menu_offset = renderer.master_offset + level.view_width


def left_menu(stdscr, player_y, player_x):
    # Display player position (y, x)
    stdscr.addstr(0, 0, f"Player Position: ({player_y}, {player_x})")
    stdscr.addstr(1, 0, f"Steps Taken: {level.step_counter}")

    height, width = stdscr.getmaxyx()

    # Draw author text at the bottom right
    stdscr.addstr(height - 1, width - 2 - len(texts.autor_text), texts.autor_text, curses.color_pair(1))
    if level.action:
        stdscr.addstr(1, width // 2 - len(texts.interaction_text) // 2, texts.interaction_text, curses.color_pair(1))
