from Dungeon import level
from Resources.tiles import Tiles


class DoorController:

    @staticmethod
    def open_door(pos):
        x, y = pos
        door = level.current_level.level[x][y]

        if door == Tiles.closed_door:
            level.current_level.level[x][y] = Tiles.open_door
            return 0
        elif door == Tiles.trapped_door:
            level.current_level.level[x][y] = Tiles.open_door
            return 2, 5

    @staticmethod
    def close_door(pos):
        x, y = pos
        door = level.current_level.level[x][y]
        if door == Tiles.open_door and not level.current_level.occupied[x][y]:
            level.current_level.level[x][y] = Tiles.closed_door
            # menuRenderer.debug_log("Door closed")
