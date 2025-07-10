import random
import Dungeon.level as level


# błąd by bo kiedy on chce zrobić korytarz ma dwie przeszkody
#
# 1. próbóje znaleść ścianę ale klatka z której zaczyta to już ściana
# 2. gdy tworzy pokój to jest próba czy te pola są już zajęte
# pracuj pracuj


def generate_level():
    level.level = [["." for _ in range(level.width)] for _ in range(level.height)]
    # generate_room(10, 10, 1, 1)
    # generate_room(10, 10, 20, 1)
    # generate_corridor_horizontal(4, 10, right=True)
    for i in range(random.randint(level.roomCount[0], level.roomCount[1])):
        generate_room()
    for i in range(1000):
        generate_corridors()
    return level.level


def generate_room(roomW=None, roomH=None, x=None, y=None, force=False):
    if roomW == None:
        roomW = random.randint(level.roomSize[0], level.roomSize[1])
        roomH = random.randint(level.roomSize[0], level.roomSize[1])
        x = random.randint(1, level.width - roomW - 1)
        y = random.randint(1, level.height - roomH - 1)

    for i in range(roomH):
        for j in range(roomW):
            if level.level[y + i][x + j] != '.' and force == False:
                print('room already exists')
                return
    level.rooms.append((x, y, x + roomW, y + roomH))
    for i in range(roomH):
        for j in range(roomW):
            level.level[y + i][x + j] = '#'
    print('generating...')

    for i in range(roomH - 2):
        for j in range(roomW - 2):
            level.level[y + i + 1][x + j + 1] = '.'
    print('room generated')


def generate_corridors():
    for i in range(1, level.height - 1):
        for j in range(1, level.width - 1):
            if level.level[i][j] == '#':
                for room in level.rooms:
                    if room[1] <= i < room[3] and room[0] <= j < room[2] and random.random() < 0.5:
                        # Check vertical corridor possibility
                        if level.level[i + 1][j] == '#' and level.level[i - 1][j] == '#':
                            center_x = (room[0] + room[2]) // 2
                            generate_corridor_horizontal(i, j, right=(j > center_x))
                        # Check horizontal corridor possibility
                        if level.level[i][j + 1] != '.' and level.level[i][j - 1] != '.':
                            center_y = (room[1] + room[3]) // 2
                            generate_corridor_vertical(i, j, up=(i > center_y))
                        break
                break


def generate_corridor_vertical(i, j, up=True, first=True):
    print('coridor begin')
    level.level[i][j] = '+'
    for k in range(random.randint(level.corridorLength[0], level.corridorLength[1])):
        if i + k >= level.height - 1 or i + k < 0:
            print('coridor out of bounds')
            return
        if level.level[i + k][j] == '#':
            print('coridor found')
            print(k)
            generate_room(roomW=3, roomH=k + 1 if up else -k - 1, x=j - 1, y=i, force=True)
            level.level[i + k][j] = '+'
            level.level[i][j] = '+'
            return
    print('coridor not found')


def generate_corridor_horizontal(i, j, right=True, first=True):
    print('coridor begin')
    # level.level[i][j] = '+'
    for k in range(random.randint(level.corridorLength[0], level.corridorLength[1])):
        if j + k >= level.width - 1 or j + k < 0:
            print('coridor out of bounds')
            return
        if level.level[i][j + k] == '#' and k != 0:
            print('coridor found')
            print(k)
            generate_room(roomW=k + 1 if right else -k - 1, roomH=3, x=j, y=i - 1, force=True)
            level.level[i][j + k] = '+'
            level.level[i][j] = '+'
            return
    print('coridor not found')
