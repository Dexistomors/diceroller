import uuid

class Roll:

    def __init__(self, dice, modifiers=[]):
        self.id = uuid.uuid4()
        self.dice = dice
        self.modifiers = modifiers
        self.roll_result = None
        self.final_value = None

    def create_dice_from_dice_configs(self, dice_configs):
        pass

    def add_die(self, die):
        pass

    def remove_die(self, die):
        pass

    def edit_die(self, die):
        pass

    def add_modifier(self, modifier):
        pass

    def remove_modifier(self, modifier):
        pass

    def edit_modifier(self, modifier):
        pass

    def roll(self):
        pass

    def reset(self):
        pass

    def get_roll_result(self):
        pass

    def get_final_result(self):
        pass