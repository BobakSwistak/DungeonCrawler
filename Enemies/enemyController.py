import random

from Dungeon import level, levelManager, levelInit
from Player import player, playerHp
from Renderers import menuRenderer
from Enemies.aStarAlgoritm import AStarAlgorithm
from Resources import colors
from doorController import DoorController
from Dungeon.tiles import Tiles


# todo add ability to sleep.

class EnemyController:
    def __init__(self):
        self.name = "Enemy"
        self.enemy_symbol = 'M'  # Symbol for the enemy
        self.color = colors.ORANGE  # Color code for rendering
        self.speed = 1
        self.hp = 10
        self.hp_max = 10
        self.perception = -10
        self.morale = 2  # Morale of the enemy
        self.max_morale = 2  # Maximum morale of the enemy
        self.last_damage_time = 0  # Time when the enemy last took damage

        self.attack_dmg = [2, 5]
        self.heavy_dmg = [5, 10]
        self.ranged_dmg = [5, 10]

        self.heavy = False
        self.ranged = False

        self.is_visible = False

        self.astar_algorithm = AStarAlgorithm()

        self.move_counter = 0

        self.enemy_pos = None
        self.target_pos = [53, 103]
        self.field_of_view = None

        self.path = []

        self.agro = False

        self.escaping_counter = 0

        self.enemy_position()
        # self.find_target_pos()
        self.create_path()

    def controller(self):
        self.field_of_view = levelManager.calculate_field_of_view(self.enemy_pos[0], self.enemy_pos[1],
                                                                  10 + self.perception)
        self.heal()
        if self.escaping_counter > 0:
            self.escaping_counter -= 1

        if self.morale <= 0:
            if not self.field_of_view[player.player_y][player.player_x]:
                self.agro = False
            else:
                self.escaping_counter = 20
                self.agro = False
                self.path.clear()
        if self.escaping_counter <= 0:
            if self.agro:
                self.target_pos = [player.player_y, player.player_x]
                self.path = levelManager.bresenham_line(self.enemy_pos[0], self.enemy_pos[1], player.player_y,
                                                        player.player_x)
                if len(self.path) <= 2:
                    self.attack()
                    return

            if self.enemy_pos == self.target_pos or not self.path:
                self.find_target_pos()
                self.create_path()
            self.agro = False
            if self.field_of_view[player.player_y][player.player_x]:
                self.agro = True
                self.target_pos = [player.player_y, player.player_x]
                self.create_path()
                self.path.pop(0)
        self.move_counter += self.speed
        while self.move_counter >= 1:
            self.move()
            self.move_counter -= 1

    def move(self):
        level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = False
        if self.escaping_counter <= 0:
            if self.path and self.enemy_pos != self.target_pos:
                next_y, next_x = self.path[0]
                # Check if the next tile is walkable and not occupied
                if (Tiles.is_walkable(level.current_level.level[next_y][next_x]) or
                    Tiles.is_door(level.current_level.level[next_y][next_x])) and not \
                        level.current_level.occupied[next_y][next_x]:
                    level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = False
                    if Tiles.is_door(level.current_level.level[next_y][next_x]):
                        door = DoorController.open_door((next_y, next_x))
                        if isinstance(door, tuple): self.hp -= random.randint(door[0], door[1])
                    else:
                        self.enemy_pos = self.path.pop(0)
                    level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = True
                else:
                    # Recalculate path if blocked or not walkable
                    self.move_to_the_furthest_tile()
                    self.find_target_pos()
                    self.create_path()
            else:
                # If the enemy is not moving towards the target, find a new target position
                self.target_pos = [player.player_y, player.player_x]
                self.create_path()
                level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = True
        elif self.escaping_counter > 0:
            # If the enemy is escaping, find the furthest tile from the player
            level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = False
            self.move_to_the_furthest_tile()

            # If no valid escape tile, stay in place
        level.current_level.occupied[self.enemy_pos[0]][self.enemy_pos[1]] = True

    def move_to_the_furthest_tile(self):
        max_tiles = 3
        for i in range(3):
            escape_roots = self.furthest_tiles(self.enemy_pos, [player.player_y, player.player_x], max_tiles)
            max_tiles += 2
            valid_tiles = [pos for pos in escape_roots
                           if pos != tuple(self.enemy_pos)
                           and not level.current_level.occupied[pos[0]][pos[1]]
                           and (Tiles.is_walkable(level.current_level.level[pos[0]][pos[1]]) or
                                Tiles.is_door(level.current_level.level[pos[0]][
                                    pos[1]]))]
            if valid_tiles:

                pos = random.choice(valid_tiles)
                if Tiles.is_door(level.current_level.level[pos[0]][pos[1]]):
                    door = DoorController.open_door(pos)
                    if isinstance(door, tuple):
                        self.hp -= random.randint(door[0], door[1])
                else:
                    self.enemy_pos = list(pos)
                break
            else:
                if i == 2:
                    # If no valid escape tile found after 3 attempts, stay in place
                    if len(levelManager.bresenham_line(self.enemy_pos[0], self.enemy_pos[1], player.player_y,
                                                       player.player_x)) <= 2:
                        # The enemy is close to the player, so it will not escape
                        self.attack()

    def attack(self):
        if len(levelManager.bresenham_line(self.enemy_pos[0], self.enemy_pos[1], player.player_y,
                                           player.player_x)) <= 2:
            playerHp.damage_player(self.attack_dmg[0], self.attack_dmg[1])

    def heal(self):
        self.last_damage_time -= 1
        if self.last_damage_time <= 0:
            self.last_damage_time = random.randint(10, 30)
            self.hp += 1  # Regenerate health over time
            self.morale += 1  # Regenerate morale over time
            if self.hp > self.hp_max:
                self.hp = self.hp_max
            if self.morale > self.max_morale:
                self.morale = self.max_morale

    def enemy_position(self):
        while True:
            self.enemy_pos = [random.randint(0, levelInit.height - 1), random.randint(0, levelInit.width - 1)]
            if Tiles.is_walkable(level.current_level.level[self.enemy_pos[0]][self.enemy_pos[1]]):
                break

    def find_target_pos(self):
        room = random.choice(level.current_level.rooms)
        y = random.randint(room[0] + 1, room[2] - 1)
        x = random.randint(room[1] + 1, room[3] - 1)
        self.target_pos = [y, x]
        self.create_path()

    def create_path(self):
        start = tuple(self.enemy_pos)
        goal = tuple(self.target_pos)
        self.path = self.astar_algorithm.astar(start, goal)

    def furthest_tiles(self, enemy_pos, player_pos, max_tiles=3):
        y, x = enemy_pos
        neighbors = [(y + dy, x + dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if not (dy == 0 and dx == 0)]
        neighbors.sort(key=lambda tile: abs(tile[0] - player_pos[0]) + abs(tile[1] - player_pos[1]), reverse=True)
        return neighbors[:max_tiles]
