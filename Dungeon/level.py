from Dungeon import levelGenerator


class Level:
    def __init__(self):
        self.changes = False

        self.player_y, self.player_x = 0, 0

        self.enemies_list = []

        self.step_counter = 0  # counter for steps taken by the player

        self.rooms = []  # list of rooms
        self.level = []  # list of all tiles

        self.occupied = []  # list of occupied tiles

        self.memorized = []  # list of memorized tiles
        self.visible = []  # list of visible tiles


levels = []
levels.append(Level())
current_level = levels[0]
current_level.player_y, current_level.player_x = levelGenerator.generate_dungeon(0)
