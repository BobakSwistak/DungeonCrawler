import random
import Dungeon.level as level
import curses
import Renderers.menuRenderer as menuRenderer


def generate_level():
    level.level = [["#" for _ in range(level.width)] for _ in range(level.height)]
    level.visible = [[" " for _ in range(level.width)] for _ in range(level.height)]
    carve_room(10, 8, level.height // 2, level.width // 2)
    generate_rooms()
    generate_tunnels()
    generating_doors()
    clean_up()


def reload_level(stdscr):
    generate_level()
    # Spawn player in the center room
    center_x = level.width // 2 + 3
    center_y = level.height // 2 + 3
    return center_x, center_y


def generate_rooms():
    for _ in range(level.roomCount):
        minDistance = 9999
        nearestPlace = None
        room = carve_room()
        if room is None:
            continue
        for x in range(level.height):
            for y in range(level.width):
                if level.level[x][y] == ".":
                    if x > room[0] and x < room[2] and y > room[1] and y < room[3]:
                        continue
                    distance = ((x - room[0] + 3) ** 2 + (y - room[1] + 3) ** 2) ** 0.5
                    if distance < minDistance:
                        minDistance = distance
                        nearestPlace = (x, y)
        # print(nearestPlace, minDistance)
        startPos = (room[0] + room[2]) // 2, (room[1] + room[3]) // 2
        endPos = nearestPlace
        carve_tunnel(startPos, endPos)


def generate_tunnels():
    for room in level.rooms:
        minDistance = 9999
        roomCenter = [(room[0] + room[2]) // 2, (room[1] + room[3]) // 2]
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


def carve_room(roomW=None, roomH=None, x=None, y=None):
    if roomW is None:
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        x = random.randint(1, level.height - roomH - 2)
        y = random.randint(1, level.width - roomW - 2)

    for i in range(roomH):
        for j in range(roomW):
            check_x = x + i
            check_y = y + j
            if check_x >= level.height or check_y >= level.width:
                # print('room check out of bounds')
                return None
            if level.level[check_x][check_y] != '#':
                # print('room already exists')
                return None
    for i in range(roomH):
        for j in range(roomW):
            level.level[x + i][y + j] = '#'

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[x + i + 1][y + j + 1] = '.'
    room = [x, y, roomH + x, roomW + y]
    level.rooms.append(room)
    return room


def carve_tunnel(startPos, endPos):
    if startPos[0] < endPos[0]:
        for i in range(startPos[0], endPos[0] + 1):
            level.level[i][startPos[1]] = '.'
    else:
        for i in range(endPos[0], startPos[0] + 1):
            level.level[i][startPos[1]] = '.'
    if startPos[1] < endPos[1]:
        for j in range(startPos[1], endPos[1] + 1):
            level.level[endPos[0]][j] = '.'
    else:
        for j in range(endPos[1], startPos[1] + 1):
            level.level[endPos[0]][j] = '.'


def generating_doors():
    for x in range(level.height):
        for y in range(level.width):
            if level.level[x][y] == '.':
                if ((level.level[x - 1][y] == '#' and level.level[x + 1][y] == '#' and
                     level.level[x][y - 1] == '.' and level.level[x][y + 1] == '.') or
                        (level.level[x][y - 1] == '#' and level.level[x][y + 1] == '#' and
                         level.level[x - 1][y] == '.' and level.level[x + 1][y] == '.')):
                    if (level.level[x + 1][y + 1] == '.' or level.level[x + 1][y - 1] == '.' or
                            level.level[x - 1][y + 1] == '.' or level.level[x - 1][y - 1] == '.'):
                        if random.random() < level.open_door_chance:
                            level.level[x][y] = '`'
                        else:
                            level.level[x][y] = '+'
            if level.level[x][y] == '#':
                if ((level.level[x - 1][y] == '.' and level.level[x + 1][y] == '.' and
                     level.level[x][y - 1] == '#' and level.level[x][y + 1] == '#') or
                        (level.level[x][y - 1] == '.' and level.level[x][y + 1] == '.' and
                         level.level[x - 1][y] == '#' and level.level[x + 1][y] == '#')):
                    if random.random() < level.random_door_chance:
                        if random.random() < level.open_door_chance:
                            level.level[x][y] = '`'
                        else:
                            level.level[x][y] = '+'


def clean_up():
    for x in range(0, level.height - 1):
        for y in range(0, level.width - 1):
            if level.level[x][y] == '#':
                if ((level.level[x - 1][y] == '#' or level.level[x - 1][y] == ' ') and
                        (level.level[x + 1][y] == '#' or level.level[x + 1][y] == ' ') and
                        (level.level[x][y - 1] == '#' or level.level[x][y - 1] == ' ') and
                        (level.level[x][y + 1] == '#' or level.level[x][y + 1] == ' ') and
                        (level.level[x + 1][y + 1] == '#' or level.level[x + 1][y + 1] == ' ') and
                        (level.level[x + 1][y - 1] == '#' or level.level[x + 1][y - 1] == ' ') and
                        (level.level[x - 1][y + 1] == '#' or level.level[x - 1][y + 1] == ' ') and
                        (level.level[x - 1][y - 1] == '#' or level.level[x - 1][y - 1] == ' ')):
                    level.level[x][y] = ' '

    for x in range(level.height):
        level.level[x][0] = ' '
        level.level[x][level.width - 1] = ' '
    for y in range(level.width):
        level.level[0][y] = ' '
        level.level[level.height - 1][y] = ' '
