import random
import Enemies.enemyManager as enemyManager

from Dungeon import level, levelInit
from Resources.tiles import Tiles

local_level = []
local_occupied = []
local_visible = []
local_memorized = []
local_rooms = []


def generate_dungeon():
    global local_level, local_occupied, local_visible, local_memorized, local_rooms
    # Initialize level and visible arrays as [y][x]
    local_level = [[Tiles.wall for _ in range(levelInit.width)] for _ in range(levelInit.height)]
    local_occupied = [[False for _ in range(levelInit.width)] for _ in range(levelInit.height)]
    local_visible = [[Tiles.void for _ in range(levelInit.width)] for _ in range(levelInit.height)]
    local_memorized = [[Tiles.void for _ in range(levelInit.width)] for _ in range(levelInit.height)]
    carve_room(10, 8, levelInit.height // 2, levelInit.width // 2)
    generate_rooms()
    generate_tunnels()
    generating_doors()
    generate_staircases()
    clean_up()
    # Spawn player in the center room
    center_y = levelInit.height // 2 + 3
    center_x = levelInit.width // 2 + 3
    set_level()
    generate_enemies()
    return center_y, center_x  # (y, x)


def generate_rooms():
    for _ in range(levelInit.roomCount):
        minDistance = 9999
        nearestPlace = None
        room = carve_room()
        if room is None:
            continue
        for y in range(levelInit.height):
            for x in range(levelInit.width):
                if local_level[y][x] == Tiles.floor:
                    if y > room[0] and y < room[2] and x > room[1] and x < room[3]:
                        continue
                    distance = ((y - room[0] + 3) ** 2 + (x - room[1] + 3) ** 2) ** 0.5
                    if distance < minDistance:
                        minDistance = distance
                        nearestPlace = (y, x)
        startPos = (room[0] + room[2]) // 2, (room[1] + room[3]) // 2  # (y, x)
        endPos = nearestPlace
        carve_tunnel(startPos, endPos)


def generate_tunnels():
    for room in local_rooms:
        minDistance = 9999
        roomCenter = [(room[0] + room[2]) // 2, (room[1] + room[3]) // 2]  # (y, x)
        nearestRoom = None
        for other in local_rooms:
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
        roomH = random.randint(levelInit.roomSize[0], levelInit.roomSize[1])
        roomW = random.randint(levelInit.roomSize[0], levelInit.roomSize[1])
        y = random.randint(1, levelInit.height - roomH - 2)
        x = random.randint(1, levelInit.width - roomW - 2)

    for j in range(roomH):
        for i in range(roomW):
            check_y = y + j
            check_x = x + i
            if check_y >= levelInit.height or check_x >= levelInit.width:
                return None
            if local_level[check_y][check_x] != Tiles.wall:
                return None
    for j in range(roomH):
        for i in range(roomW):
            local_level[y + j][x + i] = Tiles.wall

    for j in range(roomH - 2):
        for i in range(roomW - 2):
            local_level[y + j + 1][x + i + 1] = Tiles.floor
    room = [y, x, roomH + y, roomW + x]  # [y1, x1, y2, x2]
    local_rooms.append(room)
    return room


def carve_tunnel(startPos, endPos):
    # startPos and endPos are (y, x)
    if startPos[0] < endPos[0]:
        for y in range(startPos[0], endPos[0] + 1):
            local_level[y][startPos[1]] = Tiles.floor
    else:
        for y in range(endPos[0], startPos[0] + 1):
            local_level[y][startPos[1]] = Tiles.floor
    if startPos[1] < endPos[1]:
        for x in range(startPos[1], endPos[1] + 1):
            local_level[endPos[0]][x] = Tiles.floor
    else:
        for x in range(endPos[1], startPos[1] + 1):
            local_level[endPos[0]][x] = Tiles.floor


def carve_door(y, x):
    if random.random() < levelInit.open_door_chance:
        local_level[y][x] = Tiles.open_door
    elif random.random() < levelInit.trapped_door_chance:
        local_level[y][x] = Tiles.trapped_door
    else:
        local_level[y][x] = Tiles.closed_door


def generating_doors():
    for y in range(1, levelInit.height - 1):
        for x in range(1, levelInit.width - 1):
            if local_level[y][x] == Tiles.floor:
                if ((local_level[y - 1][x] == Tiles.wall and local_level[y + 1][x] == Tiles.wall and
                     local_level[y][x - 1] == Tiles.floor and local_level[y][x + 1] == Tiles.floor) or
                        (local_level[y][x - 1] == Tiles.wall and local_level[y][x + 1] == Tiles.wall and
                         local_level[y - 1][x] == Tiles.floor and local_level[y + 1][x] == Tiles.floor)):
                    if (local_level[y + 1][x + 1] == Tiles.floor or local_level[y + 1][x - 1] == Tiles.floor or
                            local_level[y - 1][x + 1] == Tiles.floor or local_level[y - 1][x - 1] == Tiles.floor):
                        carve_door(y, x)
            if local_level[y][x] == Tiles.wall:
                if ((local_level[y - 1][x] == Tiles.floor and local_level[y + 1][x] == Tiles.floor and
                     local_level[y][x - 1] == Tiles.wall and local_level[y][x + 1] == Tiles.wall) or
                        (local_level[y][x - 1] == Tiles.floor and local_level[y][x + 1] == Tiles.floor and
                         local_level[y - 1][x] == Tiles.wall and local_level[y + 1][x] == Tiles.wall)):
                    if random.random() < levelInit.random_door_chance:
                        carve_door(y, x)
                        if random.random() < levelInit.hidden_door_chance:
                            local_level[y][x] = Tiles.hidden_door
                        else:
                            local_level[y][x] = Tiles.closed_door


def clean_up():
    for y in range(1, levelInit.height - 1):
        for x in range(1, levelInit.width - 1):
            if local_level[y][x] == Tiles.wall:
                if ((local_level[y - 1][x] == Tiles.wall or local_level[y - 1][x] == Tiles.void) and
                        (local_level[y + 1][x] == Tiles.wall or local_level[y + 1][x] == Tiles.void) and
                        (local_level[y][x - 1] == Tiles.wall or local_level[y][x - 1] == Tiles.void) and
                        (local_level[y][x + 1] == Tiles.wall or local_level[y][x + 1] == Tiles.void) and
                        (local_level[y + 1][x + 1] == Tiles.wall or local_level[y + 1][x + 1] == Tiles.void) and
                        (local_level[y + 1][x - 1] == Tiles.wall or local_level[y + 1][x - 1] == Tiles.void) and
                        (local_level[y - 1][x + 1] == Tiles.wall or local_level[y - 1][x + 1] == Tiles.void) and
                        (local_level[y - 1][x - 1] == Tiles.wall or local_level[y - 1][x - 1] == Tiles.void)):
                    local_level[y][x] = Tiles.void

    for y in range(levelInit.height):
        local_level[y][0] = Tiles.void
        local_level[y][levelInit.width - 1] = Tiles.void
    for x in range(levelInit.width):
        local_level[0][x] = Tiles.void
        local_level[levelInit.height - 1][x] = Tiles.void


def generate_enemies():
    for i in range(random.randint(10, 10)):
        enemyManager.generate_enemy("Skeleton")


def generate_staircases():
    for i in range(levelInit.staircase_down_count):
        generate_down_staircase()
    for i in range(levelInit.staircase_up_count):
        generate_up_staircase()


def generate_up_staircase():
    y = random.randint(1, levelInit.height - 1)
    x = random.randint(1, levelInit.width - 1)
    if local_level[y][x] == Tiles.floor:
        local_level[y][x] = Tiles.staircase_up
    else:
        generate_up_staircase()


def generate_down_staircase():
    y = random.randint(1, levelInit.height - 1)
    x = random.randint(1, levelInit.width - 1)
    if local_level[y][x] == Tiles.floor:
        local_level[y][x] = Tiles.staircase_down
    else:
        generate_down_staircase()


def set_level():
    level.current_level.level = local_level
    level.current_level.occupied = local_occupied
    level.current_level.visible = local_visible
    level.current_level.memorized = local_memorized
    level.current_level.rooms = local_rooms
