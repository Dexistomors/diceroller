import unittest
from context import diceroller
from unittest.mock import patch

class TestDie(unittest.TestCase):
    def test_init_die(self):
        with self.subTest('valid instance'):
            faces = 20
            test_die = diceroller.Die(faces)
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
            test_die.roll()
            self.assertEqual([1], test_die.get_die_result())
            test_die.roll()
            self.assertEqual([1, 1], test_die.get_die_result())
            test_die.reset()
            self.assertEqual(None, test_die.get_die_result())
            
        with patch('random.randint', randint_max), \
            self.subTest("correct maximum roll and reset"):
            faces = 20
            test_die = diceroller.Die(faces)
            test_die.roll()
            self.assertEqual([20], test_die.get_die_result())
            test_die.roll()
            self.assertEqual([20, 20], test_die.get_die_result())
            test_die.reset()
            self.assertEqual(None, test_die.get_die_result())