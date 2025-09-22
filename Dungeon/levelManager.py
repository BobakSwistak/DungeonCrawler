from Dungeon import level, levelGenerator
from Resources.tiles import Tiles


class levelManager:
    @staticmethod
    def go_level_downwards(staircase_pos):
        if level.current_level.level[staircase_pos[0]][staircase_pos[1]] == Tiles.staircase_down:
            level.current_level.last_staircase_down = staircase_pos
            if level.levels.index(level.current_level) + 1 < len(level.levels):
                level.current_level = level.levels[level.levels.index(level.current_level) + 1]

            else:

                level.levels.append(level.Level())
                level.current_level = level.levels[level.levels.index(level.current_level) + 1]
                level.current_level.player_x, level.current_level.player_y = levelGenerator.generate_dungeon(
                    level.levels.index(level.current_level) + 1)
