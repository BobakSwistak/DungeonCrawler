import Dungeon.level as level
import curses



def rendering_map(stdscr):
    for x in range(level.height):
        for y in range(level.width):
            tile = level.level[x][y]
            if tile == '#':
                stdscr.addstr(x, y, tile, curses.color_pair(2))  # Wall
            elif tile == '+' or tile == '`':
                stdscr.addstr(x, y, tile, curses.color_pair(3))  # Doors
            elif tile == '.':
                stdscr.addstr(x, y, tile, curses.color_pair(1))  # Floor
            else:
                stdscr.addstr(x, y, tile, curses.color_pair(1))  # Other
