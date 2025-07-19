import curses


def left_menu(stdscr, player_x, player_y):
    stdscr.addstr(0, 0, f"Player Position: ({player_x}, {player_y})")
