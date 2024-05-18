import unittest
from context import diceroller
from unittest.mock import patch

class TestRoll(unittest.TestCase):
    def test_init_roll(self):
         with self.subTest('valid instance'):   
            dice = [diceroller.Die(20), diceroller.Die(10)]
            modifiers = [1, 2, 3]
            test_roll = diceroller.Roll(dice, modifiers)
            self.assertTrue(hasattr(test_roll, "id"))
            self.assertTrue(hasattr(test_roll, "dice"))
            self.assertTrue(hasattr(test_roll, "modifiers"))
            self.assertTrue(hasattr(test_roll, 'roll_result'))
            self.assertTrue(hasattr(test_roll, 'final_value'))

         with self.subTest('invalid modifier'):   
            dice = [diceroller.Die(20), diceroller.Die(10)]
            modifiers = [1, 2, 'dog']
            self.assertRaisesRegex(diceroller.RollException, "modifier not int", diceroller.Roll, dice, modifiers)

         with self.subTest('invalid die'):   
            dice = [5, 3]
            modifiers = [1, 2, 3]
            self.assertRaisesRegex(diceroller.RollException, "die not Die", diceroller.Roll, dice, modifiers)


    def test_init_roll(self):
        with self.subTest('valid roll_result'):
            dice = [diceroller.Die(20)]
            modifiers = [1]
            test_roll = diceroller.Roll(dice, modifiers)
            test_roll.roll()
            self.assertTrue(2 <= test_roll.final_value <= 21)
