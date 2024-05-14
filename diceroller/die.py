from diceroller.rerollrule import RerollRule
import random

class Die:

    def __init__(self, faces, advantage = 0, reroll_rules = []):
        self.set_faces(faces)
        self.set_advantage(advantage)
        self.set_reroll_rules(reroll_rules)
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

    def set_reroll_rules(self, reroll_rules):
        self.reroll_rules = []
        if type(reroll_rules) != list:
            raise DieException("reroll_rules has incorrect data format")
        for reroll_rule in reroll_rules:
            self.add_reroll_rule(reroll_rule)
        

    def add_reroll_rule(self, reroll_rule):
        if type(reroll_rule) == RerollRule:
            self.reroll_rules.append(reroll_rule)
        else:
            raise DieException("reroll_rule not of RerollRule class")
            

    def remove_reroll_rule(self, reroll_rule):
        pass

    def roll(self):
        if self.dieresult is None:
            self.dieresult = []
        if type(self.faces) == int:
            self.dieresult.append(random.randint(1,self.faces))
        else:
            raise DieException("roll has failed")
        
    def reset(self):
        self.dieresult = None

    def get_die_result(self):
        return self.dieresult

class DieException(Exception):
    pass