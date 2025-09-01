import json
import uuid
from diceroller.die import Die
from diceroller.rollresult import RollResult

class Roll:

    def __init__(self, dice, modifiers=[]):
        self.id = str(uuid.uuid4())
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

    def add_die(self, die):
        self.dice.append(Roll._validate_die(die))

    def add_modifier(self, modifier):
        self.modifiers.append(Roll._validate_modifier)

    def roll(self):
        dice_results = []
        dice_final_value = sum(self.modifiers)
        for die in self.dice:
            diceresult = die.roll()
            dice_final_value = dice_final_value + diceresult.get_final_value()
            dice_results.append(diceresult)
        self.roll_result = RollResult(self.id, dice_results, self.modifiers, dice_final_value)
        self.final_value = dice_final_value
        return self.roll_result

    def reset(self):
        self.roll_result = None
        self.final_value = None

    def get_roll_result(self):
        return self.roll_result

    def get_final_value(self):
        return self.final_value
    
    def prettify(self):
        tmp = {}
        for die in self.dice:
            key = str(die.faces) + 'a' + str(die.advantage)
            if key not in tmp:
                tmp[key] = 1
            else:
                tmp[key] = tmp[key] + 1

        finalstring = ''
        delim = ' + '

        for key in tmp:
            count = tmp[key]
            faces = key.split('a')[0]
            advantage = key.split('a')[1]

            if advantage == '1':
                string_rep = 'adv({}d{})'.format(count, faces)
            elif advantage == '-1':
                string_rep = 'dis({}d{})'.format(count, faces)
            else:
                string_rep = '{}d{}'.format(count, faces)

            if not finalstring:
                finalstring = string_rep
            else:
                finalstring = finalstring + delim + string_rep
        if self.modifiers:
            finalstring = finalstring + delim + delim.join([str(x) for x in self.modifiers])

        return finalstring


class RollException(Exception):
    pass