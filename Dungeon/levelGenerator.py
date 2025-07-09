import random

import Dungeon.level as level
import random


def generate_level():
    level.level = [["." for _ in range(level.width)] for _ in range(level.height)]

    for i in range(random.randint(level.roomCount[0], level.roomCount[1])):
        generate_room()

    return level.level


def generate_room():
    roomW = random.randint(level.roomSize[0], level.roomSize[1])
    roomH = random.randint(level.roomSize[0], level.roomSize[1])
    x = random.randint(0, level.width - roomW)
    y = random.randint(0, level.height - roomH)

    for i in range(roomH):
        for j in range(roomW):
            if level.level[y + i][x + j] != '.':
                return  # Abort if overlap

    for i in range(roomH):
        for j in range(roomW):
            level.level[y + i][x + j] = '#'
    # Create empy space inside the room
    for i in range(roomH-2):
        for j in range(roomW-2):
            level.level[y + i + 1][x + j + 1] = '.'

