import curses


def colors(stdscr):
    # Initialize curses color system and set up color pairs
    curses.start_color()
    # Colors are defined as RGB values (0-1000)
    curses.init_color(0, 0, 0, 0)  # Black
    curses.init_color(10, 700, 400, 100)  # Brown
    curses.init_color(11, 500, 500, 500)  # Grey
    curses.init_color(12, 400, 200, 50)  # Dark brown
    curses.init_color(1, 1000, 0, 0)  # Red
    curses.init_color(2, 1000, 500, 0)  # Orange
    curses.init_color(3, 1000, 1000, 0)  # Yellow
    curses.init_color(4, 0, 1000, 0)  # Green

    # Initialize color pairs (Color of text, Color of background)

    # Bright colors
    curses.init_pair(1, curses.COLOR_WHITE, 0)  # Floors and Walls
    curses.init_pair(2, 11, 0)  # Floor

    curses.init_pair(3, 10, 0)  # Door
    curses.init_pair(4, 12, 0)  # Door

    curses.init_pair(5, curses.COLOR_CYAN, 0)  # Player

    curses.init_pair(100, 1, 0)  # Red
    curses.init_pair(101, 2, 0)  # Orange
    curses.init_pair(102, 3, 0)  # Yellow
    curses.init_pair(103, 4, 0)  # Green

    # Dark colors
