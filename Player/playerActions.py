import random
from Dungeon import level, levelManager
from Player import player, playerHp
from Renderers import menuRenderer
from Resources import texts


def open_door(new_y, new_x):
    door = level.level[new_y][new_x]
    if door == "+":
        level.level[new_y][new_x] = "`"  # Open the door
        # menuRenderer.debug_log("Door opened")

    elif door == "t+":
        playerHp.damage_player(2, 5)
        level.level[new_y][new_x] = "`"  # Open the door
        menuRenderer.debug_log("Door was trapped")


def close_door(new_y, new_x):
    door = level.level[new_y][new_x]
    if door == "`" and not level.occupied[new_y][new_x]:
        level.level[new_y][new_x] = "+"
        # menuRenderer.debug_log("Door closed")


def action(new_y, new_x):
    if level.level[new_y][new_x] == "`":
        close_door(new_y, new_x)
    elif level.level[new_y][new_x] in level.doors:
        open_door(new_y, new_x)
    player.action = False
    player.can_move = True


def inspect_tile(new_y, new_x):
    tile = level.level[new_y][new_x]
    if tile == "h+":
        level.level[new_y][new_x] = "+"
        menuRenderer.debug_log("you found something")
    else:
        menuRenderer.debug_log("there is nothing unusual to see here")


def attack(enemy):
    enemy.hp -= random.randint(2, 5)  # Deal damage to the enemy
    enemy.morale -= random.randint(1, 2)  # Reduce enemy morale
    enemy.last_damage_time = random.randint(10, 30)  # Deal damage to the enemy


def passive_inspect(new_y, new_x):
    for i in range(new_y - 1, new_y + 1):
        for j in range(new_x - 1, new_x + 1):
            if 0 <= i < level.height and 0 <= j < level.width:
                tile = level.level[i][j]
                if tile == "h+" and random.random() < player.passive_inspect_chance:
                    level.level[i][j] = "+"
                    menuRenderer.debug_log("you noticed something")
