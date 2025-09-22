import random

from Enemies import enemies
from Dungeon import level, levelInit
from Resources.tiles import Tiles
from Renderers import menuRenderer
from Player import player
from Resources import colors


def generate_enemy(enemy_name):
    while True:
        random_x = random.randint(0, levelInit.height - 1)
        random_y = random.randint(0, levelInit.width - 1)
        if Tiles.is_walkable(level.current_level.level[random_x][random_y]) and not \
                level.current_level.occupied[random_x][random_y]:
            enemy_class = getattr(enemies, enemy_name)  # Retrieve the class dynamically
            enemy_instance = enemy_class()  # Instantiate the enemy
            enemy_instance.enemy_pos = [random_x, random_y]
            level.current_level.enemies_list.append(enemy_instance)
            level.current_level.occupied[random_x][random_y] = True
            break


def enemy_update():
    if level.current_level.enemies_list:
        for enemy in level.current_level.enemies_list:
            if enemy.hp < 0:
                level.current_level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                level.current_level.enemies_list.remove(enemy)
                if enemy.is_visible:
                    menuRenderer.debug_log(f"{enemy.name} died.", color=colors.ORANGE)
                elif abs(level.current_level.player_x - enemy.enemy_pos[0]) + abs(
                        level.current_level.player_y - enemy.enemy_pos[1]) >= 10:
                    menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)
                continue
            enemy.controller()
