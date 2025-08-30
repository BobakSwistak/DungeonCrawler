from Enemies import enemies
from Dungeon import level, levelInit
from Resources.tiles import Tiles
from Renderers import menuRenderer
from Player import player
from Resources import colors
import random


def generate_enemy(enemy_name):
    while True:
        random_y = random.randint(0, levelInit.height - 1)
        random_x = random.randint(0, levelInit.width - 1)
        if Tiles.is_walkable(level.current_level.level[random_y][random_x]) and not level.current_level.occupied[random_y][random_x]:
            enemy_class = getattr(enemies, enemy_name)  # Retrieve the class dynamically
            enemy_instance = enemy_class()  # Instantiate the enemy
            enemy_instance.enemy_pos = [random_y, random_x]
            enemies.enemies_list.append(enemy_instance)
            level.current_level.occupied[random_y][random_x] = True
            break

def enemy_update():
    if enemies.enemies_list:
        for enemy in enemies.enemies_list:
            if enemy.hp < 0:
                level.current_level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                enemies.enemies_list.remove(enemy)
                if enemy.is_visible:
                    menuRenderer.debug_log(f"{enemy.name} died.", color=colors.ORANGE)
                elif abs(player.player_y - enemy.enemy_pos[0]) + abs(
                        player.player_x - enemy.enemy_pos[1]) >= 10:
                    menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)
                continue
            enemy.controller()