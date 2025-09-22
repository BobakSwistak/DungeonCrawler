import services

from Dungeon import levelInit
from Player import playerHp, player
from Player.playerInputs import player_input
from Resources import texts, colors, offsets

menu_offset = offsets.level_offset + levelInit.view_width + 5
height_offset = 1
log_array = []
height, width = 0, 0

control_menu_toggle = False


def menus(terminal, player_x, player_y):
    global height, width, control_menu_toggle  # Global variables for terminal size
    height, width = services.get_screen_size(terminal)
    left_menu(terminal, player_x, player_y, height, width)
    right_menu(terminal)
    hp_menu(terminal)
    if control_menu_toggle: control_menu(terminal)


def left_menu(terminal, player_x, player_y, height, width):
    # Display player position (x, y)
    terminal.color(colors.WHITE)
    terminal.printf(0, 2, f"Player Position: ({player_x}, {player_y})")
    # terminal.printf(0, 1, f"Steps Taken: {level.step_counter}")

    # Draw author text at the bottom right
    height, _ = services.get_screen_size(terminal)
    terminal.printf(width - 2 - len(texts.Texts.autor_text), height - 1, texts.Texts.autor_text)
    terminal.printf(0, height - 1, texts.Texts.F1_text)


def interaction_text_render(terminal):
    terminal.color(colors.WHITE)
    terminal.printf(width // 2 - len(texts.Texts.interaction_text) // 2, 1, texts.Texts.interaction_text)


def inspection_text_render(terminal):
    terminal.color(colors.WHITE)
    terminal.printf(width // 2 - len(texts.Texts.inspection_text) // 2, 1, texts.Texts.inspection_text)


def rest_text_controller(terminal):
    user_input = ""
    text = texts.Texts.rest_text
    text_pos = width // 2 - len(text) // 2
    input_pos = text_pos + len(text)

    terminal.clear_area(menu_offset, 1, width, 2)
    terminal.printf(text_pos, 1, text)
    terminal.refresh()

    while True:
        key = terminal.read()
        if key == terminal.TK_RETURN:  # Enter key
            break
        elif key == 27 or key == terminal.TK_ESCAPE:  # Escape key
            return None  # Cancel input
        elif key == terminal.TK_BACKSPACE and len(user_input) > 0:  # Backspace key
            user_input = user_input[:-1]
        elif terminal.state(terminal.TK_CHAR):  # Any printable character
            user_input += chr(terminal.state(terminal.TK_CHAR))

        # Update only the input area
        terminal.clear_area(menu_offset, 1, width, 2)
        terminal.printf(text_pos, 1, text)
        terminal.printf(input_pos, 1, user_input)
        terminal.refresh()

    return user_input

def text_renderer(terminal, text):
    terminal.color(colors.WHITE)
    terminal.printf(width // 2 - len(text) // 2, 1, text)

def debug_log(text, color=colors.WHITE):
    log_array.append((str(text), color))  # Append the text and color pair to the log array


def clear_log():
    global log_array
    log_array = []  # Clear the log array


def hp_menu(terminal):
    terminal.color(colors.WHITE)
    terminal.printf(0, 0, f"Hp: ")
    hp_percentage = playerHp.hp / playerHp.max_hp  # Calculate the health percentage
    hp_color = services.get_color(playerHp.hp, playerHp.max_hp, colors.WHITE)
    terminal.color(hp_color)
    terminal.printf(4, 0, str(playerHp.hp))
    offset = len(str(playerHp.hp))
    terminal.color(colors.WHITE)  # Reset color to white for max HP
    terminal.printf(offset + 4, 0, f"/{playerHp.max_hp}")  # Display max HP


# Python
def right_menu(terminal):
    global log_array  # Global variable to store log entries
    global menu_offset  # Offset for the menu position

    # Ensure the log does not exceed the height of the screen
    if len(log_array) >= height - 2:
        log_array.pop(0)  # Remove the oldest log entry to make space

    lines = 0  # Counter for lines in the menu
    new_log_array = []  # Temporary list to store processed log entries

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
            new_log_array.append((text.strip(), log_array[i][1]))  # Add the last line
        else:
            new_log_array.append(log_array[i])  # Add short entries as-is

    # Update the global log array with the processed entries
    log_array = new_log_array

    # Display the log entries on the screen
    for i in range(len(log_array)):
        terminal.color(log_array[i][1])
        terminal.printf(menu_offset, i + height_offset, log_array[i][0])
    # Update log_array with the processed lines
    log_array = new_log_array


def control_menu(terminal):
    global height_offset
    height, width = services.get_screen_size(terminal)
    terminal.color(colors.WHITE)
    for i in range(len(texts.Texts.controls_text)):
        terminal.printf(offsets.level_offset, i + height_offset, texts.Texts.controls_text[i])
