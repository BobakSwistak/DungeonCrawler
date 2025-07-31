from Dungeon import level, levelManager
import curses

master_offset = 30  # Reserve 30 columns on the left for a menu


def renderer(stdscr, player_y, player_x):
    global offset_y, offset_x
    offset_y = max(0, min(player_y - level.view_height // 2, level.height - level.view_height))
    offset_x = max(0, min(player_x - level.view_width // 2, level.width - level.view_width))
    render_map(stdscr, player_y, player_x)
    # if level.fog_of_war:
    render_fog_of_war(stdscr, player_y, player_x)


def render_map(stdscr, player_y, player_x):
    # Loop through each cell in the viewport
    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            # Check if the map coordinates are within bounds
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                tile = level.level[map_y][map_x]
                # Draw each tile with its corresponding color, shifted by master_offset
                if tile == '#' or tile == '.':
                    stdscr.addstr(y, x + master_offset, tile, curses.color_pair(2))  # Wall or Floor
                elif tile in level.doors:
                    stdscr.addstr(y, x + master_offset, "+", curses.color_pair(4))  # Door
                elif tile == '`':
                    stdscr.addstr(y, x + master_offset, "`", curses.color_pair(4))  # open Door
                else:
                    stdscr.addstr(y, x + master_offset, tile, curses.color_pair(2))  # Default

    # Calculate player's position in the viewport
    screen_y = player_y - offset_y
    screen_x = player_x - offset_x
    # Draw the player character '@' at their position in the viewport, shifted by master_offset

    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y
            map_x = offset_x + x
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                if level.visible[map_y][map_x]:
                    tile = level.level[map_y][map_x]
                    if tile == '#' or tile == '.':
                        stdscr.addstr(y, x + master_offset, tile, curses.color_pair(1))  # Wall or Floor
                    elif tile in level.doors:
                        stdscr.addstr(y, x + master_offset, "+", curses.color_pair(3))  # Door
                    elif tile == '`':
                        stdscr.addstr(y, x + master_offset, "`", curses.color_pair(3))  # open Door
                    else:
                        stdscr.addstr(y, x + master_offset, tile, curses.color_pair(1))  # Default

    if 0 <= screen_y < level.view_height and 0 <= screen_x < level.view_width:
        stdscr.addstr(screen_y, screen_x + master_offset, '@', curses.color_pair(5))


def render_fog_of_war(stdscr, player_y, player_x):
    # for y in range(3):
    #     for x in range(3):
    #         if 0 <= screen_y + y < level.view_height and 0 <= screen_x + x < level.view_width:
    #             level.visible[player_y + y - 1][player_x + x - 1] = ''
    levelManager.calculate_field_of_view(player_y, player_x, 20)
    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                stdscr.addstr(y, x + master_offset, level.memorized[map_y][map_x], curses.color_pair(1))
