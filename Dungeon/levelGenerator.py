import random
import Dungeon.level as level


def generate_level():
    # Outer list is rows (x), inner is columns (y)
    level.level = [["." for _ in range(level.width)] for _ in range(level.height)]
    # generate_room(10, 10, 1, 1)
    # generate_room(10, 10, 1, 20)
    # connect_rooms()
    for _ in range(random.randint(level.roomCount[0], level.roomCount[1])):
        generate_room()
    connect_rooms()
    clean_Up()
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
    level.rooms_tech.append((x, y, x + roomH, y + roomW, number))
    for i in range(roomH):
        for j in range(roomW):
            level.level[x + i][y + j] = '#'

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[x + i + 1][y + j + 1] = '.'


def connect_rooms():
    # If there are no rooms, nothing to connect
    if not level.rooms:
        return
    connected = [level.rooms[0]]  # Start with the first room as connected
    unconnected = level.rooms[1:]  # The rest are unconnected
    while unconnected:
        min_dist = float('inf')
        to_connect = None
        from_room = None
        # Find the closest pair: one from connected, one from unconnected
        for room in connected:
            room_cx = (room[0] + room[2]) // 2
            room_cy = (room[1] + room[3]) // 2
            for other_room in unconnected:
                other_cx = (other_room[0] + other_room[2]) // 2
                other_cy = (other_room[1] + other_room[3]) // 2
                distance = ((room_cx - other_cx) ** 2 + (room_cy - other_cy) ** 2) ** 0.5
                if distance < min_dist:
                    min_dist = distance
                    to_connect = other_room
                    from_room = room
        # Connect the closest unconnected room to the connected set
        if to_connect and from_room:
            connection = (from_room[4], to_connect[4])
            reverse_connection = (to_connect[4], from_room[4])
            # Avoid duplicate connections
            if connection not in level.roomsConnected and reverse_connection not in level.roomsConnected:
                generate_corridor(from_room, to_connect)
                level.roomsConnected.append(connection)
            connected.append(to_connect)
            unconnected.remove(to_connect)


def generate_corridor(room, other_room):
    # Calculate center points of both rooms
    room_cx = (room[0] + room[2]) // 2
    room_cy = (room[1] + room[3]) // 2
    other_cx = (other_room[0] + other_room[2]) // 2
    other_cy = (other_room[1] + other_room[3]) // 2

    # Create a vertical corridor from the first room's center to the target row
    if room_cx != other_cx:
        x1 = min(room_cx, other_cx)
        length = abs(room_cx - other_cx) + 1
        generate_room(roomW=3, roomH=length, x=x1, y=room_cy - 1, force=True)
        corridor_end_x = other_cx
        corridor_end_y = room_cy
    else:
        corridor_end_x = room_cx
        corridor_end_y = room_cy

    # Create a horizontal corridor from the end of the vertical corridor to the target column
    if corridor_end_y != other_cy:
        if corridor_end_y < room_cy:
            # corridor goes left
            y1 = min(corridor_end_y, other_cy)
            length = abs(corridor_end_y - other_cy) + 1
            generate_room(roomW=length, roomH=3, x=corridor_end_x, y=y1 - 1, force=True)
        else:
            # corridor goes right
            y1 = min(corridor_end_y, other_cy)
            length = abs(corridor_end_y - other_cy) + 1
            generate_room(roomW=length, roomH=3, x=corridor_end_x, y=y1 + 1, force=True)


def clean_Up():
    for i in level.rooms_tech:
        # clean each room inside to .
        for x in range(i[0] + 1, i[2] - 1):
            for y in range(i[1] + 1, i[3] - 1):
                level.level[x][y] = '.'
