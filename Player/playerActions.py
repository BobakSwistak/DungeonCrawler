import random

from Dungeon import level, levelManager
from Player import player, playerHp
from Renderers import menuRenderer
from Resources import texts


def open_door(new_y, new_x):
    door = level.level[new_y][new_x]
    if door == "+":
        level.level[new_y][new_x] = "`"  # Open the door
        menuRenderer.debug_log("Door opened")

    elif door == "t+":
        playerHp.damage_player(2, 5)
        level.level[new_y][new_x] = "`"  # Open the door
        menuRenderer.debug_log("Door was trapped")


def close_door(new_y, new_x):
    door = level.level[new_y][new_x]
    if door == "`":
        level.level[new_y][new_x] = "+"
        menuRenderer.debug_log("Door closed")


def inspect_tile(new_y, new_x):
    tile = level.level[new_y][new_x]
    if tile == "h+":
        level.level[new_y][new_x] = "+"
        menuRenderer.debug_log("you found something")
    else:
        menuRenderer.debug_log("there is nothing unusual to see here")


def passive_inspect(new_y, new_x):
    for i in range(new_y - 1, new_y + 1):
        for j in range(new_x - 1, new_x + 1):
            if 0 <= i < level.height and 0 <= j < level.width:
                tile = level.level[i][j]
                if tile == "h+" and random.random() < player.passive_inspect_chance:
                    level.level[i][j] = "+"
                    menuRenderer.debug_log("you noticed something")
