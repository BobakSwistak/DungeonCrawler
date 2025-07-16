import Dungeon.levelGenerator as levelGenerator
import Dungeon.level as level

levelGenerator.generate_level()

for x in range(len(level.level)):
    print("".join(level.level[x]))
