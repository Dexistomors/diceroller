import unittest
from context import diceroller
from unittest.mock import patch
import json


valid_json = """{
   "id": "789",
   "dice": [
      {
            "id": "1234",
            "faces": 20,
            "advantage": 1,
            "reroll_rules": []
      },
      {
            "id": "5678",
            "faces": 8,
            "advantage": 0,
            "reroll_rules": []
      }
   ],
   "modifiers": [
      1,
      2,
      3,
      -4
   ]
}"""


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


   def test_roll_result(self):
      with self.subTest('valid roll_result'):
            dice = [diceroller.Die(20)]
            modifiers = [1]
            test_roll = diceroller.Roll(dice, modifiers)
            test_roll.roll()
            self.assertTrue(2 <= test_roll.final_value <= 21)

    

   def test_result_and_final_value(self):
      def randint_min(min, max):
         return min
      def randint_max(min, max):
         return max
        
      with patch('random.randint', randint_min), \
         self.subTest('valid get_roll_result and get_final_value min'):
            dice = [diceroller.Die(20, 1)]
            modifiers = [0]
            test_roll = diceroller.Roll(dice, modifiers)
            test_roll_results = test_roll.roll()
            test_dice_result = test_roll_results.dice_results[0]
            test_roll_values = test_dice_result.get_roll_values()
            test_final_value = test_dice_result.get_final_value()
            self.assertEqual([1, 1], test_roll_values)
            self.assertEqual(1, test_final_value)

      with patch('random.randint', randint_max), \
         self.subTest('valid get_roll_result and get_final_value max'):
            dice = [diceroller.Die(20), diceroller.Die(10), diceroller.Die(8)]
            modifiers = [3]
            test_roll = diceroller.Roll(dice, modifiers)
            test_roll_results = test_roll.roll()
            self.assertEqual(41, test_roll_results.total)

   def test_deserialize(self):
      def randint_max(min, max):
          return max
      with patch('random.randint', randint_max), \
         self.subTest('valid deserialize'):
         test_roll = diceroller.Roll.deserialize(valid_json)
         self.assertIsInstance(test_roll, diceroller.Roll)
         test_roll_results = test_roll.roll()
         self.assertEqual(30, test_roll_results.total)
      
   def test_serialize(self):
       def randint_max(min, max):
           return max
       with patch('random.randint', randint_max), \
         self.subTest('valid reserialization'):
           expected_dict = {"id": "823672c8-3632-40cd-af6e-3b4cdd1e38f4",
                            "dice_results": [
                              { "id": "123",
                                 "roll_values": [20, 20],
                                 "final_value": 20 },

                              { "id": "123",
                                 "roll_values": [10],
                                 "final_value": 10 }
                              ],
                              "modifiers": [2, 3],
                              "total": 35}

           dice_results = [diceroller.DieResult([20, 20], 20), diceroller.DieResult([10], 10)]
           modifiers = [2, 3]
           total = 35
           preserialized_roll_result = diceroller.RollResult(dice_results, modifiers, total)
           postserialized_roll_result = preserialized_roll_result.serialize()
           result_dict = json.loads(postserialized_roll_result)
           self.assertEqual(type(expected_dict.get('id')), type(result_dict.get('id')))
           self.assertEqual(expected_dict.get('dice_results'), result_dict.get('dice_results'))
           self.assertEqual(expected_dict.get('modifiers'), result_dict.get('modifiers'))
           self.assertEqual(expected_dict.get('total'), result_dict.get('total'))