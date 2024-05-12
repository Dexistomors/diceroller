import unittest
from context import diceroller

class TestDieResult(unittest.TestCase):
    def test_init_dieresult(self):
        with self.subTest('valid instance'):
            roll_values = {
                'test_uuid1' : 6,
                'test_uuid2' : 3,
                'test_uuid3' : 1,
            }
            final_value = 6
            test_dieresult = diceroller.DieResult(roll_values, final_value)
            self.assertTrue(hasattr(test_dieresult, "roll_values"))
            self.assertTrue(hasattr(test_dieresult, "final_value"))

        with self.subTest('invalid roll_values'):
            roll_values = {
                'test_uuid1' : 'dog',
                'test_uuid2' : 3,
                'test_uuid3' : 1,
            }
            final_value = 6
            self.assertRaisesRegex(diceroller.DieResultException, "roll_values values must be integers", diceroller.DieResult, roll_values, final_value)

        with self.subTest('invalid final_value'):
            roll_values = {
                'test_uuid1' : 6,
                'test_uuid2' : 3,
                'test_uuid3' : 1,
            }
            final_value = 2
            self.assertRaisesRegex(diceroller.DieResultException, "final_value not in roll_values", diceroller.DieResult, roll_values, final_value)

    def test_get_roll_values(self):
        roll_values = {
                'test_uuid1' : 6,
                'test_uuid2' : 3,
                'test_uuid3' : 1,
            }
        final_value = 6
        test_dieresult = diceroller.DieResult(roll_values, final_value)
        self.assertEqual(roll_values, test_dieresult.get_roll_values())

    def test_get_final_values(self):
        roll_values = {
                'test_uuid1' : 6,
                'test_uuid2' : 3,
                'test_uuid3' : 1,
            }
        final_value = 6
        test_dieresult = diceroller.DieResult(roll_values, final_value)
        self.assertEqual(final_value, test_dieresult.get_final_value())

