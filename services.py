from Resources import colors


def get_screen_size(terminal):
    height, width = terminal.state(terminal.TK_HEIGHT), terminal.state(terminal.TK_WIDTH)
    return height, width


def flush_input(terminal):
    while terminal.has_input():
        terminal.read()

def get_color(hp, max_hp, max_color):
    hp_percentage = hp / max_hp  # Calculate the health percentage
    hp_color = 0  # Default color pair for health
    if hp_percentage == 1:
        hp_color = max_color
    elif hp_percentage > 0.75:
        hp_color = colors.GREEN
    elif hp_percentage > 0.5:
        hp_color = colors.YELLOW
    elif hp_percentage > 0.25:
        hp_color = colors.ORANGE
    else:
        hp_color = colors.RED
    return hp_color