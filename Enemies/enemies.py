from Enemies import enemyController
from Resources import colors


class Skeleton(enemyController.EnemyController):
    def __init__(self):
        name = "Skeleton"
        enemy_symbol = 'S'
        color = colors.WHITE
        speed = 1
        hp_max = 20
        morale_max = hp_max // 2
        perception = 0

        attack_dmg = [2, 5]
        heavy_dmg = [5, 10]

        super().__init__(name, enemy_symbol, color, speed, hp_max, morale_max, perception, attack_dmg, False)
