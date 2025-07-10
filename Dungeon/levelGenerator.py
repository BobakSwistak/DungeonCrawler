import random
import Dungeon.level as level


def generate_level():
    # Outer list is rows (x), inner is columns (y)
    level.level = [["." for _ in range(level.width)] for _ in range(level.height)]
    generate_room(10, 10, 1, 1)
    generate_room(10, 10, 1, 20)
    connect_rooms()
    # for _ in range(random.randint(level.roomCount[0], level.roomCount[1])):
    #     generate_room()
    # connect_rooms()
    return level.level


def generate_room(roomW=None, roomH=None, x=None, y=None, force=False):
    if roomW is None:
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        x = random.randint(1, level.height - roomH - 1)
        y = random.randint(1, level.width - roomW - 1)

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            check_x = x + i + 1
            check_y = y + j + 1
            if check_x >= level.height or check_y >= level.width:
                print('room check out of bounds')
                return
            if level.level[check_x][check_y] != '.' and not force:
                print('room already exists')
                return
    number = len(level.rooms) + 1
    if not force:
        level.rooms.append((x, y, x + roomH, y + roomW, number))
    for i in range(roomH):
        for j in range(roomW):
            level.level[x + i][y + j] = '#'

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[x + i + 1][y + j + 1] = '.'





def connect_rooms():
    for room in range(level.rooms):
        for i in range(3):
            # finding nearest room
            nearest_room = None
            nearest_distance = 9999
            for other_room in level.rooms:
                if room == other_room:
                    continue
                distance = abs(room[0] - other_room[0]) + abs(room[1] - other_room[1])
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_room = other_room

