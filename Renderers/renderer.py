from Dungeon import level, levelManager
import curses

# xy solved

master_offset = 30  # Reserve 30 columns on the left for a menu


def rendering_map(stdscr, player_y, player_x):
    fog_of_war = True
    # Calculate the top-left corner of the viewport so the player stays centered
    offset_y = max(0, min(player_y - level.view_height // 2, level.height - level.view_height))
    offset_x = max(0, min(player_x - level.view_width // 2, level.width - level.view_width))

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
                    stdscr.addstr(y, x + master_offset, tile, curses.color_pair(5))  # Wall or Floor
                elif tile == '+' or tile == '`':
                    stdscr.addstr(y, x + master_offset, tile, curses.color_pair(7))  # Door
                else:
                    stdscr.addstr(y, x + master_offset, tile, curses.color_pair(5))  # Default

    # Calculate player's position in the viewport
    screen_y = player_y - offset_y
    screen_x = player_x - offset_x
    # Draw the player character '@' at their position in the viewport, shifted by master_offset

    if fog_of_war:
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

    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y
            map_x = offset_x + x
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                if level.visible[map_y][map_x]:
                    tile = level.level[map_y][map_x]
                    if tile == '#' or tile == '.':
                        stdscr.addstr(y, x + master_offset, tile, curses.color_pair(1))  # Wall or Floor
                    elif tile == '+' or tile == '`':
                        stdscr.addstr(y, x + master_offset, tile, curses.color_pair(2))  # Door
                    else:
                        stdscr.addstr(y, x + master_offset, tile, curses.color_pair(1))  # Default

    if 0 <= screen_y < level.view_height and 0 <= screen_x < level.view_width:
        stdscr.addstr(screen_y, screen_x + master_offset, '@', curses.color_pair(3))
# for y in range(level.view_height):
#     stdscr.addstr(y, level.view_width, '|')
# for x in range(level.view_width+1):
#     stdscr.addstr(level.view_height, x, '-')
