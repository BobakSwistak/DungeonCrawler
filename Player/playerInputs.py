import curses
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer
from Player import player_hp
from Resources import texts
import sys


def player_input(stdscr, player_y, player_x):
    key = stdscr.getch()

    if key is not None:

        level.changes = True  # Mark level as changed
        if key == ord('q'):
            sys.exit(0)
            # return False # Exit to the main menu, for the future.

        elif key == ord('a'):
            level.action = True
            level.can_move = False

        elif key == 27:  # ESC key
            level.action = False
            level.can_move = True
            renderer.renderer(stdscr, player_y, player_x)

        dy, dx = 0, 0
        # Handle movement keys
        if key == curses.KEY_UP or key == ord('8'):  # Up arrow or numpad 8
            dy = -1
        elif key == curses.KEY_DOWN or key == ord('2'):  # Down arrow or numpad 2
            dy = 1
        elif key == curses.KEY_LEFT or key == ord('4'):  # Left arrow or numpad 4
            dx = -1
        elif key == curses.KEY_RIGHT or key == ord('6'):  # Right arrow or numpad 6
            dx = 1
        elif key == curses.KEY_HOME or key == ord('7'):  # Home key or numpad 7
            dy = -1
            dx = -1
        elif key == curses.KEY_END or key == ord('1'):  # End key or numpad 1
            dy = 1
            dx = -1
        elif key == curses.KEY_PPAGE or key == ord('9'):  # Page Up or numpad 9
            dy = -1
            dx = 1
        elif key == curses.KEY_NPAGE or key == ord('3'):  # Page Down or numpad 3
            dy = 1
            dx = 1

        new_y = player_y + dy
        new_x = player_x + dx
        if 0 <= new_y < level.height and 0 <= new_x < level.width:
            if level.action and (dx != 0 or dy != 0):
                level.action = False
                level.can_move = True

                if level.level[new_y][new_x] == "`":
                    level.level[new_y][new_x] = "+"  # Close the door
                    menuRenderer.debug_log("Door closed")
                elif level.level[new_y][new_x] in level.doors:
                    if level.level[new_y][new_x] == "+":
                        level.level[new_y][new_x] = "`"  # Open the door
                        menuRenderer.debug_log("Door opened")

                    if level.level[new_y][new_x] == "t+":
                        player_hp.damage_player(2, 5)
                        level.level[new_y][new_x] = "`"  # Open the door
                        menuRenderer.debug_log("Door was trapped")

            elif level.level[new_y][new_x] in level.walkable and level.can_move:
                player_y, player_x = new_y, new_x
                if dx != 0 or dy != 0:
                    level.step_counter += 1

            elif level.level[new_y][new_x] in level.doors and level.can_move:
                if level.level[new_y][new_x] == "+":
                    level.level[new_y][new_x] = "`"  # Open the door
                    menuRenderer.debug_log("Door opened")
                elif level.level[new_y][new_x] == "t+":
                    player_hp.damage_player(2, 5)
                    level.level[new_y][new_x] = "`"  # Open the door
                    menuRenderer.debug_log("Door was trapped")

        return player_y, player_x
