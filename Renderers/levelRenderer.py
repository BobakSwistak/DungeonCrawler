import services

from Dungeon import level, levelInit
from Resources.tiles import Tiles
from Player import playerHp
from Resources import colors, offsets
from Renderers import fieldOfView

offset_x, offset_y = 0, 0


def render_level(terminal, player_x, player_y):
    global offset_x, offset_y
    offset_x = max(0, min(player_x - levelInit.view_height // 2, levelInit.height - levelInit.view_height))
    offset_y = max(0, min(player_y - levelInit.view_width // 2, levelInit.width - levelInit.view_width))

    if levelInit.fog_of_war:
        render_fog_of_war(terminal, player_x, player_y)
    render_map(terminal, player_x, player_y)
    render_enemies(terminal)


def render_map(terminal, player_x, player_y):
    # Calculate player's position in the viewport
    screen_x = player_x - offset_x
    screen_y = player_y - offset_y

    for x in range(levelInit.view_height):
        for y in range(levelInit.view_width):
            map_x = offset_x + x
            map_y = offset_y + y
            if 0 <= map_x < levelInit.height and 0 <= map_y < levelInit.width:
                if level.current_level.visible[map_x][map_y] or not levelInit.fog_of_war:
                    render_tile(level.current_level.level[map_x][map_y], y, x, terminal, colors.WHITE, colors.BROWN,
                                colors.GREEN)

    if 0 <= screen_x < levelInit.view_height and 0 <= screen_y < levelInit.view_width:
        terminal.color(services.get_color(playerHp.hp, playerHp.max_hp, colors.CYAN))
        terminal.printf(screen_y + offsets.level_offset, screen_x + offsets.top_offset, '@')


def render_fog_of_war(terminal, player_x, player_y):
    # for x in range(3):
    #     for y in range(3):
    #         if 0 <= screen_x + x < levelInit.view_height and 0 <= screen_y + y < levelInit.view_width:
    #             level.current_level.visible[player_x + x - 1][player_y + y - 1] = ''
    fov = fieldOfView.calculate_field_of_view(player_x, player_y, 20)
    fieldOfView.player_fov(player_x, player_y, fov)
    for fov_tile in fov:
        level.current_level.memorized[fov_tile[0]][fov_tile[1]] = level.current_level.level[fov_tile[0]][fov_tile[1]]
    for x in range(levelInit.view_height):
        for y in range(levelInit.view_width):
            map_x = offset_x + x  # Map coordinate for current row (x)
            map_y = offset_y + y  # Map coordinate for current column (y)
            # Check if the map coordinates are within bounds
            if 0 <= map_x < levelInit.height and 0 <= map_y < levelInit.width:
                render_tile(level.current_level.memorized[map_x][map_y], y, x, terminal, colors.GREY, colors.DARK_BROWN,
                            colors.GREEN)


def render_tile(tile, y, x, terminal, wall_floor_color, door_color, other_color):
    if tile == Tiles.wall or tile == Tiles.floor:
        terminal.color(wall_floor_color)
        terminal.printf(y + offsets.level_offset, x + offsets.top_offset, tile)  # Wall or Floor
    elif tile == Tiles.hidden_door:
        terminal.color(wall_floor_color)
        terminal.printf(y + offsets.level_offset, x + offsets.top_offset, Tiles.wall)  # Hidden Door
    elif Tiles.is_door(tile):
        terminal.color(door_color)
        terminal.printf(y + offsets.level_offset, x + offsets.top_offset, Tiles.closed_door)  # Door
    elif tile == Tiles.open_door:
        terminal.color(door_color)
        terminal.printf(y + offsets.level_offset, x + offsets.top_offset, Tiles.open_door)  # Open Door
    else:
        terminal.color(other_color)
        terminal.printf(y + offsets.level_offset, x + offsets.top_offset, tile)  # Default


def render_enemies(terminal):
    for enemy in level.current_level.enemies_list:
        if level.current_level.visible[enemy.enemy_pos[0]][enemy.enemy_pos[1]] or not levelInit.fog_of_war:
            enemy.is_visible = True
            enemy_x, enemy_y = enemy.enemy_pos
            if offset_x <= enemy_x < offset_x + levelInit.view_height and offset_y <= enemy_y < offset_y + levelInit.view_width:
                screen_x = enemy_x - offset_x
                screen_y = enemy_y - offset_y
                terminal.color(services.get_color(enemy.hp, enemy.hp_max, enemy.color))
                terminal.printf(screen_y + offsets.level_offset, screen_x + offsets.top_offset, enemy.enemy_symbol)
        else:
            enemy.is_visible = False
