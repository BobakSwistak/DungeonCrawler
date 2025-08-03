from Dungeon import level, levelGenerator
import random
import heapq


class EnemyManager:
    def __init__(self):
        self.level = level.level
        self.speed = 1
        self.hp = 1
        self.target_pos = None
        self.path = []

    def enemyPosition(self):
        self.enemy_pos = [random.randint(0, level.height), random.randint(0, level.width)]

        if level.level[self.enemy_pos[0]][self.enemy_pos[1]] not in level.walkable:
            self.enemyPosition()

    def controller(self):
        self.enemyPosition()
        self.find_target_pos()
        self.create_path()
        print("Initial path:", self.path)

    def move(self):
        if not self.path:
            self.create_path()
            return

        # Move one step along the path
        next_pos = self.path.pop(0)
        self.enemy_pos = list(next_pos)
        # level.level[self.enemy_pos[0]][self.enemy_pos[1]] = 'M'  # Mark enemy position

        # If we reached the target, pick a new one
        if self.enemy_pos == self.target_pos:
            self.find_target_pos()
            self.create_path()

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

        if self.path:
            print(f"Path from {start} to {goal}: {self.path}")
        else:
            print(f"No valid path found from {start} to {goal}")

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

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < level.height and 0 <= nx < level.width:
                if level.level[ny][nx] in level.walkable:
                    neighbors.append((ny, nx))

        # Debug: Print neighbors for the current position
        print(f"Neighbors of {pos}: {neighbors}")
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

            # Debug: Print current node being processed
            print(f"Processing node: {current}")

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

        # Debug: No path found
        print(f"No path found from {start} to {goal}")
        return []


# === RUNNING ===
levelGenerator.generate_dungeon()


enemy_manager = EnemyManager()
enemy_manager.controller()

# Simulate movement for 20 steps
for _ in range(20):
    enemy_manager.move()


for i in enemy_manager.path:
    level.level[i[0]][i[1]] = 'E'  # Mark path with 'E'
print("\n".join("".join(str(j) for j in i) for i in level.level))