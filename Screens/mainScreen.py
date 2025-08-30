import sys
import updates

from Renderers import logoRenderer

def main_screen(terminal):
    terminal.clear()
    logoRenderer.draw_centered_logo(terminal)
    terminal.refresh()

    while True:
        key = terminal.read()
        if key == terminal.TK_CLOSE or key == terminal.TK_Q:
            sys.exit()
        elif key != -1:  # Wait for any key press
            updates.update(terminal)
            return
