import random

from Dungeon import level


class DoorController:

    @staticmethod
    def open_door(pos):
        y, x = pos
        door = level.current_level.level[y][x]

        if door == "+":
            level.current_level.level[y][x] = "`"
            return 0
        elif door == "t+":
            level.current_level.level[y][x] = "`"
            return 2, 5

    @staticmethod
    def close_door(pos):
        y, x = pos
        door = level.current_level.level[y][x]
        if door == "`" and not level.current_level.occupied[y][x]:
            level.current_level.level[y][x] = "+"
            # menuRenderer.debug_log("Door closed")