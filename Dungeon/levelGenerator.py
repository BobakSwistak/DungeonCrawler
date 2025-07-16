import random
import Dungeon.level as level


def generate_level():
    # Outer list is rows (x), inner is columns (y)
    level.level = [["#" for _ in range(level.width)] for _ in range(level.height)]
    # generate_room(10, 10, 1, 1)
    # generate_room(10, 10, 1, 20)
    # connect_rooms()
    for _ in range(random.randint(level.roomCount[0], level.roomCount[1])):
        generate_room()
    connect_rooms()
    return level.level


def generate_room(roomW=None, roomH=None, x=None, y=None, force=False):
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
                return
            if level.level[check_x][check_y] != '#' and not force:
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


def generate_tunnel(room, otherRoom):
    # todo add tunnel generation.
    # This function will create a tunnel between two rooms from center to center.
    return


def connect_rooms():
    for room in level.rooms:
        for otherRoom in level.rooms:
            can_continue = True
            if room == otherRoom:
                continue
            # creating a tunnel between two rooms from center to center using .
            room_pos = [random.randint(room[0] + 2, room[2] - 2),
                        random.randint(room[1] + 2, room[3] - 2)]
            other_room_pos = [random.randint(otherRoom[0] + 2, otherRoom[2] - 2),
                              random.randint(otherRoom[1] + 2, otherRoom[3] - 2)]
            for i in level.roomsConnected:
                if i == [room[4], otherRoom[4]] or i == [otherRoom[4], room[4]]:
                    print('rooms already connected')
                    can_continue = False
                    break
            if can_continue:
                print('connecting rooms')
                level.roomsConnected.append([room[4], otherRoom[4]])
                generate_tunnel(room_pos, other_room_pos)
