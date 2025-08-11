from Enemies import enemyController
from Resources import colors

enemies_list = []


class Skeleton(enemyController.EnemyController):
    def __init__(self):
        super().__init__()  # Properly initialize the parent class
        self.name = "Skeleton"
        self.enemy_symbol = 'S'
        self.color = colors.WHITE
        self.speed = 1
        self.hp = 20
        self.hp_max = 20
        self.perception = 0
        self.morale = 2  # Morale of the enemy
        self.max_morale = 2  # Maximum morale of the enemy
        self.enemy_pos = None  # Initialize enemy position




        self.enemy_position()
        self.find_target_pos()
        self.create_path()
