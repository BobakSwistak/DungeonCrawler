import curses
import random

hp = 0
max_hp = 30
heal_counter = 0  # Track recent damage for healing purposes


def hp_init():
    global hp, max_hp, heal_counter
    heal_counter = random.randint(10, 30)
    hp = max_hp


def hp_update():
    global hp, max_hp, heal_counter
    heal_counter -= 1
    if heal_counter <= 0 and hp < max_hp:
        heal_counter = 0
        hp += 1
        heal_counter = random.randint(10, 30)


def damage_player(dmg_min, dmg_max):  # healing is the same but -dmg
    global hp
    dmg = random.randint(dmg_min, dmg_max)
    hp -= dmg


def rest(counter):
    while counter > 0:
        counter -= 1

