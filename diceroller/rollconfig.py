import uuid

class RollConfig:

    def __init__(self, dice_configs, modifiers):
        self.id = str(uuid.uuid4())
        self.dice_configs = dice_configs
        self.modifiers = modifiers

    def create_roll(self, roll_config):
        pass

    def serialize(self):
        pass
    
    ## Takes a JSON string and returns a RollConfig object
    def deserialize(json_config):
        pass