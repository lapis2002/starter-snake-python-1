# from gameboard import Point
import heapq

#TO DO: fix g
class Point():
    def __init__(self, coord, reachable, value):
        self.reachable = reachable
        self.x = coord[0]
        self.y = coord[1]
        self.parent = None
        self.g = value
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

    def distance (self, other):
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        return dx + dy

class Grid ():
    def __init__(self, height, width):
        self.opened = []
        self.closed = set()
        self.cells = []
        self.height = height
        self.width = width
        self.grid = [[(False, 1) for col in range(width)]
                     for row in range(height)]

    def set_cell(self, point):
        reachable = point.reachable
        value = point.g
        self.grid[point.x][point.y] = (reachable, value)

    def set_grid(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
                 (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                reachable, value = self.grid[x][y]
                self.cells.append(Point(x, y, reachable, value))

        print(len(self.cells))
        # self.start = self.get_cell(0, 0)
        # self.end = self.get_cell(5, 5)

    # def get_heuistic(self, point, end):
    #     dx = abs(point.x-end.x)
    #     dy = abs(point.y-end.y)
    #     return dx + dy

    def get_cell(self, coord):
        return self.cells[coord[0]*self.height + coord[1]]


    def get_path(self, start, end):
        path = []
        point = end
        while point.parent is not start:
            path.append(point.get_direction())
            point = point.parent

        path.append(point.get_direction())


    def get_neighbor(self, point):
        neighbors = []
        if point.get_x() > 0:
            neighbors.append(self.get_cell([point.x-1, point.y]))
        if point.get_y() > 0:
            neighbors.append(self.get_cell([point.x, point.y-1]))
        if point.get_x() < self.width-1:
            neighbors.append(self.get_cell([point.x+1, point.y]))
        if point.get_y() < self.height-1:
            neighbors.append(self.get_cell([point.x, point.y+1]))
        return neighbors

    def update_cell(self, adj, point, end):
        adj.g += point.g
        # adj.h = self.get_heuistic(adj, end)
        adj.h = adj.distance(end)
        adj.parent = point
        adj.f = adj.g + adj.h

    def process(self, start, end):
        # start: coord of start
        # end: coord of end
        start = self.get_cell(start)
        end = self.get_cell(end)
        heapq.heappush(self.opened, (start, start.f))
        while len(self.opened):
            point, f = heapq.heappop(self.opened)
            self.closed.add(point)
            if point is self.end:
                return self.get_path(start, end)
            neighbors = self.get_neighbors(point)
            for neighbor in neighbors:
                if neighbor.reachable and neighbor not in self.closed:
                    if (neighbor.f, neighbor) in self.opened:
                        if neighbor.g > neighbor.g + point.g:
                            self.update_cell(neighbor, point, end)
                    else:
                        self.update_cell(neighbor, point, end)
                        heapq.heappush(self.opened, (neighbor, neighbor.f))



def dist(p1, p2):
    dx = abs(p1.get_x()-p2.get_x())
    dy = abs(p1.get_y()-p2.get_y())
    return dx + dy

def valid_move(grid, moves):
    return None
