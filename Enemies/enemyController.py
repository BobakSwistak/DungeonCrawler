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
        self.perception = 99

        self.astar_algorithm = AStarAlgorithm()

        self.enemy_pos = None
        self.target_pos = [52, 102]
        self.path = []
        self.agro = False

        self.enemyPosition()
        # self.find_target_pos()
        self.create_path()

    def controller(self):
        self.field_of_view = levelManager.calculate_field_of_view(self.enemy_pos[0], self.enemy_pos[1],
                                                                  10 + self.perception)
        if not self.agro:

            if self.enemy_pos == self.target_pos:
                self.find_target_pos()
                self.create_path()
        else:
            self.target_pos = [player.player_y, player.player_x]
            self.path = levelManager.bresenham_line(self.enemy_pos[0], self.enemy_pos[1], player.player_y,
                                                    player.player_x)

        if self.field_of_view[player.player_y][player.player_x]:
            self.agro = True
            self.path = levelManager.bresenham_line(self.enemy_pos[0], self.enemy_pos[1], player.player_y,
                                                    player.player_x)
            self.path.pop(0)
        else:
            self.agro = False
        self.move()

    def move(self):
        if self.path and self.enemy_pos != self.target_pos:
            level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = False
            if level.level[self.path[0][0]][self.path[0][1]] in level.doors:
                self.open_door(self.path[0])
            elif level.occupied[self.path[0][0]][self.path[0][1]] == False:
                self.enemy_pos = self.path.pop(0)
            menuRenderer.debug_log(f"Enemy moved to position: {self.enemy_pos}")
            level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = True
        else:
            self.target_pos = [player.player_y, player.player_x]
            self.create_path()
            self.move()

    def open_door(self, door_pos):
        door = level.level[door_pos[0]][door_pos[1]]
        menuRenderer.debug_log("door")
        if door == "+":
            level.level[door_pos[0]][door_pos[1]] = "`"  # Open the door

        elif door == "t+":
            self.hp -= random.randint(2, 5)
            level.level[door_pos[0]][door_pos[1]] = "`"  # Open the door

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
