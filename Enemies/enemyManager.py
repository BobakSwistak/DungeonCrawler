from Enemies import enemies, enemyController
from Dungeon import level


def generate_enemy(enemy_name):
    center_y = level.height // 2 + 1
    center_x = level.width // 2 + 1
    skeleton_instance = enemies.Skeleton()  # Create an instance of Skeleton
    enemies.enemies_list.append(skeleton_instance)  # Add the instance to the list
    skeleton_instance.controller()  # Call the controller method on the instance
