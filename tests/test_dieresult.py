import unittest
from context import diceroller

class TestDieResult(unittest.TestCase):
    def test_init_dieresult(self):
        with self.subTest('valid instance'):
            id = '123'
            roll_values = [6, 3, 1]
            final_value = 6
            #Initializing an instance of the DieResult class
            test_dieresult = diceroller.DieResult(id, roll_values, final_value)
            self.assertTrue(hasattr(test_dieresult, "roll_values"))
            self.assertTrue(hasattr(test_dieresult, "final_value"))

        with self.subTest('invalid roll_values'):
            roll_values = ['dog', 3, 1]
            final_value = 6
            self.assertRaisesRegex(diceroller.DieResultException, "roll_values values must be integers", diceroller.DieResult, id, roll_values, final_value)

        with self.subTest('invalid final_value'):
            roll_values = [6, 3, 1]
            final_value = 2
            self.assertRaisesRegex(diceroller.DieResultException, "final_value not in roll_values", diceroller.DieResult, id, roll_values, final_value)

    def test_get_roll_values(self):
        id = '123'
        roll_values = [6, 3, 1]
        final_value = 6
        test_dieresult = diceroller.DieResult(id, roll_values, final_value)
        self.assertEqual(roll_values, test_dieresult.get_roll_values())

    def test_get_final_values(self):
        id = '123'
        roll_values = [6, 3, 1]
        final_value = 6
        test_dieresult = diceroller.DieResult(id, roll_values, final_value)
        self.assertEqual(final_value, test_dieresult.get_final_value())

