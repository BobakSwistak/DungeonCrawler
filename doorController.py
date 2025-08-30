from Dungeon import level
from Resources.tiles import Tiles


class DoorController:

    @staticmethod
    def open_door(pos):
        y, x = pos
        door = level.current_level.level[y][x]

        if door == Tiles.closed_door:
            level.current_level.level[y][x] = Tiles.open_door
            return 0
        elif door == Tiles.trapped_door:
            level.current_level.level[y][x] = Tiles.open_door
            return 2, 5

    @staticmethod
    def close_door(pos):
        y, x = pos
        door = level.current_level.level[y][x]
        if door == Tiles.open_door and not level.current_level.occupied[y][x]:
            level.current_level.level[y][x] = Tiles.closed_door
            # menuRenderer.debug_log("Door closed")
