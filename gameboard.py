class Point():
    def __init__(self, coord, value):
        # self.reachable = reachable
        self.x = coord[0]
        self.y = coord[1]
        self.parent = None
        self.v = value
        self.g = 0
        self.h = 0
        self.f = 0

    def get_direction(self):
        if self.parent.x > self.x:
            direction = "left"
        elif self.parent.x < self.x:
            direction = "right"
        elif self.parent.y > self.y:
            direction = "up"
        elif self.parent.y < self.y:
            direction = "down"
        return direction

    def distance(self, other):
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        return dx + dy

    def __eq__(self, other):
        return self.x == other.x and self.y and other.y


class GameBoard (Point):
    def __init__(self, height, weight, value=0):
        self.height = height
        self.width = width
        self.grid = [[value for col in range(width)]
                     for row in range(height)]

    def set_cell(self, coord, value):
        self.grid[coord[0]][coord[1]] = (value)

    def get_cell(self, coord):
        return self.grid[coord[0]][coord[1]]

    def get_neighbors(self, point):
        neighbors = []
        if point.x > 0:
            neighbors.append([point.x-1, point.y])
        if point.y > 0:
            neighbors.append([point.x, point.y-1])
        if point.x < self.width-1:
            neighbors.append([point.x+1, point.y])
        if point.y < self.height-1:
            neighbors.append([point.x, point.y+1])
        return neighbors

    def update_cell(self, child, parent, end):
        child.g = parent.g + child.v
        child.h = child.distance(end)
        child.parent = parent
        child.f = child.g + child.h

