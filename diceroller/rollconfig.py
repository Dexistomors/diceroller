import uuid

class RollConfig:

    def __init__(self, dice_configs, modifiers):
        self.id = uuid.uuid4()
        self.dice_configs = dice_configs
        self.modifiers = modifiers

    def create_roll(self, roll_config):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass