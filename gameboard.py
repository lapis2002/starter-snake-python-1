DANGER = 10
SAFE = 0
FOOD = 3
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

    def get_direction(self, other):
        if other.x > self.x:
            direction = "right"
        elif other.x < self.x:
            direction = "left"
        elif other.y > self.y:
            direction = "down"
        elif other.y < self.y:
            direction = "up"
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

    def isGoal(self, goals):
        coord_goals = [[goal.x, goal.y] for goal in goals]
        for coord in coord_goals:
            if (coord[0] == self.x) and (coord[1] == self.y):
                return True
        return False

    def get_heuistic(self, goals):
        closest = float("inf")
        for goal in goals:
            dist = self.distance(goal)
            closest = min(closest, dist)
        return closest
    
    def is_neighbor_of(self, gameboard, other):
        neighbors = gameboard.get_neighbors([self.x, self.y])
        if other in neighbors:
            return True
        return False

class Grid ():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[SAFE for col in range(width)]
                     for row in range(height)]
        self.next_stage = [[SAFE for col in range(width)]
                            for row in range(height)]
        self.cells = []

    def set_cell(self, coord, value):
        # reachable = point.reachable
        # value = point.v
        self.grid[coord[0]][coord[1]] = (value)
        self.cells[coord[0]*self.height + coord[1]] = Point([coord[0], coord[1]], value) 

    # def set_cell_next_stage(self, coord, value):
    #     self.grid[coord[0]][coord[1]] = (value)

    # def set_back_to_current_stage(self, coord, value):
    #     self.grid[coord[0]][coord[1]] = (value)

    '''set the grid back to the current stage after consider the next stage'''
    def set_back(self, prev_tail, next_head):
        self.set_cell([prev_tail.x, prev_tail.y], DANGER)
        self.set_cell([next_head.x, next_head.y], SAFE)

    def set_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                # value = self.grid[x][y]
                self.cells.append(Point([x, y], SAFE))

    def get_cell(self, coord):
        return self.cells[coord[0]*self.height + coord[1]]

    def get_path(self, start, end):
        path = []
        current = end
        while current.parent is not start:
            path.append(current.parent.get_direction(current))
            current = current.parent
        path.append(current.parent.get_direction(current))
        return path[::-1]

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

    def get_surroundings(self, point):
        surroundings = []
        if point.x > 0 and self.grid[point.x-1][point.y] != DANGER:
            surroundings.append(self.get_cell([point.x-1, point.y]))
            if point.y > 0 and self.grid[point.x-1][point.y-1] != DANGER:
                surroundings.append(self.get_cell([point.x-1, point.y-1]))
            if point.y < self.height-1 and self.grid[point.x-1][point.y+1] != DANGER:
                surroundings.append(self.get_cell([point.x-1, point.y+1]))

        if point.y > 0 and self.grid[point.x][point.y-1] != DANGER:
            surroundings.append(self.get_cell([point.x, point.y-1]))
            if point.x > 0 and self.grid[point.x-1][point.y-1] != DANGER:
                surroundings.append(self.get_cell([point.x-1, point.y-1]))
            if point.x < self.width-1 and self.grid[point.x+1][point.y-1] != DANGER:
                surroundings.append(self.get_cell([point.x+1, point.y-1]))

        if point.x < self.width-1 and self.grid[point.x+1][point.y] != DANGER:
            surroundings.append(self.get_cell([point.x+1, point.y]))
        if point.y < self.height-1 and self.grid[point.x][point.y+1] != DANGER:
            surroundings.append(self.get_cell([point.x, point.y+1]))
        return surroundings

    def update_cell(self, adj, point, goals):
        adj.g = point.g + adj.v
        adj.h = adj.get_heuistic(goals)
        adj.parent = point
        adj.f = adj.g + adj.h
        self.set_cell([adj.x, adj.y], adj.f)

    '''this function is finding the cell with specific value, 
    follow_tail finds the cell with specific coord'''
    def a_star(self, start, goals):
        #return path if found, NoneType otherwise
        opened = []
        closed = set()
        # start = self.get_cell(start)
        # end = self.get_cell(end)
        opened.append(start)
        while len(opened) > 0:
            point = min(opened, key=lambda x: x.f)
            opened.remove(point)
            closed.add(point)
            if point.isGoal(goals):
                return self.get_path(start, point)

            neighbors = self.get_neighbors(point)
            for neighbor in neighbors:
                if neighbor not in closed:
                    if neighbor in opened:
                        # print("neighbor", neighbor.g)
                        # print("current", point.g + neighbor.v)
                        if neighbor.g > neighbor.v + point.g:
                            self.update_cell(neighbor, point, goals)
                    else:
                        self.update_cell(neighbor, point, goals)
                        opened.append(neighbor)

    #cell is a Point
    def flood_fill(self, cell, visited):
        # coord = [cell.x, cell.y]
        if cell in visited or cell.v == DANGER:
            return 0
        visited.append(cell)
        neighbors = self.get_neighbors(cell)
        reachable_cells = 1
        for neighbor in neighbors:
            reachable_cells += self.flood_fill(neighbor, visited)
        return reachable_cells

    def count_reachable_area(self, cell):
        visited = []
        return self.flood_fill(cell, visited)

    #enemies: list of snake
    def is_on_enemy_way(self, enemies, snake):
        head = self.get_cell([snake.head.x, snake.head.y])
        for enemy in enemies:
            enemy_head = self.get_cell([enemy.head.x, enemy.head.y])
            if snake.len < enemy.len:
                if head in self.get_neighbors(enemy_head):
                    return True
        return False

    #cell is a Point
    def get_reachable_area_list_from_flood_fill(self, cell, visited):
        # coord = [cell.x, cell.y]
        if cell in visited or cell.v == DANGER:
            return visited
        visited.append(cell)
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            self.get_reachable_area_list_from_flood_fill(neighbor, visited)
        return visited

    def get_reachable_area(self, cell):
        visited = []
        self.get_reachable_area_list_from_flood_fill(cell, visited)

    #cell is a Point
    def get_reachable_head_tail(self, cell, visited, heads, tails, 
                                reachable_heads, reachable_tails):
        # coord = self.get_cell([snake.head.x, snake.head.y])
        if cell in visited:
            if cell in heads and cell not in reachable_heads:
                reachable_heads.append(cell)
            if cell in tails and cell not in reachable_tails:
                reachable_tails.append(cell)
            return visited
        visited.append(cell)

        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            self.get_reachable_head_tail(cell, visited, heads, tails, 
                                        reachable_heads, reachable_tails)
        return visited

        




        



    

    


    


