import heapq
from Dungeon import level, levelInit
from Resources.tiles import Tiles


class AStarAlgorithm:

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
            if 0 <= ny < levelInit.height and 0 <= nx < levelInit.width:
                if Tiles.is_walkable(level.current_level.level[ny][nx]) or Tiles.is_door(level.current_level.level[ny][nx]) and not \
                        level.current_level.occupied[ny][nx]:
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
        # Return an empty path if no valid path is found
        return [(start[0], start[1])]  # Stay in place if no path is found
