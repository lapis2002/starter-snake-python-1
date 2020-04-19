import os
import random
from snake import Snake
# from gameboard import GameBoard
from A_star import *
import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

SAFE = 1
FOOD = 7
E_HEAD = 5
DANGER = 10


def dist(p1, p2):
    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])
    return dx + dy

def find_food():
    return None

def get_food(foods, gameboard, snake):
    start = gameboard.get_cell([snake.head.x, snake.head.y])
    foods = sorted(foods, key=lambda x: start.distance(x))
    end = gameboard.get_cell([foods[0].x, foods[0].y])
    snake.next_move = gameboard.process(start, end)[0]

def next_move (foods, gameboard, opponents, snake):
    for enemy in opponents:
        get_food(foods, gameboard, enemy)
        coord = enemy.head.get_cell_from_direction(enemy.next_move)
        gameboard.set_cell(coord, DANGER)

    find_food(foods, gameboard, snake)
    # if snake.health < 30:
    #     find_food(foods, gameboard, snake)
    # else:
    #     get_food(foods, gameboard, snake)

def find_food(foods, gameboard, snake):
    for food in foods:
        gameboard.set_cell([food.x, food.y], 0)
    get_food(foods, gameboard, snake)

def follow_tail(gameboard, snake):
    start = gameboard.get_cell([snake.head.x, snake.head.y])
    end = gameboard.get_cell([snake.tail.x, snake.tail.y])
    snake.next_move = gameboard.process(start, end)[0]


def init(data):
    foods = []
    opponents = []
    # data = cherrypy.request.json
    grid = Grid(data["board"]["height"], data["board"]["width"])
    my_snake = Snake(data["you"], DANGER)

    grid.set_grid()
    for coord in my_snake.body[:-1]:
        grid.set_cell([coord.x, coord.y], DANGER)

    for food in data["board"]["food"]:
        food = Point([food["x"], food["y"]], FOOD)
        foods.append(food)
        grid.set_cell([food.x, food.y], FOOD)

    for snake in data["board"]["snakes"]:
        snake = Snake(snake, DANGER)
        if snake.id != my_snake.id:
            opponents.append(snake)
            for coord in snake.body[:-1]:
                grid.set_cell([coord.x, coord.y], coord.v)
            
    for y in range(len(grid.grid)):
        for x in range(len(grid.grid[0])):
            if x == my_snake.head.x and y == my_snake.head.y:
                print("@ ", end ="")
            elif grid.grid[x][y] == 10:
                print("* ", end="")
            elif grid.grid[x][y] == 7:
                print("o ", end="")
            else:
                print(". ", end="")
        print()
    return my_snake, grid, foods, opponents


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        print("test")
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        print("START")
        return {"color": "#C06C84", "headType": "bendr", "tailType": "curled"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        '''
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)
        # move = "left"
        check = 0

        if data["you"]["body"][0]["x"] == 0 or data["you"]["body"][0]["x"] == data["board"]["width"]-1:
            if data["you"]["body"][0]["x"] != data["you"]["body"][1]["x"]:
                if data["you"]["body"][0]["y"] == 0:
                    move = "down"
                else:
                    move = "up"
            elif data["you"]["body"][1]["x"] == 0:
                move = "right"
            else:
                move = "left"

        elif data["you"]["body"][0]["y"] == 0 or data["you"]["body"][0]["y"] == data["board"]["height"]-1:
            if data["you"]["body"][0]["y"] != data["you"]["body"][1]["y"]:
                if data["you"]["body"][0]["x"] == 0:
                    move = "right"
                else:
                    move = "left"
            elif data["you"]["body"][1]["y"] == 0:
                move = "down"
            else:
                move = "up"

        else:
            if data["you"]["body"][0]["y"] > data["you"]["body"][1]["y"]:
                # move = "down"
                possible_moves = ["down", "down", "left", "right"]
            elif data["you"]["body"][0]["y"] < data["you"]["body"][1]["y"]:
                # move = "up"
                possible_moves = ["up", "up", "left", "right"]
            elif data["you"]["body"][0]["x"] > data["you"]["body"][1]["x"]:
                # move = "right"
                possible_moves = ["up", "down", "right", "right"]
            else:
                # move = "left"
                possible_moves = ["up", "down", "left", "left"]

            move = random.choice(possible_moves)
        '''


        my_snake, grid, foods, opponents = init(data)
        # if my_snake.len < 3 or my_snake.health < 30:
        #     get_food(foods, grid, my_snake)
        # else:
        #     follow_tail(grid, my_snake)
        next_move(foods, grid, opponents, my_snake)

        move = my_snake.next_move
        
        print(f"MOVE: {move}")
        # print(data["you"])
        return {"move": move}

    

        


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


        

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
