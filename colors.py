import curses


def Colors(stdscr):
    # Initialize curses color system and set up color pairs
    curses.start_color()
    # Colors are defined as RGB values (0-1000)
    curses.init_color(0, 0, 0, 0)  # Black
    curses.init_color(10, 700, 400, 100)  # Brown
    # Initialize color pairs (Color of text, Color of background)
    curses.init_pair(1, curses.COLOR_WHITE, 0)  # Floor
    curses.init_pair(2, curses.COLOR_WHITE, 0)  # Wall
    curses.init_pair(3, 10, 0)  # Door
    curses.init_pair(4, curses.COLOR_CYAN, 0)  # Player
