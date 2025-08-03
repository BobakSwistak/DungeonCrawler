class Enemy:  # skeleton, orc, goblin, etc.

    test_var = 10;

    def __init__(self):
        self.name = 0
        self.health = 0
        self.speed = 2

    def func_name(self):
        return self.name


class Orc(Enemy):
    def __init__(self):
        super().__init__()  # calling __init__ from Enemy
        self.name = 10

    def func_name(self):
        return "FISH"

    def get_speed(self):
        return self.speed


class Goblin(Enemy):

    def func_war_cry(self):
        return "BLOOD FOR THE BLOOD GOD"

    def get_speed(self):
        return 2


enemies = []
orc = Orc()
goblin = Goblin()

enemies.append(Orc())
print(enemies[0].func_name())
print(orc.speed)

orc.test_var = 20

print(orc.test_var)
print(goblin.test_var)
