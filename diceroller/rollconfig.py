import json
import uuid
from diceroller.die import Die
from diceroller.roll import Roll


class RollConfig:

    def __init__(self, dice_configs, modifiers):
        self.id = str(uuid.uuid4())
        self.dice_configs = dice_configs
        self.modifiers = modifiers

    def create_roll(roll_config):
        roll = Roll(roll_config.dice_configs, roll_config.modifiers)
        return roll

    def serialize(self):
        try:
            tmp_dice = []
            for die in self.dice_configs:
                tmp_die = {
                    "id": die.id,
                    "faces": die.faces,
                    "advantage": die.advantage,
                    "reroll_rules": []
                }
                tmp_dice.append(tmp_die)
            tmp_modifiers = self.modifiers
            tmp_config = {
                "id": "123",
                "dice": tmp_dice,
                "modifiers": tmp_modifiers
            }
            final_config = json.dumps(tmp_config)
            return final_config
        except:
            raise RollConfigException()
    
    ## Takes a JSON string and returns a RollConfig object
    def deserialize(json_config):
        try:
            try:
                roll_config = json.loads(json_config)
            except json.decoder.JSONDecodeError:
                raise RollConfigException("Invalid JSON; could not be parsed")
            id = roll_config.get('id')
            dice = []
            for dice_config in roll_config.get('dice'):
                try:
                    die_id = dice_config.get('id')
                except ValueError:
                    raise RollConfigException("cannot parse data from 'id'")
                try:    
                    die_faces = dice_config.get('faces')
                except ValueError:
                    raise RollConfigException("cannot parse data from 'faces'")
                try:
                    die_advantage = dice_config.get('advantage')
                except ValueError:
                    raise RollConfigException("cannot parse data from 'advantage'")
                try:
                    die_reroll_rules = dice_config.get('reroll_rules')
                except ValueError:
                    raise RollConfigException("cannot parse data from 'reroll_rules'")
                dice.append(Die(die_faces, die_advantage, die_reroll_rules))
            modifiers = roll_config.get('modifiers')
        except RollConfigException as failure:
            raise RollConfigException("could not deserialize roll_config: %s" % failure)
        #roll_config = {"dice": dice, "modifiers": modifiers}
        roll_config = RollConfig(dice, modifiers)
        return roll_config

class RollConfigException(Exception):
    pass