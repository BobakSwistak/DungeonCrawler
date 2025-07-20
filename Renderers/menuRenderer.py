import curses


text = " by Bobak Świstak"


def left_menu(stdscr, player_x, player_y):
    stdscr.addstr(0, 0, f"Player Position: ({player_x}, {player_y})")

    height, width = stdscr.getmaxyx()

    stdscr.addstr(height - 1, width - 2 - len(text), text, curses.color_pair(1))
