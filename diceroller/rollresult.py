import uuid

class RollResult:

    def __init__(self, dice_results, modifiers = []):
        self.id = uuid.uuid4()
        self.dice_results = dice_results
        self.modifiers = modifiers
        self.total = None

    def serialize(self):
        pass

    def deserialize(self):
        pass