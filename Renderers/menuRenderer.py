import curses
import Dungeon.level as level
import Renderers.renderer as renderer
from Dungeon.level import height
from Resources import texts

menu_offset = renderer.master_offset + level.view_width + 20
height_offset = 1
log_array = []
height, width = 0, 0


def menus(stdscr, player_y, player_x):
    global height, width  # Global variables for terminal size
    height, width = stdscr.getmaxyx()  # Get the current terminal size
    left_menu(stdscr, player_y, player_x, height, width)
    right_menu(stdscr)


def left_menu(stdscr, player_y, player_x, height, width):
    # Display player position (y, x)
    stdscr.addstr(0, 0, f"Player Position: ({player_y}, {player_x})")
    stdscr.addstr(1, 0, f"Steps Taken: {level.step_counter}")

    # Draw author text at the bottom right
    stdscr.addstr(height - 1, width - 2 - len(texts.autor_text), texts.autor_text, curses.color_pair(1))
    if level.action:
        stdscr.addstr(1, width // 2 - len(texts.interaction_text) // 2, texts.interaction_text, curses.color_pair(1))


def debug_log(stdscr, text):
    log_array.append(text)


def right_menu(stdscr):
    global log_array
    """aka debug log"""
    global menu_offset

    if len(log_array) >= height - 2:  # Check if log exceeds height
        log_array.pop(0)
        right_menu(stdscr)
    lines = 0
    # Create a new list to store the processed log entries
    new_log_array = []
    for i in range(len(log_array)):
        if not isinstance(log_array[i], (list, tuple)) or len(log_array[i]) < 2:
            log_array[i] = [log_array[i], 1]  # Ensure log entries are lists with a color pair

    for i in range(len(log_array)):  # Loop through log entries
        if len(log_array[i][0]) > width - menu_offset:  # Check if entry exceeds width
            parts = log_array[i][0].split(" ")  # Split entry into words
            text = ''  # Current line text
            for part in parts:  # Loop through words
                if len(text + part + " ") > width - menu_offset:  # Check line length
                    new_log_array.append(text.strip())  # Add the current line to the new list
                    text = part + " "  # Start a new line
                else:
                    text += part + " "  # Add word to the current line
            new_log_array.append(text.strip())
        else:
            new_log_array.append(log_array[i])  # Add short entries as-is

    # Update log_array with the processed lines
    log_array = new_log_array

    # Display the log entries
    for i in range(len(log_array)):
        stdscr.addstr(i + height_offset, menu_offset, log_array[i][0], curses.color_pair(log_array[i][1]))
