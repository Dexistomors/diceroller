import uuid

class RollResult:

    def __init__(self, dice_results, modifiers, total):
        self.id = uuid.uuid4()
        self.dice_results = dice_results
        self.modifiers = modifiers
        self.total = total
        
    ##Takes a RollResult object and returns a JSON string representing RollResult
    def serialize():
        pass
