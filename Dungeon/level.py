class Level:
    def __init__(self):
        self.changes = False

        self.step_counter = 0  # counter for steps taken by the player

        self.rooms = []  # list of rooms
        self.level = []  # list of all tiles

        self.occupied = []  # list of occupied tiles

        self.memorized = []  # list of memorized tiles
        self.visible = []  # list of visible tiles

levels = []
current_level = Level()