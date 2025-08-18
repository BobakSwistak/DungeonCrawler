from Enemies import enemies
from Dungeon import level
import random


def generate_enemy(enemy_name):
    while True:
        random_y = random.randint(0, level.height - 1)
        random_x = random.randint(0, level.width - 1)
        if level.level[random_y][random_x] in level.walkable and not level.occupied[random_y][random_x]:
            enemy_class = getattr(enemies, enemy_name)  # Retrieve the class dynamically
            enemy_instance = enemy_class()  # Instantiate the enemy
            enemy_instance.enemy_pos = [random_y, random_x]
            enemies.enemies_list.append(enemy_instance)
            level.occupied[random_y][random_x] = True
            break
