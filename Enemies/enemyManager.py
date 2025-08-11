from Enemies import enemies
from Dungeon import level
import random


def generate_enemy(enemy_name):
    while True:
        random_y = random.randint(0, level.height - 1)
        random_x = random.randint(0, level.width - 1)
        if level.level[random_y][random_x] in level.walkable and not level.occupied[random_y][random_x]:
            enemy_instance = enemies.Skeleton()  # Replace with dynamic enemy creation if needed
            enemy_instance.enemy_pos = [random_y, random_x]
            enemies.enemies_list.append(enemy_instance)
            level.occupied[random_y][random_x] = True
            break