import os
import sys

##Edits system path to look into the directory above for diceroller python
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import diceroller