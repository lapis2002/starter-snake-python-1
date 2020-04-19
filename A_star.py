# from gameboard import Point

#FIX SET_CELL/SET_GRID!!!!!!
from gameboard import *
DANGER = 10
#TO DO: fix g
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

    def get_cell_from_direction(self, direction):
        if direction == "up":
            x = self.x
            y = self.y - 1
        elif direction == "right":
            x = self.x + 1
            y = self.y
        elif direction == "down":
            x = self.x
            y = self.y + 1
        else:
            x = self.x - 1
            y = self.y
        return [x, y]

    def distance (self, other):
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        return dx + dy

class Grid ():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[0 for col in range(width)]
                     for row in range(height)]
        self.cells = []

    def set_cell(self, coord, value):
        # reachable = point.reachable
        # value = point.v
        self.grid[coord[0]][coord[1]] = (value)
        self.cells[coord[0]*self.height + coord[1]] = Point([coord[0], coord[1]], value)
        

    def set_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                # value = self.grid[x][y]
                self.cells.append(Point([x, y], 0))

        # self.start = self.get_cell(0, 0)
        # self.end = self.get_cell(5, 5)

    # def get_heuistic(self, point, end):
    #     dx = abs(point.x-end.x)
    #     dy = abs(point.y-end.y)
    #     return dx + dy

    def get_cell(self, coord):
        return self.cells[coord[0]*self.height + coord[1]]

    ###
    def init_grid(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
                 (3, 1), (3, 2), (3, 5), (4, 4), (5, 1))

        start = (0,0)
        end = (5,2)
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in walls:
                    reachable = False
                    value = 10
                else:
                    reachable = True
                    value = 0
                if x==1 and y==4:
                    value = 7
                if x==5 and y==2:
                    value = 7
                if x == 4 and y == 2:
                    value = 7
                if x == 4 and y == 1:
                    value = 7
                self.set_cell([x,y],value)
                self.cells.append(Point([x, y], value))
        self.start = self.get_cell(start)
        self.end = self.get_cell(end)


    def get_path(self, start, end):
        path = []
        dir = []
        current = end
        while current.parent is not start:
            path.append(current.get_direction())
            current = current.parent
        # print("go to", (current.x, current.y))

        path.append(current.get_direction())
        print("path return", path[::-1])
        return path[::-1]
    
    # def get_path(self):
    #     cell = self.end
    #     path = [(cell.x, cell.y)]
    #     while cell.parent is not self.start:
    #         cell = cell.parent
    #         path.append((cell.x, cell.y))
    #     path.append((self.start.x, self.start.y))
    #     path.reverse()
    #     return path

    # def distance(self, p1, p2):
    #     dist_x = dist_y = 0
    #     for x in range(p1.x + 1, p2.x + 1):
    #         dist_x += self.grid[x][1] 

    def get_neighbors(self, point):
        neighbors = []
        if point.x > 0 and self.grid[point.x-1][point.y] != DANGER:
            neighbors.append(self.get_cell([point.x-1, point.y]))
        if point.y > 0 and self.grid[point.x][point.y-1] != DANGER:
            neighbors.append(self.get_cell([point.x, point.y-1]))
        if point.x < self.width-1 and self.grid[point.x+1][point.y] != DANGER:
            neighbors.append(self.get_cell([point.x+1, point.y]))
        if point.y < self.height-1 and self.grid[point.x][point.y+1] != DANGER:
            neighbors.append(self.get_cell([point.x, point.y+1]))
        return neighbors

    def update_cell(self, adj, point, end):
        adj.g = point.g + adj.v
        # adj.h = self.get_heuistic(adj, end)
        adj.h = adj.distance(end)
        adj.parent = point
        adj.f = adj.g + adj.h
        self.set_cell([adj.x, adj.y], adj.f)
        # for y in range(self.height):
        #     print(self.grid[y])
        # print()

    def process(self, start, end):
        opened = []
        closed = set()
        # start = self.get_cell(start)
        # end = self.get_cell(end)
        opened.append(start)
        while len(opened) > 0:
            point = min(opened, key=lambda x: x.f)
            opened.remove(point)

            closed.add(point)

            if point is end:
                return self.get_path(start, end)

            neighbors = self.get_neighbors(point)
            for neighbor in neighbors:
                if neighbor not in closed:
                    if neighbor in opened:
                        print("neighbor", neighbor.g)
                        print("current", point.g + neighbor.v)
                        if neighbor.g > neighbor.v + point.g:
                            self.update_cell(neighbor, point, end)
                    else:
                        self.update_cell(neighbor, point, end)
                        opened.append(neighbor)

    # def a_star (self, start, end):
    #     self.opened = []
    #     start = self.get_cell(start)
    #     end = self.get_cell(end)
    #     self.opend.append([start.x, start.y])
    #     self.closed.add([start.x, start.y])
    #     while len(self.opened) > 0:
    #         current = self.opened[0]
    #         print(current)

    #         current = self.get_cell(current)
    #         print(type(current))
    #         if current is self.end:
    #             return self.get_path(start, end)
            
    #         neighbors = self.get_neighbors(current)
    #         for neighbor in neighbors:
    #             if neighbor in self.closed:
    #                 continue
    #             if neighbor in self.opened:
    #                 if neighbor.g > neighbor.v + current.g:
    #                     self.update_cell(neighbor, current, end)
    #             else:
    #                 self.update_cell(neighbor, current, end)
    #                 self.opened.append(neighbor)



        '''
            start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
            '''


def dist(p1, p2):
    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])
    return dx + dy

def a_star (grid, start, end):
    opened = [start]
    closed = set()

    g = GameBoard(grid.height, grid.weight, 1)
    g.set_cell(start,0)
    f = GameBoard(grid.height, grid.weight)
    f.set_cell(start, dist(start, end))

    while len(opened) > 0:
        current = min(opened, key=lambda x: f.get_cell(x))
        opened.remove(current)

        if current == end:
            return grid.get_path(start, end)

        closed.add(current)
        neighbors = grid.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor in closed:
                continue
            if neighbor in opened:
                if g.get_cell(neighbor) > grid.get_cell(neighbor) + g.get_cell(current):
                    g.set_cell(neighbor, grid.get_cell(neighbor) + g.get_cell(current))
                    f.set_cell(neighbor, grid.get_cell(neighbor) + 
                              g.get_cell(current) + dist(neighbor, end))
            else:
                g.set_cell(neighbor, grid.get_cell(neighbor) + g.get_cell(current))
                opened.append(neighbor)
                f.set_cell(neighbor, grid.get_cell(neighbor) +
                           g.get_cell(current) + dist(neighbor, end))




'''
def process(self, start, end):
        # start: coord of start
        # end: coord of end
        opened = []
        closed = set()
        start = self.get_cell(start)
        end = self.get_cell(end)
        opened.append((start, start.f))
        while len(opened) > 0:
            point, f = min(opened, key=lambda x: x[1])
            opened.remove((point, f))
            closed.add(point)
            if point is end:
                return self.get_path(start, end)
            neighbors = self.get_neighbors(point)
            for neighbor in neighbors:
                if neighbor not in closed:
                    if (neighbor.f, neighbor) in opened:
                        print("neighbor", neighbor.g)
                        print("current", point.g + neighbor.v)
                        if neighbor.g > neighbor.v + point.g:
                            self.update_cell(neighbor, point, end)
                    else:
                        self.update_cell(neighbor, point, end)
                        opened.append((neighbor, neighbor.f))

'''

