class RerollRule:

    def __init__(self, condition, action, die):
        self.condition = condition
        self.action = action
        self.die = die

    def run(self):
        pass