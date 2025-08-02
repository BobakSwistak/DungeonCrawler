import curses
from Dungeon import levelGenerator, level
from Renderers import renderer, menuRenderer
from Player import playerHp, player, playerActions
import sys


def player_input(stdscr, player_y, player_x):
    key = stdscr.getch()

    if key is not None:
        level.changes = True  # Mark level as changed
        if key == ord('q'):
            sys.exit(0)
            # return False # Exit to the main menu, for the future.

        elif key == ord('a') and player.can_move:
            player.action = True
            player.can_move = False

        elif key == ord('i'):
            player.inspect = True
            player.can_move = False

        elif key == 27:  # ESC key
            player.action = False  # Disable action mode
            player.inspect = False  # Disable inspect mode
            player.can_move = True  # Allow movement again
            renderer.renderer(stdscr, player_y, player_x)

        dy, dx = directiom_input(stdscr, key)
        new_y = player_y + dy
        new_x = player_x + dx

        if 0 <= new_y < level.height and 0 <= new_x < level.width and player.can_move:
            if level.level[new_y][new_x] in level.walkable:  # Check if the tile is walkable
                player_y, player_x = new_y, new_x  # Update player position
                if dx != 0 or dy != 0:
                    level.step_counter += 1  # Increment step counter for movement
            elif level.level[new_y][new_x] in level.doors:
                playerActions.open_door(new_y, new_x)  # Handle door interaction

        if player.action or player.inspect:
            player_action(stdscr, player_y, player_x, dy, dx)

    return player_y, player_x


def player_action(stdscr, player_y, player_x, dy, dx):
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
            if level.level[new_y][new_x] == "h+":
                level.level[new_y][new_x] = "+"
                menuRenderer.debug_log("you found something")
            else:
                menuRenderer.debug_log("there is nothing unusual to see here")
            player.inspect = False
            player.can_move = True


def directiom_input(stdscr, key=None):
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
    return dy, dx
