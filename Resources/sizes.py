import bearlibterminal as terminal

def get_screen_size(terminal):
    height, width = terminal.state(terminal.TK_HEIGHT), terminal.state(terminal.TK_WIDTH)
    return height, width


def flush_input():
    from bearlibterminal import terminal
    while terminal.has_input():
        terminal.read()
