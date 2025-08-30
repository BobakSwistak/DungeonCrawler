import services

from Dungeon import level, levelManager, levelInit
from Dungeon.tiles import Tiles
from Enemies import enemies, enemyController, enemyManager
from Player import player, playerHp
from Resources import colors

master_offset = 30  # Reserve 30 columns on the left for a menu


def render_level(terminal, player_y, player_x):
    global offset_y, offset_x
    offset_y = max(0, min(player_y - levelInit.view_height // 2, levelInit.height - levelInit.view_height))
    offset_x = max(0, min(player_x - levelInit.view_width // 2, levelInit.width - levelInit.view_width))
    if not player.menu_opened:

        if levelInit.fog_of_war:
            render_fog_of_war(terminal, player_y, player_x)
        render_map(terminal, player_y, player_x)
    render_enemies(terminal)


def render_map(terminal, player_y, player_x):
    """    Loop through each cell in the viewport
    for y in range(levelInit.view_height):
        for x in range(levelInit.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            # Check if the map coordinates are within bounds
            if 0 <= map_y < levelInit.height and 0 <= map_x < levelInit.width:
                render_tile(level.current_level.memorized[map_y][map_x], x, y, terminal, colors.GREY,
                            colors.DARK_BROWN, colors.GREEN)"""

    # Calculate player's position in the viewport
    screen_y = player_y - offset_y
    screen_x = player_x - offset_x
    # Draw the player character '@' at their position in the viewport, shifted by master_offset

    for y in range(levelInit.view_height):
        for x in range(levelInit.view_width):
            map_y = offset_y + y
            map_x = offset_x + x
            if 0 <= map_y < levelInit.height and 0 <= map_x < levelInit.width:
                if level.current_level.visible[map_y][map_x]:
                    render_tile(level.current_level.level[map_y][map_x], x, y, terminal, colors.WHITE, colors.BROWN,
                                colors.GREEN)

    if 0 <= screen_y < levelInit.view_height and 0 <= screen_x < levelInit.view_width:
        terminal.color(services.get_color(playerHp.hp, playerHp.max_hp, colors.CYAN))
        terminal.printf(screen_x + master_offset, screen_y, '@')


def render_fog_of_war(terminal, player_y, player_x):
    # for y in range(3):
    #     for x in range(3):
    #         if 0 <= screen_y + y < levelInit.view_height and 0 <= screen_x + x < levelInit.view_width:
    #             level.current_level.visible[player_y + y - 1][player_x + x - 1] = ''
    fov = levelManager.calculate_field_of_view(player_y, player_x, 20)
    levelManager.player_fov(player_y, player_x, fov)
    for fov_tile in fov:
        level.current_level.memorized[fov_tile[0]][fov_tile[1]] = level.current_level.level[fov_tile[0]][fov_tile[1]]
    for y in range(levelInit.view_height):
        for x in range(levelInit.view_width):
            map_y = offset_y + y  # Map coordinate for current row (y)
            map_x = offset_x + x  # Map coordinate for current column (x)
            # Check if the map coordinates are within bounds
            if 0 <= map_y < levelInit.height and 0 <= map_x < levelInit.width:
                render_tile(level.current_level.memorized[map_y][map_x], x, y, terminal, colors.GREY, colors.DARK_BROWN,
                            colors.GREEN)


def render_tile(tile, x, y, terminal, wall_floor_color, door_color, other_color):
    if tile == Tiles.wall or tile == Tiles.floor:
        terminal.color(wall_floor_color)
        terminal.printf(x + master_offset, y, tile)  # Wall or Floor
    elif tile == Tiles.hidden_door:
        terminal.color(wall_floor_color)
        terminal.printf(x + master_offset, y, Tiles.wall)  # Hidden Door
    elif Tiles.is_door(tile):
        terminal.color(door_color)
        terminal.printf(x + master_offset, y, Tiles.closed_door)  # Door
    elif tile == Tiles.open_door:
        terminal.color(door_color)
        terminal.printf(x + master_offset, y, Tiles.open_door)  # Open Door
    else:
        terminal.color(other_color)
        terminal.printf(x + master_offset, y, tile)  # Default


def render_enemies(terminal):
    for enemy in enemies.enemies_list:
        if level.current_level.visible[enemy.enemy_pos[0]][enemy.enemy_pos[1]]:
            enemy.is_visible = True
            enemy_y, enemy_x = enemy.enemy_pos
            if offset_y <= enemy_y < offset_y + levelInit.view_height and offset_x <= enemy_x < offset_x + levelInit.view_width:
                screen_y = enemy_y - offset_y
                screen_x = enemy_x - offset_x
                terminal.color(services.get_color(enemy.hp, enemy.hp_max, enemy.color))
                terminal.printf(screen_x + master_offset, screen_y, enemy.enemy_symbol)
        else:
            enemy.is_visible = False
