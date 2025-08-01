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
