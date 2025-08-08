from Dungeon import level, levelManager
from Player import player
from Renderers import menuRenderer
from Enemies.aStarAlgoritm import AStarAlgorithm
import random


class EnemyController:
    def __init__(self):
        self.name = "Enemy"
        self.enemy_symbol = 'M'  # Symbol for the enemy
        self.color = 1  # Color code for rendering
        self.speed = 1
        self.hp = 1
        self.perception = 1

        self.astar_algorithm = AStarAlgorithm()

        self.enemy_pos = None
        self.target_pos = None
        self.path = []
        self.agro = False

        self.enemyPosition()
        self.find_target_pos()
        self.create_path()

    def controller(self):
        if not self.agro:
            self.field_of_view = levelManager.calculate_field_of_view(self.enemy_pos[0], self.enemy_pos[1],
                                                                      10 + self.perception)
            if self.enemy_pos == self.target_pos:
                self.find_target_pos()
                self.create_path()
        else:
            self.target_pos = [player.player_y, player.player_x]
            self.create_path()

        if [player.player_y, player.player_x] in self.field_of_view:
            self.agro = True
            self.target_pos = [player.player_y, player.player_x]
            self.create_path()
        else:
            self.agro = False
        self.move()

    def move(self):
        if self.path and self.enemy_pos != self.target_pos:
            level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = False
            self.enemy_pos = self.path.pop(0)
            menuRenderer.debug_log(f"Enemy moved to position: {self.enemy_pos}")
            level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = True
        else:
            self.target_pos = [player.player_y, player.player_x]
            self.create_path()

    def open_door(self, door_pos):
        door = level.level[door_pos[0]][door_pos[1]]
        menuRenderer.debug_log("door")
        if door == "+":
            level.level[door_pos[0]][door_pos[1]] = "`"  # Open the door
            menuRenderer.debug_log("Door opened")

        elif door == "t+":
            self.hp -= random.randint(2, 5)
            level.level[door_pos[0]][door_pos[1]] = "`"  # Open the door
            menuRenderer.debug_log("Door was trapped")

    def enemyPosition(self):
        while True:
            self.enemy_pos = [random.randint(0, level.height - 1), random.randint(0, level.width - 1)]
            if level.level[self.enemy_pos[0]][self.enemy_pos[1]] in level.walkable:
                break

    def find_target_pos(self):
        self.room = random.choice(level.rooms)
        self.y = random.randint(self.room[0] + 2, self.room[2] - 2)
        self.x = random.randint(self.room[1] + 2, self.room[3] - 2)
        self.target_pos = [self.y, self.x]
        self.create_path()
        print(self.enemy_pos)

    def create_path(self):
        start = tuple(self.enemy_pos)
        goal = tuple(self.target_pos)
        self.path = self.astar_algorithm.astar(start, goal)
#
# # levelGenerator.generate_dungeon()
#
# enemy_manager = EnemyController()
# enemy_manager.controller()
#
# for i in enemy_manager.path:
#     level.level[i[0]][i[1]] = 'E'  # Mark path with 'E'

