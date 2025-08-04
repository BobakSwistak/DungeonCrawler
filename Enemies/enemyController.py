from Dungeon import level, levelManager
from Player import player
from Renderers import menuRenderer
import random
import heapq


class EnemyController:
    def __init__(self):
        self.name = "Enemy"
        self.enemy_symbol = 'M'  # Symbol for the enemy
        self.color = 1  # Color code for rendering
        self.speed = 1
        self.hp = 1
        self.perception = 1

        self.enemy_pos = None
        self.target_pos = None
        self.path = []
        self.agro = False

        self.enemyPosition()
        self.find_target_pos()
        self.create_path()

    def controller(self):
        if not self.agro:
            self.field_of_view = levelManager.calculate_field_of_view(self.enemy_pos[0], self.enemy_pos[1],
                                                                      10 + self.perception)
        else:
            self.target_pos = [player.player_y, player.player_x]
            self.create_path()

        self.move()
        if [player.player_y, player.player_x] in self.path:
            self.agro = True

    def move(self):
        if not self.path:
            self.create_path()
            return
        self.enemy_pos = self.path.pop()
        menuRenderer.debug_log("Enemy moved to position: {}".format(self.enemy_pos))

    def enemyPosition(self):
        while True:
            self.enemy_pos = [random.randint(0, level.height - 1), random.randint(0, level.width - 1)]
            if level.level[self.enemy_pos[0]][self.enemy_pos[1]] in level.walkable:
                break

    def find_target_pos(self):
        while True:
            target_pos = [random.randint(1, level.height - 2), random.randint(1, level.width - 2)]
            if level.level[target_pos[0]][target_pos[1]] in level.walkable:
                self.target_pos = target_pos
                break

    def create_path(self):
        start = tuple(self.enemy_pos)
        goal = tuple(self.target_pos)
        self.path = self.astar(start, goal)

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_neighbors(self, pos):
        y, x = pos
        neighbors = []

        # Include diagonal movements
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal directions
        ]

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < level.height and 0 <= nx < level.width:
                if level.level[ny][nx] in level.walkable:
                    neighbors.append((ny, nx))
        return neighbors

    def astar(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []

#
# # levelGenerator.generate_dungeon()
#
# enemy_manager = EnemyController()
# enemy_manager.controller()
#
# for i in enemy_manager.path:
#     level.level[i[0]][i[1]] = 'E'  # Mark path with 'E'
# print("\n".join("".join(str(j) for j in i) for i in level.level))
