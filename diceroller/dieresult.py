class DieResult:
    #my_dice_roll_result=DieResult(some_roll_values, the_final_result)
    def __init__(self, id, roll_values, final_value):
        self.id = id
        self.roll_values = roll_values
        self.final_value = final_value
        self._validate_roll_values()
        self._validate_final_value()

    def get_roll_values(self):
        return self.roll_values
        
    def get_final_value(self):
        return self.final_value
    
    ##_validate_id(self):

    def _validate_final_value(self):
        if type(self.final_value) != int:
            raise DieResultException("final_value is not int")
        if self.final_value not in self.roll_values:
            raise DieResultException("final_value not in roll_values")
        
    def _validate_roll_values(self):
        if type(self.roll_values) != list:
            raise DieResultException("roll_values is not dict") 
        if not all([type(value) == int for value in self.roll_values]):
            raise DieResultException("roll_values values must be integers")
    
class DieResultException(Exception):
    pass
    


