from Enemies import enemyController

enemies_list = []


class Skeleton(enemyController.EnemyController):
    def __init__(self):
        super().__init__()  # Properly initialize the parent class
        self.name = "Skeleton"
        self.enemy_symbol = 'S'
        self.color = 1
        self.speed = 1
        self.hp = 10
        self.perception = 1
        self.enemy_pos = [0, 0]

        self.enemyPosition()
        self.find_target_pos()
        self.create_path()