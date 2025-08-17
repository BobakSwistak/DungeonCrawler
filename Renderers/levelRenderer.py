from Dungeon import level, levelManager
from Enemies import enemies, enemyController, enemyManager
from Player import player, playerHp
from Resources import colors
import services

master_offset = 30  # Reserve 30 columns on the left for a menu


def render_level(terminal, player_y, player_x):
    global offset_y, offset_x
    offset_y = max(0, min(player_y - level.view_height // 2, level.height - level.view_height))
    offset_x = max(0, min(player_x - level.view_width // 2, level.width - level.view_width))
    if not player.menu_opened:

        if level.fog_of_war:
            render_fog_of_war(terminal, player_y, player_x)
        render_map(terminal, player_y, player_x)
    render_enemies(terminal)


def render_map(terminal, player_y, player_x):
    # Loop through each cell in the viewport
    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            # Check if the map coordinates are within bounds
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                tile = level.memorized[map_y][map_x]
                # Draw each tile with its corresponding color, shifted by master_offset
                if tile == '#' or tile == '.':
                    terminal.color(colors.GREY)
                    terminal.printf(x + master_offset, y, tile)  # Wall or Floor
                elif tile == 'h+':
                    terminal.color(colors.GREY)
                    terminal.printf(x + master_offset, y, '#')  # Hidden Door
                elif tile in level.doors:
                    terminal.color(colors.DARK_BROWN)
                    terminal.printf(x + master_offset, y, "+")  # Door
                elif tile == '`':
                    terminal.color(colors.DARK_BROWN)
                    terminal.printf(x + master_offset, y, "`")  # Open Door
                else:
                    terminal.color(colors.GREY)
                    terminal.printf(x + master_offset, y, tile)  # Default

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
                        terminal.color(colors.WHITE)
                        terminal.printf(x + master_offset, y, tile)  # Wall or Floor
                    if tile == 'h+':
                        terminal.color(colors.WHITE)
                        terminal.printf(x + master_offset, y, '#')
                    elif tile in level.doors:
                        terminal.color(colors.BROWN)
                        terminal.printf(x + master_offset, y, "+")  # Door
                    elif tile == "`":
                        terminal.color(colors.BROWN)
                        terminal.printf(x + master_offset, y, "`")  # open Door
                    else:
                        terminal.color(colors.WHITE)
                        terminal.printf(x + master_offset, y, tile)  # Default

    if 0 <= screen_y < level.view_height and 0 <= screen_x < level.view_width:
        terminal.color(services.get_color(playerHp.hp, playerHp.max_hp, colors.CYAN))
        terminal.printf(screen_x + master_offset, screen_y, '@')


def render_fog_of_war(terminal, player_y, player_x):
    # for y in range(3):
    #     for x in range(3):
    #         if 0 <= screen_y + y < level.view_height and 0 <= screen_x + x < level.view_width:
    #             level.visible[player_y + y - 1][player_x + x - 1] = ''
    fov = levelManager.calculate_field_of_view(player_y, player_x, 20)
    levelManager.player_fov(player_y, player_x, fov)
    for fov_tile in fov:
        level.memorized[fov_tile[0]][fov_tile[1]] = level.level[fov_tile[0]][fov_tile[1]]
    for y in range(level.view_height):
        for x in range(level.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            # Check if the map coordinates are within bounds
            if 0 <= map_y < level.height and 0 <= map_x < level.width:
                tile = level.memorized[map_y][map_x]
                # Draw each tile with its corresponding color, shifted by master_offset
                if tile == '#' or tile == '.':
                    terminal.color(colors.GREY)
                    terminal.printf(x + master_offset, y, tile)  # Wall or Floor
                elif tile == 'h+':
                    terminal.color(colors.GREY)
                    terminal.printf(x + master_offset, y, '#')  # Hidden Door
                elif tile in level.doors:
                    terminal.color(colors.DARK_BROWN)
                    terminal.printf(x + master_offset, y, "+")  # Door
                elif tile == '`':
                    terminal.color(colors.DARK_BROWN)
                    terminal.printf(x + master_offset, y, "`")  # Open Door
                else:
                    terminal.color(colors.RED)
                    terminal.printf(x + master_offset, y, tile)  # Default



def render_enemies(terminal):
    for enemy in enemies.enemies_list:
        if level.visible[enemy.enemy_pos[0]][enemy.enemy_pos[1]]:
            enemy.is_visible = True
            enemy_y, enemy_x = enemy.enemy_pos
            if offset_y <= enemy_y < offset_y + level.view_height and offset_x <= enemy_x < offset_x + level.view_width:
                screen_y = enemy_y - offset_y
                screen_x = enemy_x - offset_x
                terminal.color(services.get_color(enemy.hp, enemy.hp_max, enemy.color))
                terminal.printf(screen_x + master_offset, screen_y, enemy.enemy_symbol)
        else:
            enemy.is_visible = False