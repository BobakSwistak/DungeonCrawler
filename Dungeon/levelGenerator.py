import random
import Dungeon.level as level


def generate_level():
    level.level = [["." for _ in range(level.width)] for _ in range(level.height)]

    for i in range(random.randint(level.roomCount[0], level.roomCount[1])):
        generate_room()
    for i in range(1000):
        generate_corridors()
    return level.level


def generate_room(roomW=None, roomH=None, x=None, y=None):
    if roomW == None:
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        x = random.randint(1, level.width - roomW - 1)
        y = random.randint(1, level.height - roomH - 1)

    for i in range(roomH):
        for j in range(roomW):
            if level.level[y + i][x + j] != '.':
                return
    level.rooms.append((x, y, x + roomW, y + roomH))
    for i in range(roomH):
        for j in range(roomW):
            level.level[y + i][x + j] = '#'

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[y + i + 1][x + j + 1] = '.'


def generate_corridors():
    for i in range(1, level.height - 1):
        for j in range(1, level.width - 1):
            if level.level[i][j] == '#':
                for room in level.rooms:
                    if room[1] <= i < room[3] and room[0] <= j < room[2]:
                        # Check vertical corridor possibility
                        if level.level[i + 1][j] != '.' and level.level[i - 1][j] != '.':
                            center_x = (room[0] + room[2]) // 2
                            generate_corridor_horizontal(i, j, right=(j < center_x))
                        # Check horizontal corridor possibility
                        if level.level[i][j + 1] != '.' and level.level[i][j - 1] != '.':
                            center_y = (room[1] + room[3]) // 2
                            generate_corridor_vertical(i, j, up=(i < center_y))
                        break  # No need to check other rooms for this cell

def generate_corridor_vertical(i, j, up=True, first=True):
    direction = 1 if up else -1
    max_length = random.randint(level.corridorLength[0], level.corridorLength[1])
    for c in range(max_length):
        ni = i + c * direction
        if not (0 <= ni < level.height):
            break
        if level.level[ni][j] == '#':
            for k in range(c):
                level.level[i + k * direction][j] = '|'
            return
    if first:
        ni = i + max_length * direction
        if 0 <= ni < level.height:
            generate_corridor_horizontal(ni, j, right=bool(random.getrandbits(1)), first=False)

def generate_corridor_horizontal(i, j, right=True, first=True):
    direction = 1 if right else -1
    max_length = random.randint(level.corridorLength[0], level.corridorLength[1])
    for c in range(max_length):
        nj = j + c * direction
        if not (0 <= nj < level.width):
            break
        if level.level[i][nj] == '#':
            for k in range(c):
                level.level[i][j + k * direction] = '-'
            return
    if first:
        nj = j + max_length * direction
        if 0 <= nj < level.width:
            generate_corridor_vertical(i, nj, up=bool(random.getrandbits(1)), first=False)