import Dungeon.level as level
from Dungeon.level import visible


def bresenham_line(x0, y0, x1, y1):
    """Generate points on a line from (x0, y0) to (x1, y1)."""
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
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
    local_visible = [[False for _ in range(level.width)] for _ in range(level.height)]

    for y in range(player_y - radius, player_y + radius + 1):
        for x in range(player_x - radius, player_x + radius + 1):
            if 0 <= x < level.width and 0 <= y < level.height:
                line = bresenham_line(player_x, player_y, x, y)
                for (lx, ly) in line:
                    if 0 <= lx < level.width and 0 <= ly < level.height:
                        local_visible[ly][lx] = True
                        if level.level[ly][lx] in level.unwalkable:
                            break  # stop ray on wall

    # Update the global visible variable
    for y in range(level.height):
        for x in range(level.width):
            if local_visible[y][x]:
                level.visible[y][x] = ''
