import random
import Dungeon.level as level
from Dungeon.level import roomCount


def generate_level():
    level.level = [["#" for _ in range(level.width)] for _ in range(level.height)]
    carve_room(10, 8, level.height // 2, level.width // 2)
    generate_rooms()


def generate_rooms():
    for _ in range(random.randint(roomCount[0], roomCount[1])):
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
                    distance = ((x - room[0]) ** 2 + (y - room[1]) ** 2) ** 0.5
                    if distance < minDistance:
                        minDistance = distance
                        nearestPlace = (x, y)
        print(nearestPlace, minDistance)
        # we found nearest place join our new room to our room web.
        # creating a tunnel to the nearest place
        # first by the x-axis then by the y-axis
        startPos = (room[0] + room[2]) // 2, (room[1] + room[3]) // 2
        endPos = nearestPlace
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


def carve_room(roomW=None, roomH=None, x=None, y=None):
    if roomW is None:
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        x = random.randint(1, level.height - roomH - 1)
        y = random.randint(1, level.width - roomW - 1)

    for i in range(roomH):
        for j in range(roomW):
            check_x = x + i
            check_y = y + j
            if check_x >= level.height or check_y >= level.width:
                print('room check out of bounds')
                return None
            if level.level[check_x][check_y] != '#':
                print('room already exists')
                return None
    for i in range(roomH):
        for j in range(roomW):
            level.level[x + i][y + j] = '#'

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[x + i + 1][y + j + 1] = '.'
    return [x, y, roomH + x, roomW + y]

# todo: add a function which cleans up the level and add toors
