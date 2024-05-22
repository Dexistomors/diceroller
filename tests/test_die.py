import unittest
from context import diceroller
from unittest.mock import patch

class TestDie(unittest.TestCase):
    def test_init_die(self):
        with self.subTest('valid instance'):
            faces = 20
            test_die = diceroller.Die(faces)
            self.assertTrue(hasattr(test_die, 'id'))
            self.assertTrue(hasattr(test_die, 'faces'))
            self.assertTrue(hasattr(test_die, 'advantage'))
            self.assertTrue(hasattr(test_die, 'reroll_rules'))
            self.assertTrue(hasattr(test_die, 'dieresult'))

        with self.subTest('invalid faces data'):
            faces = 'dog'
            self.assertRaisesRegex(diceroller.DieException, "faces has incorrect data type", diceroller.Die, faces)

        with self.subTest('invalid advantage data, cannot be str'):
            faces = 8
            advantage = 'dog'
            self.assertRaisesRegex(diceroller.DieException, "advantage has incorrect data type", diceroller.Die, faces, advantage)

        with self.subTest('invalid advantage data, outside of expected int'):
            faces = 8
            advantage = 4
            self.assertRaisesRegex(diceroller.DieException,"advantage has incorrect data type", diceroller.Die, faces, advantage)

        with self.subTest('incorrect reroll_rules format'):
            faces = 8
            advantage = 0
            reroll_rules = {}
            self.assertRaisesRegex(diceroller.DieException, "reroll_rules has incorrect data format")
        
        def randint_min(min, max):
            return min
        def randint_max(min, max):
            return max
        
        with patch('random.randint', randint_min), \
            self.subTest("correct minimum roll and reset"):
            faces = 20
            test_die = diceroller.Die(faces)
            test_results = test_die.roll()
            self.assertEqual([1], test_results.get_roll_values())
            test_die.roll()
            self.assertEqual([1], test_results.get_roll_values())
            test_die.reset()
            test_results = test_die.get_die_result()
            self.assertIsNone(test_results)
        
        with patch('random.randint', randint_max), \
            self.subTest("correct maximum roll and reset"):
            faces = 20
            test_die = diceroller.Die(faces)
            test_results = test_die.roll()
            self.assertEqual([20], test_results.get_roll_values())
            test_die.set_advantage(1)
            test_results = test_die.roll()
            self.assertEqual([20, 20], test_results.get_roll_values())
            test_die.reset()
            test_die.set_advantage(0)
            test_results = test_die.roll()
            self.assertEqual([20], test_results.get_roll_values())

        with patch('random.randint', randint_min), \
            self.subTest("correct disadvantage roll and reset"):
            faces = 20
            advantage = -1
            test_die = diceroller.Die(faces, advantage)
            test_results = test_die.roll()
            self.assertEqual([1, 1], test_results.get_roll_values())
            self.assertEqual(1, test_results.get_final_value())
            test_die.reset()
            test_results = test_die.get_die_result()
            self.assertIsNone(test_results)
            test_results = test_die.roll()
            self.assertEqual(1, test_results.get_final_value())