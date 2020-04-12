class Snake(object):
    def __init__(self, snake):
        self.id = snake["id"]
        self.health = snake["health"]
        self.body, self.len = self.set_body(snake)

    def set_body(self, snake):
        body = []
        for coord in snake["body"]:
            body.append([coord["x"], coord["y"]])

        return body, len(body)

    def get_body(self):
        return self.body