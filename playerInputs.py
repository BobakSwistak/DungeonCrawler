import curses
import Dungeon.levelGenerator as levelGenerator
import Dungeon.level as level


def player_input(stdscr, player_x, player_y, level):
    key = stdscr.getch()
    if key != None:
        level.changes = True  # Mark level as changed
        if key == ord('q'):
            return None  # Signal to quit
        elif key == ord('r'):
            player_x, player_y = levelGenerator.reload_level(stdscr)
            return player_x, player_y
        dx, dy = 0, 0
        # Handle movement keys
        if key == curses.KEY_UP:
            dy = -1
        elif key == curses.KEY_DOWN:
            dy = 1
        elif key == curses.KEY_LEFT:
            dx = -1
        elif key == curses.KEY_RIGHT:
            dx = 1
        elif key == curses.KEY_HOME:
            dx = -1
            dy = -1
        elif key == curses.KEY_END:
            dx = -1
            dy = 1
        elif key == curses.KEY_PPAGE:
            dx = 1
            dy = -1
        elif key == curses.KEY_NPAGE:
            dx = 1
            dy = 1
        new_x = player_x + dx
        new_y = player_y + dy
        if 0 <= new_y < level.height and 0 <= new_x < level.width:
            if level.level[new_y][new_x] in level.walkable:
                player_x, player_y = new_x, new_y
            elif level.level[new_y][new_x] == "+":
                level.level[new_y][new_x] = "`"  # Open the door
        return player_x, player_y
