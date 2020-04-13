from A_star import Point
# class Point():
#     def __init__(self, coord):
#         self.x = coord[0]
#         self.y = coord[1]

#     def __eq__(self, other):
#         return self.x == other.x and self.y and other.y

#     def get_x(self):
#         return self.x

#     def get_y(self):
#         return self.y

#     def left(self):
#         return Point([self.x-1, self.y])

#     def right(self):
#         return Point([self.x+1, self.y])

#     def up(self):
#         return Point([self.x, self.y-1])

#     def down(self):
#         return Point([self.x, self.y+1])
        
#     def neighbors(self):
#         return [self.left(), self.up(), self.right(), self.down()]

class GameBoard (Point):
    def __init__(self, height, weight):
        self.height = height
        self.width = width
        self.grid = [[0 for col in range(width)]
                     for row in range(height)]

    def set_cell(self, coord, value):
        self.grid[coord[0]][coord[1]] = value

    def get_cell(self, coord):
        return self.grid[coord[0]][coord[1]]

