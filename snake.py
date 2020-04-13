from A_star import Point

class Snake(Point):
    def __init__(self, snake, value):
        self.id = snake["id"]
        self.health = snake["health"]
        self.body, self.len = self.set_body(snake, value)
        self.head = self.body[0]
        self.tail = self.body[-1]
        self.next_move = ""

    def set_body(self, snake, value):
        body = []
        for coord in snake["body"]:
            coord = Point([coord["x"], coord["y"]], False, value)
            body.append(coord)

        return body, len(body)

