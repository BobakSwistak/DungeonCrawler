import random
from doorController import DoorController
from Dungeon import level, level_init
from Player import player, playerHp
from Renderers import menuRenderer
from Resources import texts, colors
from Enemies import enemies


def action(new_y, new_x):
    if level.current_level.level[new_y][new_x] == "`":
        DoorController.close_door((new_y, new_x))
    elif level.current_level.level[new_y][new_x] in level_init.doors:
        door = DoorController.open_door((new_y, new_x))
        if isinstance(door, tuple):
            playerHp.damage_player(door[0], door[1])
            menuRenderer.debug_log("the door was trapped!", color=colors.ORANGE)
    player.action = False
    player.can_move = True


def inspect_tile(new_y, new_x):
    tile = level.current_level.level[new_y][new_x]
    if tile == "h+":
        level.current_level.level[new_y][new_x] = "+"
        menuRenderer.debug_log("you found something")
    else:
        menuRenderer.debug_log("there is nothing unusual to see here")


def attack(enemy):
    enemy.hp -= random.randint(2, 5)  # Deal damage to the enemy
    enemy.morale -= random.randint(1, 2)  # Reduce enemy morale
    enemy.last_damage_time = random.randint(10, 30)  # Deal damage to the enemy
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
            if 0 <= i < level_init.height and 0 <= j < level_init.width:
                tile = level.current_level.level[i][j]
                if tile == "h+" and random.random() < player.passive_inspect_chance:
                    level.current_level.level[i][j] = "+"
                    menuRenderer.debug_log("you noticed something")
