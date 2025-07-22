from Dungeon import level


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


def calculate_field_of_view(player_y, player_x, radius):
    # local_visible[y][x]
    local_visible = [[False for _ in range(level.width)] for _ in range(level.height)]
    for y in range(player_y - radius, player_y + radius + 1):
        for x in range(player_x - radius, player_x + radius + 1):
            if 0 <= y < level.height and 0 <= x < level.width:
                line = bresenham_line(player_y, player_x, y, x)
                for (ly, lx) in line:
                    if 0 <= ly < level.height and 0 <= lx < level.width:
                        local_visible[ly][lx] = True
                        if level.level[ly][lx] in level.unwalkable:
                            break
    for y in range(level.height):
        for x in range(level.width):
            if local_visible[y][x]:
                level.memorized[y][x] = ''
    for y in range(level.height):
        for x in range(level.width):
            if local_visible[y][x]:
                level.visible[y][x] = True
            else:
                level.visible[y][x] = False
