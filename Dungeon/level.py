width = 200
height = 100

changes = True  # flag to indicate if the level has changed
can_move = True  # flag to indicate if the player can move

view_width = 80
view_height = 40

walkable = ['.', '`']  # walkable tiles
unwalkable = ['#', ' ', '+']  # unwalkable tiles

roomSize = (7, 17)
roomCount = 300

random_door_chance = 0.1
open_door_chance = 0.2

rooms = []  # list of rooms
level = []  # list of all tiles

memorized = [] # list of memorized tiles
visible = []  # list of visible tiles
