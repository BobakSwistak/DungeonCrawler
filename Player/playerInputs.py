import bearlibterminal as terminal
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer
from Player import playerHp, player, playerActions
import sys
import time

last_move_time = 0
move_delay = 0.05


def player_input(terminal, key, player_y, player_x):
    global last_move_time, move_delay
    if key != terminal.TK_CLOSE:
        current_time = time.time()
        level.changes = True

        if key == terminal.TK_Q:
            sys.exit()

        if current_time - last_move_time >= move_delay:
            last_move_time = current_time

            if key == terminal.TK_F1:
                player.can_move = False
                player.menu_opened = False

            elif key == terminal.TK_A and player.can_move and not player.menu_opened:
                player.action = True
                player.can_move = False

            elif key == terminal.TK_I and not player.menu_opened:
                player.inspect = True
                player.can_move = False

            elif key == terminal.TK_E:
                player.can_move = not player.can_move
                player.menu_opened = not player.menu_opened

            elif key == 27 or key == terminal.TK_ESCAPE:
                player.action = False
                player.inspect = False
                player.can_move = True
                renderer.renderer(terminal, player_y, player_x)

            dy, dx = direction_input(terminal, key)
            new_y = player_y + dy
            new_x = player_x + dx

            if 0 <= new_y < level.height and 0 <= new_x < level.width and player.can_move:
                playerActions.passive_inspect(new_y, new_x)
                if level.level[new_y][new_x] in level.walkable:
                    player_y, player_x = new_y, new_x
                    if dx != 0 or dy != 0:
                        level.step_counter += 1
                elif level.level[new_y][new_x] in level.doors:
                    playerActions.open_door(new_y, new_x)

            if player.action or player.inspect:
                player_action(player_y, player_x, dy, dx)

    return player_y, player_x


def player_action(player_y, player_x, dy, dx):
    global can_press
    new_y = player_y + dy
    new_x = player_x + dx

    if player.action:
        if dx != 0 or dy != 0:
            if level.level[new_y][new_x] == "`":
                playerActions.close_door(new_y, new_x)
            elif level.level[new_y][new_x] in level.doors:
                playerActions.open_door(new_y, new_x)
            player.action = False
            player.can_move = True
    elif player.inspect:
        if dx != 0 or dy != 0:
            playerActions.inspect_tile(new_y, new_x)
            player.inspect = False
            player.can_move = True


def direction_input(terminal, key=None):
    dy, dx = 0, 0
    # Handle movement keys
    if key in (terminal.TK_UP, ord('8'), terminal.TK_KP_8):  # Up arrow or numpad 8
        dy = -1
    elif key in (terminal.TK_DOWN, ord('2'), terminal.TK_KP_2):  # Down arrow or numpad 2
        dy = 1
    elif key in (terminal.TK_LEFT, ord('4'), terminal.TK_KP_4):  # Left arrow or numpad 4
        dx = -1
    elif key in (terminal.TK_RIGHT, ord('6'), terminal.TK_KP_6):  # Right arrow or numpad 6
        dx = 1
    elif key in (terminal.TK_HOME, ord('7'), terminal.TK_KP_7):  # Home key or numpad 7
        dy = -1
        dx = -1
    elif key in (terminal.TK_END, ord('1'), terminal.TK_KP_1):  # End key or numpad 1
        dy = 1
        dx = -1
    elif key in (terminal.TK_PAGEUP, ord('9'), terminal.TK_KP_9):  # Page Up or numpad 9
        dy = -1
        dx = 1
    elif key in (terminal.TK_PAGEDOWN, ord('3'), terminal.TK_KP_3):  # Page Down or numpad 3
        dy = 1
        dx = 1
    return dy, dx
