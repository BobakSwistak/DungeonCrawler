import curses


def colors(stdscr):
    # Initialize curses color system and set up color pairs
    curses.start_color()
    # Colors are defined as RGB values (0-1000)
    curses.init_color(0, 0, 0, 0)  # Black
    curses.init_color(10, 700, 400, 100)  # Brown
    curses.init_color(11, 500, 500, 500)  # Grey
    curses.init_color(12, 400, 200, 50)  # Dark brown
    # Initialize color pairs (Color of text, Color of background)

    # Bright colors
    curses.init_pair(1, curses.COLOR_WHITE, 0)  # Floors and Walls
    curses.init_pair(2, 10, 0)  # Door
    curses.init_pair(3, curses.COLOR_CYAN, 0)  # Player

    # Dark colors
    curses.init_pair(5, 11, 0)  # Floor
    curses.init_pair(7, 12, 0)  # Door
    curses.init_pair(8, curses.COLOR_CYAN, 0)  # Player
