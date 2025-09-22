from Dungeon import level, levelInit
from Resources.tiles import Tiles


def bresenham_line(y0, x0, y1, x1):
    """Generate points on a line from (y0, x0) to (y1, x1)."""
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        points.append((y0, x0))
        if y0 == y1 and x0 == x1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points


def calculate_field_of_view(player_x, player_y, radius):
    # local_visible[x][y]
    local_visible = [[False for _ in range(levelInit.width)] for _ in range(levelInit.height)]
    for x in range(player_x - radius, player_x + radius + 1):
        for y in range(player_y - radius, player_y + radius + 1):
            if 0 <= x < levelInit.height and 0 <= y < levelInit.width:
                line = bresenham_line(player_x, player_y, x, y)
                for (ly, lx) in line:
                    if 0 <= ly < levelInit.height and 0 <= lx < levelInit.width:
                        local_visible[ly][lx] = True
                        if Tiles.is_unwalkable(level.current_level.level[ly][lx]):
                            break
    return local_visible


def player_fov(player_x, player_y, local_visible):
    for x in range(levelInit.height):
        for y in range(levelInit.width):
            if local_visible[x][y]:
                level.current_level.memorized[x][y] = level.current_level.level[x][y]
    level.current_level.visible = local_visible
