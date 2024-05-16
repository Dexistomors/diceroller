from diceroller.dieresult import DieResult
from diceroller.rerollrule import RerollRule
import uuid
import random

class Die:

    def __init__(self, faces, advantage = 0, reroll_rules = []):
        self.faces = Die._validate_faces(faces)
        self.advantage = Die._validate_advantage(advantage)
        self.reroll_rules = Die._validate_reroll_rules(reroll_rules)
        self.dieresult = None

    def set_faces(self, faces):
        if Die._validate_faces(self):
            self.faces = faces

    def set_advantage(self, advantage):
        if Die._validate_advantage(self):
            self.advantage = advantage

    def set_reroll_rules(self, reroll_rules):
        if Die._validate_reroll_rules(reroll_rules):
            self.reroll_rules = reroll_rules

    def _validate_faces(faces):
        if type(faces) == int:
            return faces
        else:
            raise DieException("faces has incorrect data type")

    def _validate_advantage(advantage):
        if type(advantage) == int and (-1 <= advantage <= 1):
            return advantage
        else:
            raise DieException("advantage has incorrect data type")

    def _validate_reroll_rules(reroll_rules):
        if type(reroll_rules) != list:
            raise DieException("reroll_rules has incorrect data format")
        for reroll_rule in reroll_rules:
            Die._validate_reroll_rule(reroll_rule)
        return reroll_rules

    def _validate_reroll_rule(reroll_rule):
        if type (reroll_rule) == RerollRule:
            return reroll_rule
        else:
            raise DieException("reroll_rule not RerollRule")
        
    def add_reroll_rule(self, reroll_rule):
        if Die._validate_reroll_rule(reroll_rule):
            self.reroll_rules.append(reroll_rule)            

    def remove_reroll_rule(self, reroll_rule):
        pass

    def _rolladv(self):        
        if type(self.faces) == int:
            roll1 = random.randint(1, self.faces)
            roll2 = random.randint(1, self.faces)
            roll_values = [roll1, roll2]
            final_value = max(roll1, roll2)
            self.dieresult = DieResult(roll_values, final_value)

    def _rolldis(self):
        if type(self.faces) == int:
            roll1 = random.randint(1, self.faces)
            roll2 = random.randint(1, self.faces)
            roll_values = [roll1, roll2]
            final_value = min(roll1, roll2)
            self.dieresult = DieResult(roll_values, final_value)

    def _roll(self):
        if type(self.faces) == int:
            self.dieresult.append(random.randint(1,self.faces))

    def roll2(self):
        if self.dieresult is None:
            self.dieresult = []
        if self.advantage == 1:
            self._rolladv()
        elif self.advantage == 0:
            self._roll()
        elif self.advantage == -1:
            self._rolldis()
        else:          
            raise DieException("advantage has unexpected variable")


# add into function, private functions above to call in advantage
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