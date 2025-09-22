import random
import Enemies.enemyManager as enemyManager

from Dungeon import level, levelInit
from Resources.tiles import Tiles


class LevelGenerator:

    def __init__(self):
        self.local_level = []
        self.local_occupied = []
        self.local_visible = []
        self.local_memorized = []
        self.local_rooms = []

    def generate_dungeon(self):
        # Initialize level and visible arrays as [x][y]
        self.local_level = [[Tiles.wall for _ in range(levelInit.width)] for _ in range(levelInit.height)]
        self.local_occupied = [[False for _ in range(levelInit.width)] for _ in range(levelInit.height)]
        self.local_visible = [[Tiles.void for _ in range(levelInit.width)] for _ in range(levelInit.height)]
        self.local_memorized = [[Tiles.void for _ in range(levelInit.width)] for _ in range(levelInit.height)]
        self.carve_room()

        self.generate_rooms()
        self.generate_tunnels()
        self.generating_doors()
        self.generate_staircases()
        self.clean_up()
        # Spawn player in the center room
        center_x = levelInit.height // 2 + 3
        center_y = levelInit.width // 2 + 3
        self.export_level()
        self.generate_enemies()
        starter_room = random.choice(self.local_rooms)
        return (starter_room[0] + starter_room[2]) // 2, (starter_room[1] + starter_room[3]) // 2  # (x, y)

    def generate_rooms(self):
        for _ in range(levelInit.roomCount):
            minDistance = 9999
            nearestPlace = None
            room = self.carve_room()
            if room is None:
                continue
            for x in range(levelInit.height):
                for y in range(levelInit.width):
                    if self.local_level[x][y] == Tiles.floor:
                        if room[2] > x > room[0] and room[3] > y > room[1]:
                            continue
                        distance = ((x - room[0] + 3) ** 2 + (y - room[1] + 3) ** 2) ** 0.5
                        if distance < minDistance:
                            minDistance = distance
                            nearestPlace = (x, y)
            startPos = (room[0] + room[2]) // 2, (room[1] + room[3]) // 2  # (x, y)
            endPos = nearestPlace
            self.carve_tunnel(startPos, endPos)

    def generate_tunnels(self):
        for room in self.local_rooms:
            minDistance = 9999
            roomCenter = [(room[0] + room[2]) // 2, (room[1] + room[3]) // 2]  # (x, y)
            nearestRoom = None
            for other in self.local_rooms:
                if room != other:
                    otherCenter = [(other[0] + other[2]) // 2, (other[1] + other[3]) // 2]
                    distance = ((otherCenter[0] - roomCenter[0]) ** 2 + (otherCenter[1] - roomCenter[1]) ** 2) ** 0.5
                    if distance < minDistance:
                        minDistance = distance
                        nearestRoom = otherCenter
            if nearestRoom:
                self.carve_tunnel(roomCenter, nearestRoom)

    def carve_room(self, roomH=None, roomW=None, x=None, y=None):
        if roomH is None:
            roomH = random.randint(levelInit.roomSize[0], levelInit.roomSize[1])
            roomW = random.randint(levelInit.roomSize[0], levelInit.roomSize[1])
            x = random.randint(1, levelInit.height - roomH - 2)
            y = random.randint(1, levelInit.width - roomW - 2)

        for j in range(roomH):
            for i in range(roomW):
                check_x = x + j
                check_y = y + i
                if check_x >= levelInit.height or check_y >= levelInit.width:
                    return None
                if self.local_level[check_x][check_y] != Tiles.wall:
                    return None
        for j in range(roomH):
            for i in range(roomW):
                self.local_level[x + j][y + i] = Tiles.wall

        for j in range(roomH - 2):
            for i in range(roomW - 2):
                self.local_level[x + j + 1][y + i + 1] = Tiles.floor
        room = [x, y, roomH + x, roomW + y]  # [y1, x1, y2, x2]
        self.local_rooms.append(room)
        return room

    def carve_tunnel(self, startPos, endPos):
        # startPos and endPos are (x, y)
        if startPos[0] < endPos[0]:
            for x in range(startPos[0], endPos[0] + 1):
                self.local_level[x][startPos[1]] = Tiles.floor
        else:
            for x in range(endPos[0], startPos[0] + 1):
                self.local_level[x][startPos[1]] = Tiles.floor
        if startPos[1] < endPos[1]:
            for y in range(startPos[1], endPos[1] + 1):
                self.local_level[endPos[0]][y] = Tiles.floor
        else:
            for y in range(endPos[1], startPos[1] + 1):
                self.local_level[endPos[0]][y] = Tiles.floor

    def carve_door(self, x, y):
        if random.random() < levelInit.open_door_chance:
            self.local_level[x][y] = Tiles.open_door
        elif random.random() < levelInit.trapped_door_chance:
            self.local_level[x][y] = Tiles.trapped_door
        else:
            self.local_level[x][y] = Tiles.closed_door

    def generating_doors(self):
        for x in range(1, levelInit.height - 1):
            for y in range(1, levelInit.width - 1):
                if self.local_level[x][y] == Tiles.floor:
                    if ((self.local_level[x - 1][y] == Tiles.wall and self.local_level[x + 1][y] == Tiles.wall and
                         self.local_level[x][y - 1] == Tiles.floor and self.local_level[x][y + 1] == Tiles.floor) or
                            (self.local_level[x][y - 1] == Tiles.wall and self.local_level[x][y + 1] == Tiles.wall and
                             self.local_level[x - 1][y] == Tiles.floor and self.local_level[x + 1][y] == Tiles.floor)):
                        if (self.local_level[x + 1][y + 1] == Tiles.floor or self.local_level[x + 1][
                            y - 1] == Tiles.floor or
                                self.local_level[x - 1][y + 1] == Tiles.floor or self.local_level[x - 1][
                                    y - 1] == Tiles.floor):
                            self.carve_door(x, y)
                if self.local_level[x][y] == Tiles.wall:
                    if ((self.local_level[x - 1][y] == Tiles.floor and self.local_level[x + 1][y] == Tiles.floor and
                         self.local_level[x][y - 1] == Tiles.wall and self.local_level[x][y + 1] == Tiles.wall) or
                            (self.local_level[x][y - 1] == Tiles.floor and self.local_level[x][y + 1] == Tiles.floor and
                             self.local_level[x - 1][y] == Tiles.wall and self.local_level[x + 1][y] == Tiles.wall)):
                        if random.random() < levelInit.random_door_chance:
                            self.carve_door(x, y)
                            if random.random() < levelInit.hidden_door_chance:
                                self.local_level[x][y] = Tiles.hidden_door
                            else:
                                self.local_level[x][y] = Tiles.closed_door

    def clean_up(self):
        for x in range(1, levelInit.height - 1):
            for y in range(1, levelInit.width - 1):
                if all(self.local_level[yy][xx] in [Tiles.wall, Tiles.void] for yy in range(x - 1, x + 2) for xx in
                       range(y - 1, y + 2)): self.local_level[x][y] = Tiles.void

        for x in range(levelInit.height):
            self.local_level[x][0] = Tiles.void
            self.local_level[x][levelInit.width - 1] = Tiles.void
        for y in range(levelInit.width):
            self.local_level[0][y] = Tiles.void
            self.local_level[levelInit.height - 1][y] = Tiles.void

    def generate_enemies(self):
        for i in range(random.randint(10, 10)):
            enemyManager.generate_enemy("Skeleton")

    def generate_staircases(self):
        for i in range(levelInit.staircase_down_count):
            self.generate_down_staircase()
        for i in range(levelInit.staircase_up_count):
            self.generate_up_staircase()

    def generate_up_staircase(self):
        x = random.randint(1, levelInit.height - 1)
        y = random.randint(1, levelInit.width - 1)
        if self.local_level[x][y] == Tiles.floor:
            self.local_level[x][y] = Tiles.staircase_up
        else:
            self.generate_up_staircase()

    def generate_down_staircase(self):
        x = random.randint(1, levelInit.height - 1)
        y = random.randint(1, levelInit.width - 1)
        if self.local_level[x][y] == Tiles.floor:
            self.local_level[x][y] = Tiles.staircase_down
        else:
            self.generate_down_staircase()

    def export_level(self):
        level.current_level.level = self.local_level
        level.current_level.occupied = self.local_occupied
        level.current_level.visible = self.local_visible
        level.current_level.memorized = self.local_memorized
        level.current_level.rooms = self.local_rooms


levelGenerator = LevelGenerator()
