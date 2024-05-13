class Die:

    def __init__(self, faces, advantage = 0, reroll_rules = []):
        self.set_faces(faces)
        self.set_advantage(advantage)
        self.reroll_rules = reroll_rules
        self.dieresult = None

    def set_faces(self, faces):
        if type(faces) == int:
            self.faces = faces
        else:
            raise DieException("faces has incorrect data type")

    def set_advantage(self, advantage):
        if type(advantage) == int and (-1 <= advantage <= 1):
            self.advantage = advantage
        else:
            raise DieException("advantage has incorrect data type")

    def add_reroll_rule(self, reroll_rule):
        pass

    def remove_reroll_rule(self, reroll_rule):
        pass

    def roll(self):
        pass

    def reset(self):
        pass

    def get_die_result(self):
        pass

class DieException(Exception):
    pass