width = 200
height = 100

changes = False  # flag to indicate if the level has changed
fog_of_war = False

step_counter = 0  # counter for steps taken by the player

view_width = 80
view_height = 40

walkable = ['.', '`']  # walkable tiles
unwalkable = ['#', ' ', 'h+']  # unwalkable tiles

doors = ['+', 't+']

roomSize = (7, 17)
roomCount = 300

random_door_chance = 0.3
open_door_chance = 0.2
trapped_door_chance = 0.1
hidden_door_chance = 0.2

rooms = []  # list of rooms
level = []  # list of all tiles

occupied = [] # list of occupied tiles

memorized = []  # list of memorized tiles
visible = []  # list of visible tiles
