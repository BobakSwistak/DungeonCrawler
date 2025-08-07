import random
import Dungeon.level as level
import Enemies.enemyManager as enemyManager

def generate_dungeon():
    level.unwalkable.append(level.doors)
    # Initialize level and visible arrays as [y][x]
    level.level = [["#" for _ in range(level.width)] for _ in range(level.height)]
    level.visible = [[" " for _ in range(level.width)] for _ in range(level.height)]
    level.memorized = [[" " for _ in range(level.width)] for _ in range(level.height)]
    carve_room(10, 8, level.height // 2, level.width // 2)
    generate_rooms()
    generate_tunnels()
    generating_doors()
    clean_up()
    # Spawn player in the center room
    center_y = level.height // 2 + 3
    center_x = level.width // 2 + 3
    #enemyManager.generate_enemy("Skeleton")
    return center_y, center_x  # (y, x)


def generate_rooms():
    for _ in range(level.roomCount):
        minDistance = 9999
        nearestPlace = None
        room = carve_room()
        if room is None:
            continue
        for y in range(level.height):
            for x in range(level.width):
                if level.level[y][x] == ".":
                    if y > room[0] and y < room[2] and x > room[1] and x < room[3]:
                        continue
                    distance = ((y - room[0] + 3) ** 2 + (x - room[1] + 3) ** 2) ** 0.5
                    if distance < minDistance:
                        minDistance = distance
                        nearestPlace = (y, x)
        # print(nearestPlace, minDistance)
        startPos = (room[0] + room[2]) // 2, (room[1] + room[3]) // 2  # (y, x)
        endPos = nearestPlace
        carve_tunnel(startPos, endPos)


def generate_tunnels():
    for room in level.rooms:
        minDistance = 9999
        roomCenter = [(room[0] + room[2]) // 2, (room[1] + room[3]) // 2]  # (y, x)
        nearestRoom = None
        for other in level.rooms:
            if room != other:
                otherCenter = [(other[0] + other[2]) // 2, (other[1] + other[3]) // 2]
                distance = ((otherCenter[0] - roomCenter[0]) ** 2 + (otherCenter[1] - roomCenter[1]) ** 2) ** 0.5
                if distance < minDistance:
                    minDistance = distance
                    nearestRoom = otherCenter
        if nearestRoom:
            carve_tunnel(roomCenter, nearestRoom)


def carve_room(roomH=None, roomW=None, y=None, x=None):
    if roomH is None:
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        y = random.randint(1, level.height - roomH - 2)
        x = random.randint(1, level.width - roomW - 2)

    for j in range(roomH):
        for i in range(roomW):
            check_y = y + j
            check_x = x + i
            if check_y >= level.height or check_x >= level.width:
                # print('room check out of bounds')
                return None
            if level.level[check_y][check_x] != '#':
                # print('room already exists')
                return None
    for j in range(roomH):
        for i in range(roomW):
            level.level[y + j][x + i] = '#'

    for j in range(roomH - 2):
        for i in range(roomW - 2):
            level.level[y + j + 1][x + i + 1] = '.'
    room = [y, x, roomH + y, roomW + x]  # [y1, x1, y2, x2]
    level.rooms.append(room)
    return room


def carve_tunnel(startPos, endPos):
    # startPos and endPos are (y, x)
    if startPos[0] < endPos[0]:
        for y in range(startPos[0], endPos[0] + 1):
            level.level[y][startPos[1]] = '.'
    else:
        for y in range(endPos[0], startPos[0] + 1):
            level.level[y][startPos[1]] = '.'
    if startPos[1] < endPos[1]:
        for x in range(startPos[1], endPos[1] + 1):
            level.level[endPos[0]][x] = '.'
    else:
        for x in range(endPos[1], startPos[1] + 1):
            level.level[endPos[0]][x] = '.'


def carve_door(y, x):
    if random.random() < level.open_door_chance:
        level.level[y][x] = '`'
    elif random.random() < level.trapped_door_chance:
        level.level[y][x] = 't+'
    elif random.random() < level.hidden_door_chance:
        level.level[y][x] = 'h+'
    else:
        level.level[y][x] = '+'


def generating_doors():
    for y in range(1, level.height - 1):
        for x in range(1, level.width - 1):
            if level.level[y][x] == '.':
                if ((level.level[y - 1][x] == '#' and level.level[y + 1][x] == '#' and
                     level.level[y][x - 1] == '.' and level.level[y][x + 1] == '.') or
                        (level.level[y][x - 1] == '#' and level.level[y][x + 1] == '#' and
                         level.level[y - 1][x] == '.' and level.level[y + 1][x] == '.')):
                    if (level.level[y + 1][x + 1] == '.' or level.level[y + 1][x - 1] == '.' or
                            level.level[y - 1][x + 1] == '.' or level.level[y - 1][x - 1] == '.'):
                        carve_door(y, x)
            if level.level[y][x] == '#':
                if ((level.level[y - 1][x] == '.' and level.level[y + 1][x] == '.' and
                     level.level[y][x - 1] == '#' and level.level[y][x + 1] == '#') or
                        (level.level[y][x - 1] == '.' and level.level[y][x + 1] == '.' and
                         level.level[y - 1][x] == '#' and level.level[y + 1][x] == '#')):
                    if random.random() < level.random_door_chance:
                        carve_door(y, x)


def clean_up():
    for y in range(1, level.height - 1):
        for x in range(1, level.width - 1):
            if level.level[y][x] == '#':
                if ((level.level[y - 1][x] == '#' or level.level[y - 1][x] == ' ') and
                        (level.level[y + 1][x] == '#' or level.level[y + 1][x] == ' ') and
                        (level.level[y][x - 1] == '#' or level.level[y][x - 1] == ' ') and
                        (level.level[y][x + 1] == '#' or level.level[y][x + 1] == ' ') and
                        (level.level[y + 1][x + 1] == '#' or level.level[y + 1][x + 1] == ' ') and
                        (level.level[y + 1][x - 1] == '#' or level.level[y + 1][x - 1] == ' ') and
                        (level.level[y - 1][x + 1] == '#' or level.level[y - 1][x + 1] == ' ') and
                        (level.level[y - 1][x - 1] == '#' or level.level[y - 1][x - 1] == ' ')):
                    level.level[y][x] = ' '

    for y in range(level.height):
        level.level[y][0] = ' '
        level.level[y][level.width - 1] = ' '
    for x in range(level.width):
        level.level[0][x] = ' '
        level.level[level.height - 1][x] = ' '
