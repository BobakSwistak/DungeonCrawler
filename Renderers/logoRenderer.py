import curses
from Resources import texts

logo = [
    "    ___                                        ___                   _",
    "   /   \_   _ _ __   __ _  ___  ___  _ __     / __\ __ __ ___      _| | ___ _ __",
    "  / /\ / | | | '_ \ / _` |/ _ \/ _ \| '_ \   / / | '__/ _` \ \ /\ / / |/ _ \ '__|",
    " / /_//| |_| | | | | (_| |  __/ (_) | | | | / /__| | | (_| |\ V  V /| |  __/ |",
    "/___,'  \__,_|_| |_|\__, |\___|\___/|_| |_| \____/_|  \__,_| \_/\_/ |_|\___|_|",
    "                    |___/"]

death = [
    "__   __           ______ _          _ ",
    "\ \ / /           |  _  (_)        | |",
    " \ V /___  _   _  | | | |_  ___  __| |",
    "  \ // _ \| | | | | | | | |/ _ \/ _` |",
    "  | | (_) | |_| | | |/ /| |  __/ (_| |",
    "  \_/\___/ \__,_| |___/ |_|\___|\__,_|",
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
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 3, width // 2 - len(texts.intro_text) // 2, texts.intro_text, curses.color_pair(1))


def death_screen(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    death_height = len(death)
    death_width = max(len(line) for line in death)
    # Calculate top-left corner for centering (y, x)
    start_y = (screen_height - death_height) // 2  # y is row
    start_x = (screen_width - death_width) // 2  # x is column

    for i, line in enumerate(death):
        # Draw each line of the logo at the correct (y, x) position
        stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 3, width // 2 - len(texts.death_text) // 2, texts.death_text, curses.color_pair(1))
