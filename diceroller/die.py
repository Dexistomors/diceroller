class Die:

    def __init__(self, faces, advantage = 0, reroll_rules = []):
        self.faces = faces
        self.advantage = advantage
        self.reroll_rules = reroll_rules
        self.dieresult = None

    def set_faces(self, faces):
        pass

    def set_advantage(self, advantage):
        pass

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