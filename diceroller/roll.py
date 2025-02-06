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
        ## 1d4 + d3

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


    ## Takes a JSON string and returns a Roll object
    def deserialize(json_config):
        try:
            try:
                roll_config = json.loads(json_config)
            except json.decoder.JSONDecodeError:
                raise RollException("Invalid JSON; could not be parsed")
            id = roll_config.get('id')
            dice = []
            for dice_config in roll_config.get('dice'):
                try:
                    die_id = dice_config.get('id')
                except ValueError:
                    raise RollException("cannot parse data from 'id'")
                try:    
                    die_faces = dice_config.get('faces')
                except ValueError:
                    raise RollException("cannot parse data from 'faces'")
                try:
                    die_advantage = dice_config.get('advantage')
                except ValueError:
                    raise RollException("cannot parse data from 'advantage'")
                try:
                    die_reroll_rules = dice_config.get('reroll_rules')
                except ValueError:
                    raise RollException("cannot parse data from 'reroll_rules'")
                dice.append(Die(die_faces, die_advantage, die_reroll_rules))
            modifiers = roll_config.get('modifiers')
        except RollException as failure:
            raise RollException("could not deserialize roll_config: %s" % failure)
        roll = Roll(dice, modifiers)
        return roll

class RollException(Exception):
    pass