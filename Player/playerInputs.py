import sys
import time
import services
import updates

from Dungeon import level, levelInit, levelManager
from Resources.tiles import Tiles
from Renderers import menuRenderer, renderer
from Player import playerHp, player, playerActions
from Resources import font, colors
from Enemies import enemies
from doorController import DoorController

last_move_time = 0
move_delay = 0.05


def player_input(terminal, key):
    global last_move_time, move_delay
    if key != terminal.TK_CLOSE:

        current_time = time.time()
        tech_input(terminal, key)

        if current_time - last_move_time >= move_delay:
            last_move_time = current_time

            if key == terminal.TK_A and player.can_move and not player.menu_opened:
                level.current_level.changes = True

                renderer.renderer(terminal)
                menuRenderer.interaction_text_render(terminal)
                terminal.refresh()

                services.wait_for_input(terminal)
                dy, dx = direction_input(terminal, get_input(terminal))
                if dy == 0 and dx == 0:
                    return None

                new_x = level.current_level.player_x + dy
                new_y = level.current_level.player_y + dx

                playerActions.action(new_x, new_y)


            elif key == terminal.TK_I and not player.menu_opened:
                level.current_level.changes = True

                renderer.renderer(terminal)
                menuRenderer.inspection_text_render(terminal)
                terminal.refresh()

                services.wait_for_input(terminal)
                dy, dx = direction_input(terminal, get_input(terminal))
                new_x = level.current_level.player_x + dy
                new_y = level.current_level.player_y + dx
                if new_x == level.current_level.player_x and new_y == level.current_level.player_y:
                    return None

                playerActions.inspect_tile(new_x, new_y)

            elif key == terminal.TK_E:
                player.can_move = not player.can_move
                player.menu_opened = not player.menu_opened

            elif key == terminal.TK_R and player.can_move and not player.menu_opened:
                level.current_level.changes = True

                renderer.renderer(terminal)
                input_text = menuRenderer.rest_text_controller(terminal)
                if input_text is None:
                    return None

                elif services.is_int(input_text):
                    playerHp.resting = True
                    input_text = int(input_text)

                    for i in range(input_text):
                        if any(enemy.is_visible for enemy in level.current_level.enemies_list) and levelInit.fog_of_war:
                            break
                        if terminal.has_input():
                            break
                        terminal.color(colors.WHITE)
                        updates.fast_update(terminal, "Resting...")

                elif input_text == "*":
                    playerHp.resting = True
                    while not playerHp.hp == playerHp.max_hp:
                        if any(enemy.is_visible for enemy in level.current_level.enemies_list) and levelInit.fog_of_war:
                            break
                        if terminal.has_input():
                            break
                        terminal.color(colors.WHITE)
                        updates.fast_update(terminal, "Resting...")
                playerHp.resting = False
                return None

            elif key == terminal.TK_D:
                level.current_level.changes = True
                levelManager.levelManager.go_level_downwards(
                    (level.current_level.player_x, level.current_level.player_y))
            elif key == 27 or key == terminal.TK_ESCAPE:
                player.action = False
                player.inspect = False
                player.can_move = True
                player.menu_opened = False
                menuRenderer.control_menu_toggle = False
                player.rest = False
                renderer.renderer(terminal)
                return None

        dy, dx = direction_input(terminal, key)
        new_x = level.current_level.player_x + dy
        new_y = level.current_level.player_y + dx
        player_x = level.current_level.player_x
        player_y = level.current_level.player_y

        if 0 <= new_x < levelInit.height and 0 <= new_y < levelInit.width and player.can_move:

            if Tiles.is_walkable(level.current_level.level[new_x][new_y]) and not level.current_level.occupied[new_x][
                new_y]:
                player_x, player_y = new_x, new_y
                # Mark new position as occupied

                if dx != 0 or dy != 0:
                    level.current_level.step_counter += 1
                    playerActions.passive_inspect(new_x, new_y)
            elif Tiles.is_door(level.current_level.level[new_x][new_y]):
                door = DoorController.open_door((new_x, new_y))
                if isinstance(door, tuple):
                    playerHp.damage_player(door[0], door[1])
                    menuRenderer.debug_log("The door was trapped!", color=colors.ORANGE)
                playerActions.passive_inspect(new_x, new_y)
            elif level.current_level.occupied[new_x][new_y]:
                for enemy in level.current_level.enemies_list:
                    if enemy.enemy_pos == [new_x, new_y] or enemy.enemy_pos == (new_x, new_y):
                        playerActions.attack(enemy)
            else:
                playerActions.passive_inspect(player_y, player_x)
                level.current_level.occupied[player_x][player_y] = True

    return player_x, player_y


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
    if (dx != 0 or dy != 0) and player.can_move:
        level.current_level.changes = True
    return dy, dx


def tech_input(terminal, key):
    if key == terminal.TK_Q:
        sys.exit()

    elif key == terminal.TK_F2:
        levelInit.fog_of_war = not levelInit.fog_of_war

    elif terminal.state(terminal.TK_CONTROL):
        if key in (ord('+'), terminal.TK_KP_PLUS):
            font.font_size += 1
        elif key in (ord('-'), terminal.TK_KP_MINUS):
            font.font_size -= 1

    elif key == terminal.TK_F1:
        player.can_move = not player.can_move
        player.menu_opened = not player.menu_opened
        menuRenderer.control_menu_toggle = not menuRenderer.control_menu_toggle


def get_input(terminal):
    key = terminal.read()
    services.flush_input(terminal)
    return key
