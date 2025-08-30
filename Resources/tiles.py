class Tiles:
    floor = "."
    wall = "#"
    void = " "

    open_door = "'"
    closed_door = "+"
    trapped_door = "t+"

    hidden_door = wall

    walkable = [floor, open_door]  # walkable tiles
    unwalkable = [wall, void, hidden_door]  # unwalkable tiles

    doors = [closed_door, trapped_door]
    unwalkable += doors

    @staticmethod
    def is_walkable(tile):
        return tile in Tiles.walkable

    @staticmethod
    def is_unwalkable(tile):
        return tile in Tiles.unwalkable

    @staticmethod
    def is_door(tile):
        return tile in Tiles.doors
