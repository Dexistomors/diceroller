import json
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

    def add_modifier(self, modifier):
        self.modifiers.append(Roll._validate_modifier)

    def roll(self):
        dice_results = []
        dice_final_value = sum(self.modifiers)
        for die in self.dice:
            diceresult = die.roll()
            dice_final_value = dice_final_value + diceresult.get_final_value()
            dice_results.append(diceresult)
        self.roll_result = RollResult(dice_results, self.modifiers, dice_final_value)
        self.final_value = dice_final_value
        return self.roll_result

    def reset(self):
        self.roll_result = None
        self.final_value = None

    def get_roll_result(self):
        return self.roll_result

    def get_final_value(self):
        return self.final_value
    
    ## Takes a JSON string and returns a Roll object
    def deserialize(json_config):
        try:
            roll_config = json.loads(json_config)
            id = roll_config.get('id')
            dice = []
            for dice_config in roll_config.get('dice'):
                die_id = dice_config.get('id')
                die_faces = dice_config.get('faces')
                die_advantage = dice_config.get('advantage')
                die_reroll_rules = dice_config.get('reroll_rules')
                dice.append(Die(die_faces, die_advantage, die_reroll_rules))
            modifiers = roll_config.get('modifiers')
        except:
            raise RollException("could not deserialize roll_config {}".format(json_config))
        roll = Roll(dice, modifiers)
        return roll

class RollException(Exception):
    pass