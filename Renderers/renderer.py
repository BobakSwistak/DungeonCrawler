import Dungeon.level as level
import curses

master_offset = 30  # Reserve 30 columns on the left for a menu


def rendering_map(stdscr, player_x, player_y):
    fog_of_war = False
    # Calculate the top-left corner of the viewport so the player stays centered
    offset_x = max(0, min(player_x - level.view_width // 2, level.width - level.view_width))
    offset_y = max(0, min(player_y - level.view_height // 2, level.height - level.view_height))

    # Loop through each cell in the viewport
    for x in range(level.view_height):
        for y in range(level.view_width):
            map_x = offset_y + x  # Map coordinate for current row
            map_y = offset_x + y  # Map coordinate for current column
            # Check if the map coordinates are within bounds
            if 0 <= map_x < level.height and 0 <= map_y < level.width:
                tile = level.level[map_x][map_y]
                # Draw each tile with its corresponding color, shifted by master_offset
                if tile == '#':
                    stdscr.addstr(x, y + master_offset, tile, curses.color_pair(2))  # Wall
                elif tile == '+' or tile == '`':
                    stdscr.addstr(x, y + master_offset, tile, curses.color_pair(3))  # Door
                elif tile == '.':
                    stdscr.addstr(x, y + master_offset, tile, curses.color_pair(1))  # Floor
                else:
                    stdscr.addstr(x, y + master_offset, tile, curses.color_pair(1))  # Default

    # Calculate player's position in the viewport
    screen_x = player_x - offset_x
    screen_y = player_y - offset_y
    # Draw the player character '@' at their position in the viewport, shifted by master_offset
    if 0 <= screen_x < level.view_width and 0 <= screen_y < level.view_height:
        stdscr.addstr(screen_y, screen_x + master_offset, '@', curses.color_pair(4))
    if fog_of_war:
        for x in range(3):
            for y in range(3):
                if 0 <= screen_y + y < level.view_height and 0 <= screen_x + x < level.view_width:
                    level.visible[player_y + y - 1][player_x + x - 1] = ''

        for x in range(level.view_height):
            for y in range(level.view_width):
                map_x = offset_y + x  # Map coordinate for current row
                map_y = offset_x + y  # Map coordinate for current column
                if 0 <= map_x < level.height and 0 <= map_y < level.width:
                    stdscr.addstr(x, y + master_offset, level.visible[map_x][map_y], curses.color_pair(1))

    # for i in range(level.view_height):
    #     stdscr.addstr(i, level.view_width, '|')
    # for j in range(level.view_width+1):
    #     stdscr.addstr(level.view_height, j, '-')
