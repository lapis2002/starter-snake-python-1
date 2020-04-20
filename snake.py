from A_star import Point

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

