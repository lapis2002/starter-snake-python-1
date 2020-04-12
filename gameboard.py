class GameBoard (object):
    def __init__(self, height, weight):
        self.height = height
        self.width = width
        self.grid = [[0 for col in range(width)]
                     for row in range(height)]

    def set_cell(self, coord, value):
        self.grid[coord[0]][coord[1]] = value

    def get_cell(self, coord):
        return self.grid[coord[0]][coord[1]]
