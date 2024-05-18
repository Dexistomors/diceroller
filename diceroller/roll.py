import uuid
from diceroller.die import Die
from diceroller.rollresult import RollResult

class Roll:

    def __init__(self, dice, modifiers=[]):
        self.id = uuid.uuid4()
        self.dice = Roll._validate_dice(dice)
        self.modifiers = Roll._validate_modifiers(modifiers)
        self.roll_result = None
        self.final_value = None

    def _validate_dice(dice):
        if type(dice) != list:
            raise RollException("dice has incorrect data format")
        for die in dice:
            Roll._validate_die(die)
        return dice

    def _validate_die(die):
        if type(die) == Die:
            return die
        else:
            raise RollException("die not Die")
        
    def _validate_modifiers(modifiers):
        if type(modifiers) != list:
            raise RollException("modifier has incorrect data")
        for modifier in modifiers:
            Roll._validate_modifier(modifier)
        return modifiers

    def _validate_modifier(modifier):
        if type(modifier) == int:
            return modifier
        else:
            raise RollException("modifier not int")

    def create_dice_from_dice_configs(self, dice_configs):
        pass

    def add_die(self, die):
        self.dice.append(Roll._validate_die(die))

    def remove_die(self, die):
        pass

    def edit_die(self, die):
        pass

    def add_modifier(self, modifier):
        self.modifiers.append(Roll._validate_modifier)

    def remove_modifier(self, modifier):
        pass

    def edit_modifier(self, modifier):
        pass

    def roll(self):
        dice_final_results = []
        dice_final_value = sum(self.modifiers)
        for die in self.dice:
            diceresult = die.roll()
            dice_final_value = dice_final_value + diceresult.get_final_value()
            dice_final_results.append(diceresult)
        self.roll_result = RollResult(dice_final_results, self.modifiers, dice_final_value)
        self.final_value = dice_final_value

    def reset(self):
        pass

    def get_roll_result(self):
        pass

    def get_final_result(self):
        pass

class RollException(Exception):
    pass