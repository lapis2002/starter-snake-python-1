from gameboard import *
import random

DANGER = 10
SAFE = 0
class Snake(Point):
    def __init__(self, snake):
        self.id = snake["id"]
        self.health = snake["health"]
        self.body, self.len = self.set_body(snake)
        self.head = self.body[0]
        self.tail = self.body[-1]
        self.next_move = ""

    def set_body(self, snake):
        body = []
        for coord in snake["body"]:
            coord = Point([coord["x"], coord["y"]], DANGER)
            body.append(coord)

        return body, len(body)

    def next_movement(self, gameboard, enemies, foods):
        tails = [self.tail]
        for enemy in enemies:
            tails.append(enemy.tail)
        self.next_move = "left"
        if self.health < 75 and len(foods) > 0:
            if not(self.eat_closest_food(gameboard, foods)):
                if not(self.random_good_move(gameboard, tails)):
                    self.follow_tail(gameboard)

    def get_good_moves(self, gameboard, tails):
        neighbors = gameboard.get_neighbors(self.head)
        for neighbor in neighbors:
            if self.is_bad_move(gameboard, neighbor, tails):
                neighbors.remove(neighbor)
        moves = [self.head.get_direction(neighbor)
                 for neighbor in neighbors]

    def move_toward(self, gameboard, next_cell):
        gameboard.set_cell([next_cell.x, next_cell.y], DANGER)
        gameboard.set_cell([self.tail.x, self.tail.y], SAFE)
        return [self.tail.x, self.tail.y]

    def eat_closest_food(self, gameboard, foods):
        for food in foods:
            if len(gameboard.get_surroundings(food)) > 4:
                foods.remove(food)
        start = gameboard.get_cell([self.head.x, self.head.y])
        path = gameboard.a_star(start, foods)
        if (path is not None):
            print("yay! food! \m/")
            self.next_move = path[0]
            return True
        else:
            print("where is food? :(")
            return False


    def random_good_move(self, gameboard, tails):
        # tail_coord = [self.tail.x, self.tail.y]
        # if self.len > 2:
        #     gameboard.set_cell(tail_coord, SAFE)
        # possible_neighbors = gameboard.get_neighbors(self.head)
        # is_valid = False
        # while not(is_valid):
        #     random_neighbor = random.choice(possible_neighbors)
        #     result = gameboard.get_neighbors(random_neighbor)
        #     is_valid = len(result) > 0
        moves = self.get_good_moves(gameboard, tails)
        if moves:
            self.next_move = random.choice(moves)
            print("I'm lost on the life path..")
            return True
        print("where should I go? :?")
        return False

    def is_good_move(self, gameboard, next_head, tails):
        return not(self.is_reducing_reachable_area(gameboard, next_head) 
                and self.is_trapped(gameboard, next_head, tails) 
                and self.is_threaten)

    def is_trappped(self, gameboard, next_head ,tails):
        start = gameboard.get_cell([next_head.x, next_head.y])
        path = gameboard.a_star(start, tails)
        if (path is not None):
            return False
        else:
            return True
        
    def is_threaten(self, gameboard, enemies, next_head):
        enemy_heads = [enemy.head for enemy in enemies]
        if next_head in enemy_heads:
            if self.len <= enemies[enemy_heads.index(next_head)]:
                return True
        return False

    def count_next_reachable_area(self, gameboard):
        neighbors = gameboard.get_neighbors(self.head)
        if len(neighbors) == 0:
            print("death end :(")
            return ("left", 0)
        area = {}
        for neighbor in neighbors:
            direction = self.head.get_direction()
            coord = self.move_toward(gameboard, neighbor)
            area[direction] = gameboard.count_reachable_area(neighbor)
            gameboard.set_back(self.tail, neighbor)

        best_direction = max(area, key=lambda key: area[key])
        return (best_direction, area[best_direction])

    def is_reducing_reachable_area(self, gameboard, next_head):
        #move to this point will reduce reachable area
        coord = self.move_toward(gameboard, next_head)
        next_area = gameboard.count_reachable_area(next_head)
        gameboard.set_back(self.tail, next_head)
        current_area = gameboard.count_reachable_area(self.head)
        if current_area > next_area:
            return True
        return False        

    def is_death_end(self, gameboard, next_head):
        next_area = gameboard.count_reachable_area(next_head)
        if next_area == 0:
            print("Oh no :(")
            return True
        return False

    def follow_tail(self, gameboard):
        path = gameboard.a_star(self.head, [self.tail])
        if (path is not None):
            self.next_move = path[0]
            print("finding happiness ...")
            return True
        else:
            print("I cant find my tail! @@")
            return False

    

