from Resources import texts, colors, sizes

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


def draw_centered_logo(terminal):
    screen_height, screen_width = sizes.get_screen_size(terminal)
    logo_height = len(logo)
    logo_width = max(len(line) for line in logo)

    # Calculate top-left corner for centering (y, x)
    start_y = (screen_height - logo_height) // 2  # y is row
    start_x = (screen_width - logo_width) // 2  # x is column

    for i, line in enumerate(logo):
        terminal.color(colors.WHITE)
        terminal.printf(start_x, start_y + i, line)
    terminal.color(colors.WHITE)
    terminal.printf(screen_width // 2 - len(texts.Texts.intro_text) // 2, screen_height - 3, texts.Texts.intro_text)


def death_screen(terminal):
    screen_height, screen_width = sizes.get_screen_size(terminal)
    death_height = len(death)
    death_width = max(len(line) for line in death)
    # Calculate top-left corner for centering (y, x)
    start_y = (screen_height - death_height) // 2  # y is row
    start_x = (screen_width - death_width) // 2  # x is column

    for i, line in enumerate(death):
        # Draw each line of the logo at the correct (y, x) position
        terminal.color(colors.WHITE)
        terminal.printf(start_y + i, start_x, line)
    height, width = sizes.get_screen_size(terminal)
    terminal.color(colors.WHITE)
    terminal.printf(height - 3, width // 2 - len(texts.Texts.death_text) // 2, texts.Texts.death_text)
