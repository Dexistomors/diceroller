import uuid
import json

class RollResult:

    def __init__(self, dice_results, modifiers, total):
        self.id = str(uuid.uuid4())
        self.dice_results = dice_results
        self.modifiers = modifiers
        self.total = total
        ##Roll should cast roll's ID to self.id here
    ##Takes a RollResult object and returns a JSON string representing RollResult
    def serialize(self):
        try:
            roll_result = {}
            roll_result['id'] = self.id
            dice_results = []
            for die_result in self.dice_results:
                serialized_die_result = {}
                serialized_die_result['id'] = die_result.id
                serialized_die_result['roll_values'] = die_result.get_roll_values()
                serialized_die_result['final_value'] = die_result.get_final_value()
                dice_results.append(serialized_die_result)
            roll_result['dice_results'] = dice_results
            roll_result['modifiers'] = self.modifiers
            roll_result['total'] = self.total
            serialized_roll_result = json.dumps(roll_result, indent = 4)
        except:
            raise RollResultException("Could not serialize RollResult")
        return serialized_roll_result
    
class RollResultException(Exception):
    pass