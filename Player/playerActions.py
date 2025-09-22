import random

from Resources.tiles import Tiles
from doorController import DoorController
from Dungeon import level, levelInit
from Player import player, playerHp
from Renderers import menuRenderer
from Resources import colors
from Enemies import enemies


def action(new_x, new_y):
    if level.current_level.level[new_x][new_y] == Tiles.open_door:
        DoorController.close_door((new_x, new_y))
    elif Tiles.is_door(level.current_level.level[new_x][new_y]):
        door = DoorController.open_door((new_x, new_y))
        if isinstance(door, tuple):
            playerHp.damage_player(door[0], door[1])
            menuRenderer.debug_log("the door was trapped!", color=colors.ORANGE)
    player.action = False
    player.can_move = True


def inspect_tile(new_x, new_y):
    tile = level.current_level.level[new_x][new_y]
    if tile == Tiles.hidden_door:
        level.current_level.level[new_x][new_y] = Tiles.closed_door
        menuRenderer.debug_log("you found something")
    else:
        menuRenderer.debug_log("there is nothing unusual to see here")


def attack(enemy):
    enemy.damage_enemy(random.randint(2, 5))

    if enemy.hp <= 0:
        for i in level.current_level.enemies_list:
            if i == enemy:
                level.current_level.enemies_list.remove(i)
                level.current_level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                menuRenderer.debug_log(f"You killed {enemy.name}.", color=colors.ORANGE)
                break


def passive_inspect(new_x, new_y):
    for i in range(new_x - 1, new_x + 1):
        for j in range(new_y - 1, new_y + 1):
            if 0 <= i < levelInit.height and 0 <= j < levelInit.width:
                tile = level.current_level.level[i][j]
                if tile == "h+" and random.random() < player.passive_inspect_chance:
                    level.current_level.level[i][j] = Tiles.closed_door
                    menuRenderer.debug_log("you noticed something")
