import curses
from Dungeon import levelGenerator, level


def player_input(stdscr, player_y, player_x, level):
    key = stdscr.getch()
    if key is not None:
        level.changes = True  # Mark level as changed
        if key == ord('q'):
            return None  # Signal to quit
        elif key == ord('r'):
            player_y, player_x = levelGenerator.reload_level()
            return player_y, player_x
        if level.can_move:
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
                if level.level[new_y][new_x] in level.walkable:
                    player_y, player_x = new_y, new_x
                elif level.level[new_y][new_x] == "+":
                    level.level[new_y][new_x] = "`"  # Open the door
            return player_y, player_x
