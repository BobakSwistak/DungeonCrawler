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
    start_x = (screen_height - logo_height) // 2
    start_y = (screen_width - logo_width) // 2

    for i, line in enumerate(logo):
        stdscr.addstr(start_x + i, start_y, line, curses.color_pair(1))
