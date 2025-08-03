import curses
import Renderers.renderer as renderer
from Dungeon import level
from Player import playerHp, player
from Resources.texts import Texts

menu_offset = renderer.master_offset + level.view_width + 20
height_offset = 1
log_array = []
height, width = 0, 0


def menus(stdscr, player_y, player_x):
    global height, width  # Global variables for terminal size
    height, width = stdscr.getmaxyx()  # Get the current terminal size
    left_menu(stdscr, player_y, player_x, height, width)
    right_menu(stdscr)
    hp_menu(stdscr)
    text_help(stdscr)


def left_menu(stdscr, player_y, player_x, height, width):
    # Display player position (y, x)
    # stdscr.addstr(0, 0, f"Player Position: ({player_y}, {player_x})")
    # stdscr.addstr(1, 0, f"Steps Taken: {level.step_counter}")

    # Draw author text at the bottom right
    stdscr.addstr(height - 1, width - 2 - len(Texts.autor_text), Texts.autor_text, curses.color_pair(1))


def text_help(stdscr):
    if player.action:
        stdscr.addstr(1, width // 2 - len(Texts.interaction_text) // 2, Texts.interaction_text, curses.color_pair(1))
    if player.inspect:
        stdscr.addstr(1, width // 2 - len(Texts.inspection_text) // 2, Texts.inspection_text, curses.color_pair(1))
    elif player.rest:
        stdscr.addstr(1, width // 2 - len(Texts.rest_text) // 2, Texts.rest_text, curses.color_pair(1))
        stdscr.refresh()  # Refresh the screen to display the prompt

        curses.echo()  # Enable echo to show user input on the screen
        input_x = width // 2 - len(Texts.rest_text) // 2 + len(Texts.rest_text)  # Position input after the prompt
        stdscr.refresh()  # Ensure the input prompt is visible

        user_input = ""
        while True:
            key = stdscr.getch()
            if key == ord('\n'):  # Enter key
                break
            elif key != -1:  # Valid key press
                user_input += chr(key)
                stdscr.refresh()

        curses.noecho()  # Disable echo after capturing input
        level.rest = False
        level.can_move = True
        return user_input


def debug_log(text):
    log_array.append(text)


def clear_log():
    global log_array
    log_array = []  # Clear the log array


def hp_menu(stdscr):
    stdscr.addstr(0, 0, f"Hp: ")
    hp_percentage = playerHp.hp / playerHp.max_hp  # Calculate the health percentage
    hp_color = 0  # Default color pair for health
    if hp_percentage == 1:
        hp_color = 1
    elif hp_percentage > 0.75:
        hp_color = 103  # Green
    elif hp_percentage > 0.5:
        hp_color = 102  # Yellow
    elif hp_percentage > 0.25:
        hp_color = 101  # orange
    else:
        hp_color = 100  # Red
    stdscr.addstr(0, 4, str(playerHp.hp), curses.color_pair(hp_color))
    offset = len(str(playerHp.hp))
    stdscr.addstr(0, offset + 4, f"/{playerHp.max_hp}", curses.color_pair(1))  # Display max HP


# Python
def right_menu(stdscr):
    global log_array  # Global variable to store log entries
    global menu_offset  # Offset for the menu position

    # Ensure the log does not exceed the height of the screen
    if len(log_array) >= height - 2:
        log_array.pop(0)  # Remove the oldest log entry to make space

    lines = 0  # Counter for lines in the menu
    new_log_array = []  # Temporary list to store processed log entries

    # Validate and format each log entry
    for i in range(len(log_array)):
        # Ensure each log entry is a list or tuple with at least two elements
        if not isinstance(log_array[i], (list, tuple)) or len(log_array[i]) < 2:
            log_array[i] = [log_array[i], 1]  # Default to color pair 1 if invalid

        # Ensure the second element (color pair) is an integer
        if not isinstance(log_array[i][1], int):
            log_array[i][1] = 1  # Default to color pair 1

    # Process log entries to fit within the screen width
    for i in range(len(log_array)):
        if len(log_array[i][0]) > width - menu_offset:  # Check if the log entry exceeds the width
            parts = log_array[i][0].split(" ")  # Split the log entry into words
            text = ''  # Temporary variable to build lines
            for part in parts:
                # Check if adding the next word exceeds the width
                if len(text + part + " ") > width - menu_offset:
                    new_log_array.append([text.strip(), log_array[i][1]])  # Add the current line to the new list
                    text = part + " "  # Start a new line
                else:
                    text += part + " "  # Add the word to the current line
            new_log_array.append([text.strip(), log_array[i][1]])  # Add the last line
        else:
            new_log_array.append(log_array[i])  # Add short entries as-is

    # Update the global log array with the processed entries
    log_array = new_log_array

    # Display the log entries on the screen
    for i in range(len(log_array)):
        stdscr.addstr(i + height_offset, menu_offset, log_array[i][0], curses.color_pair(log_array[i][1]))
    # Update log_array with the processed lines
    log_array = new_log_array
