from gameboard import *
import random

DANGER = 10
SAFE = 0
FOOD = 3
SNAKE_HEAD = 1
class Snake(Point):
    def __init__(self, snake):
        self.id = snake["id"]
        self.health = snake["health"]
        self.body, self.len = self.set_body(snake)
        self.head = self.body[0]
        self.tail = self.body[-1]
        self.next_move = ""

    def set_body(self, snake):
        head_coord = (snake["body"][0]["x"], snake["body"][0]["y"])
        body = [Point([head_coord[0], head_coord[1]], SNAKE_HEAD)]

        for coord in snake["body"][1:]:
            coord = Point([coord["x"], coord["y"]], DANGER)
            body.append(coord)

        return body, len(body)

    '''snake seems to move toward right side of the board, and toward the wall'''
    def next_movement(self, gameboard, enemies, foods):
        # print("let's find next move!")
        tails = [self.tail]
        for enemy in enemies:
            tails.append(enemy.tail)
        self.next_move = "left"
        print("let's check my health", self.health)
        if self.health < 75 and len(foods) > 0:
            # print("let's check this")
            if not(self.eat_closest_food(gameboard, foods)):
                # print("how about this?")
                if not(self.random_good_move(gameboard, enemies, tails)):
                    # print("and this?")
                    if not(self.get_not_bad_move(gameboard)):
                        if not(self.follow_tail(gameboard, enemies, tails)):
                            if not(self.random_move(gameboard)):
                                print("I'm done")
        elif not(self.random_good_move(gameboard, enemies, tails)):
            # print("and this?")
            if not(self.get_not_bad_move(gameboard)):
                if not(self.follow_tail(gameboard, enemies, tails)):
                    if not(self.random_move(gameboard)):
                        print("I'm done")

        # elif not(self.get_not_bad_move(gameboard)):
        #     if not(self.follow_tail(gameboard, tails)):
        #         if not(self.random_move(gameboard)):
        #             print("I'm done")
        
        # elif not(self.follow_tail(gameboard, tails)):
        #     if not(self.random_move(gameboard)):
        #         print("I'm done")

    def get_good_moves(self, gameboard, enemies, tails):
        neighbors = gameboard.get_neighbors(self.head)
        for neighbor in neighbors:
            # print("let's check this move", self.head.get_direction(neighbor))
            if not(self.is_good_move(gameboard, neighbor, enemies, tails)):
                neighbors.remove(neighbor)
        # print("get_good_moves responded, does it work?")
        # print("there are", len(neighbors), "neighbors left.")
        moves = [self.head.get_direction(neighbor)
                 for neighbor in neighbors]
        print("let's see what moves we got", moves)
        return moves

    '''next best move in case no move leads to better reachable area'''
    def get_not_bad_move (self, gameboard):
        next_move, next_area = self.count_next_reachable_area(gameboard)
        print("get something returned")
        if next_area == 0:
            return False
        else:
            self.next_move = next_move
            return True

    def move_toward(self, gameboard, next_cell):
        gameboard.set_cell([self.head.x, self.head.y], DANGER)
        gameboard.set_cell([next_cell.x, next_cell.y], DANGER)
        gameboard.set_cell([self.tail.x, self.tail.y], SAFE)
        return [self.tail.x, self.tail.y]

    def eat_closest_food(self, gameboard, foods):
        # print("let's find some food!")
        for food in foods:
            if len(gameboard.get_surroundings(food)) > 4:
                foods.remove(food)
        start = gameboard.get_cell([self.head.x, self.head.y])
        path = gameboard.a_star(start, foods)
        if (path is not None):
            # print("yay! food! \m/")
            self.next_move = path[0]
            return True
        else:
            # print("where is food? :(")
            return False

    def random_good_move(self, gameboard, enemies, tails):
        # print("hmm.. where should I go?")
        moves = self.get_good_moves(gameboard, enemies, tails)
        if moves:
            self.next_move = random.choice(moves)
            # print("I'm lost on the life path..")
            return True
        # print("where should I go? :?")
        return False

    def random_move(self, gameboard):
        tail_coord = [self.tail.x, self.tail.y]
        if self.len > 2:
            gameboard.set_cell(tail_coord, SAFE)
        possible_neighbors = gameboard.get_neighbors(self.head)
        if len(possible_neighbors) == 0:
            return False
        is_valid = False
        while not(is_valid):
            #there's error in the result
            random_neighbor = random.choice(possible_neighbors)
            result = gameboard.get_neighbors(random_neighbor)
            is_valid = len(result) > 0
        
        self.next_move = self.head.get_direction(random_neighbor)
        return True

    # def is_bad_move(self, gameboard):

    def is_good_move(self, gameboard, next_head, enemies, tails):
        # print("is_good_move responded")
        return not(self.is_reducing_reachable_area(gameboard, next_head) 
                or self.is_trapped(gameboard, next_head, tails)
                or self.is_threaten(gameboard,enemies, next_head))

    def is_trapped(self, gameboard, next_head ,tails):
        print("check trap?")
        print("we got", len(tails))
        start = gameboard.get_cell([next_head.x, next_head.y])
        path = gameboard.a_star(start, tails)
        # print("find any path?")
        if (path is not None):
            print("path found")
            return False
        print("no path found")
        return True
        
    def is_threaten(self, gameboard, enemies, next_head):
        enemy_heads = [enemy.head for enemy in enemies]
        for enemy_head in enemy_heads:
            if next_head in gameboard.get_neighbors(enemy_head):
                if self.len <= enemies[enemy_heads.index(next_head)]:
                    return True
        return False

    def count_next_reachable_area(self, gameboard):
        neighbors = gameboard.get_neighbors(self.head)
        # print("how many ways I have", len(neighbors))
        if len(neighbors) == 0:
            print("death end :(")
            return ("left", 0)
        area = {}
        for neighbor in neighbors:
            direction = self.head.get_direction(neighbor)
            coord = self.move_toward(gameboard, neighbor)
            area[direction] = gameboard.count_reachable_area(neighbor)
            print("I got this much area", area[direction])
            gameboard.set_back(self.tail, self.head, neighbor)
        best_direction = max(area, key=lambda key: area[key])
        print("I got this", best_direction, "and", area[best_direction])

        return (best_direction, area[best_direction])

    def is_reducing_reachable_area(self, gameboard, next_head):
        #move to this point will reduce reachable area
        # print("Do I move to less reachable area?")
        current_area = gameboard.count_reachable_area(self.head)
        # print("hmm, let's check whether the function returns something", current_area)
        coord = self.move_toward(gameboard, next_head)
        
        next_area = gameboard.count_reachable_area(next_head)
        gameboard.set_back(self.tail, self.head, next_head)
        print("now I have", current_area, "then I may have", next_area)
        if current_area > next_area:
            return True
        return False        

    def is_death_end(self, gameboard, next_head):
        next_area = gameboard.count_reachable_area(next_head)
        if next_area == 0:
            # print("Oh no :(")
            return True
        return False

    def follow_tail(self, gameboard, enemies, tails):
        if self.tail.x == self.head.x and self.tail.y == self.head.y:
            self.next_move = self.random_good_move(gameboard, enemies, tails)
            return True
             
        # print("I dont know where to go...")
        path = gameboard.a_star(self.head, [self.tail])
        if (path is not None):
            self.next_move = path[0]
            # print("finding happiness ...")
            return True
        else:
            print("I cant find my tail! @@")
            return False

    

