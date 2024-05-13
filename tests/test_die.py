import unittest
from context import diceroller

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