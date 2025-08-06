import Renderers.renderer as renderer
from Dungeon import level
from Player import playerHp, player
from Resources import texts, sizes, colors

menu_offset = renderer.master_offset + level.view_width + 5
height_offset = 1
log_array = []
height, width = 0, 0


def menus(terminal, player_y, player_x):
    global height, width  # Global variables for terminal size
    height, width = sizes.get_screen_size(terminal)
    left_menu(terminal, player_y, player_x, height, width)
    right_menu(terminal)
    hp_menu(terminal)
    text_help(terminal)

def left_menu(terminal, player_y, player_x, height, width):
    # Display player position (y, x)
    terminal.color(colors.WHITE)
    terminal.printf(0, 0, f"Player Position: ({player_y}, {player_x})")
    terminal.printf(0, 1, f"Steps Taken: {level.step_counter}")

    # Draw author text at the bottom right
    terminal.printf(width - 2 - len(texts.Texts.autor_text), height - 1, texts.Texts.autor_text)


def text_help(terminal):
    terminal.color(colors.WHITE)
    if player.action:
        terminal.printf(width // 2 - len(texts.Texts.interaction_text) // 2, 1, texts.Texts.interaction_text)
    if player.inspect:
        terminal.printf(width // 2 - len(texts.Texts.inspection_text) // 2, 1, texts.Texts.inspection_text)
    # elif player.rest:
    #     terminal.printf(1, width // 2 - len(texts.Texts.rest_text) // 2, texts.Texts.rest_text)
    #     terminal.refresh()  # Refresh the screen to display the prompt
    #
    #     input_x = width // 2 - len(Texts.rest_text) // 2 + len(Texts.rest_text)  # Position input after the prompt
    #     stdscr.refresh()  # Ensure the input prompt is visible
    #
    #     user_input = ""
    #     while True:
    #         key = stdscr.getch()
    #         if key == ord('\n'):  # Enter key
    #             break
    #         elif key != -1:  # Valid key press
    #             user_input += chr(key)
    #             stdscr.refresh()
    #
    #     level.rest = False
    #     level.can_move = True
    #     return user_input


def debug_log(text):
    log_array.append(text)


def clear_log():
    global log_array
    log_array = []  # Clear the log array


def hp_menu(terminal):
    terminal.color(colors.WHITE)
    terminal.printf(0, 0, f"Hp: ")
    hp_percentage = playerHp.hp / playerHp.max_hp  # Calculate the health percentage
    hp_color = 0  # Default color pair for health
    if hp_percentage == 1:
        hp_color = colors.WHITE
    elif hp_percentage > 0.75:
        hp_color = colors.GREEN
    elif hp_percentage > 0.5:
        hp_color = colors.YELLOW
    elif hp_percentage > 0.25:
        hp_color = colors.ORANGE
    else:
        hp_color = colors.RED
    terminal.color(hp_color)
    terminal.printf(4, 0, str(playerHp.hp))
    offset = len(str(playerHp.hp))
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
        if terminal.color(log_array[i][1]):
            terminal.printf(menu_offset, i + height_offset, log_array[i][0])
        else:
            terminal.color(colors.WHITE)
            terminal.printf(menu_offset, i + height_offset, log_array[i][0])
    # Update log_array with the processed lines
    log_array = new_log_array
