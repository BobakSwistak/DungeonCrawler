import curses
import Dungeon.level as level
import Dungeon.levelGenerator as levelGenerator


def main(stdscr):
    # Initialize curses color system and set up color pairs
    curses.start_color()
    curses.init_color(0, 0, 0, 0)  # Custom Black
    curses.init_color(10, 700, 400, 100) # Custom Brown
    curses.init_pair(1, curses.COLOR_WHITE, 0)  # Floor
    curses.init_pair(2, curses.COLOR_WHITE, 0)  # Wall
    curses.init_pair(3, 10, 0)  # Door
    curses.init_pair(4, curses.COLOR_CYAN, 0)  # Player
    stdscr.bkgd(' ', curses.color_pair(1))  # Set default background
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    curses.noecho()  # Don't echo keypresses
    stdscr.timeout(1000)  # Input timeout (ms)

    # Function to generate a new level and find player start position
    def reload_level():
        levelGenerator.generate_level()
        # Spawn player in the center room
        center_x = level.width // 2 + 3
        center_y = level.height // 2 + 3
        return center_x, center_y

    player_x, player_y = reload_level()  # Initialize player position

    while True:
        stdscr.clear()
        # Draw the dungeon map
        for x in range(level.height):
            for y in range(level.width):
                tile = level.level[x][y]
                if tile == '#':
                    stdscr.addstr(x, y, tile, curses.color_pair(2))  # Wall
                elif tile == '+':
                    stdscr.addstr(x, y, tile, curses.color_pair(3))  # Door
                elif tile == '.':
                    stdscr.addstr(x, y, tile, curses.color_pair(1))  # Floor
                else:
                    stdscr.addstr(x, y, tile, curses.color_pair(1))  # Other
        # Draw the player
        stdscr.addstr(player_y, player_x, '@', curses.color_pair(4))
        stdscr.refresh()

        key = stdscr.getch()  # Get user input
        if key == ord('q'):
            break  # Quit game
        elif key == ord('r'):
            player_x, player_y = reload_level()  # Reload dungeon
            continue
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

        # Move player if new position is valid
        new_x = player_x + dx
        new_y = player_y + dy
        if 0 <= new_y < level.height and 0 <= new_x < level.width:
            if level.level[new_y][new_x] in level.walkable:
                player_x, player_y = new_x, new_y


curses.wrapper(main)
