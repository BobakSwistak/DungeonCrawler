import curses

logo = [
    " ____                             _____               _",
    "|    \ _ _ ___ ___ ___ ___ ___   |     |___ ___ _ _ _| |___ ___",
    "|  |  | | |   | . | -_| . |   |  |   --|  _| .`| | | | | -_|  _|",
    "|____/|___|_|_|_  |___|___|_|_|  |_____|_| |__,|_____|_|___|_|",
    "              |___|"
]


def draw_centered_logo(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    logo_height = len(logo)
    logo_width = max(len(line) for line in logo)
    # Calculate top-left corner for centering (y, x)
    start_y = (screen_height - logo_height) // 2  # y is row
    start_x = (screen_width - logo_width) // 2  # x is column

    for i, line in enumerate(logo):
        # Draw each line of the logo at the correct (y, x) position
        stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))
