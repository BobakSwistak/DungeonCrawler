import random

from Resources.tiles import Tiles
from doorController import DoorController
from Dungeon import level, levelInit
from Player import player, playerHp
from Renderers import menuRenderer
from Resources import colors
from Enemies import enemies


def action(new_y, new_x):
    if level.current_level.level[new_y][new_x] == Tiles.open_door:
        DoorController.close_door((new_y, new_x))
    elif Tiles.is_door(level.current_level.level[new_y][new_x]):
        door = DoorController.open_door((new_y, new_x))
        if isinstance(door, tuple):
            playerHp.damage_player(door[0], door[1])
            menuRenderer.debug_log("the door was trapped!", color=colors.ORANGE)
    player.action = False
    player.can_move = True


def inspect_tile(new_y, new_x):
    tile = level.current_level.level[new_y][new_x]
    if tile == Tiles.hidden_door:
        level.current_level.level[new_y][new_x] = Tiles.closed_door
        menuRenderer.debug_log("you found something")
    else:
        menuRenderer.debug_log("there is nothing unusual to see here")


def attack(enemy):
    enemy.damage_enemy(random.randint(2, 5))

    if enemy.hp <= 0:
        for i in enemies.enemies_list:
            if i == enemy:
                enemies.enemies_list.remove(i)
                level.current_level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                menuRenderer.debug_log(f"You killed {enemy.name}.", color=colors.ORANGE)
                break


def passive_inspect(new_y, new_x):
    for i in range(new_y - 1, new_y + 1):
        for j in range(new_x - 1, new_x + 1):
            if 0 <= i < levelInit.height and 0 <= j < levelInit.width:
                tile = level.current_level.level[i][j]
                if tile == "h+" and random.random() < player.passive_inspect_chance:
                    level.current_level.level[i][j] = Tiles.closed_door
                    menuRenderer.debug_log("you noticed something")
