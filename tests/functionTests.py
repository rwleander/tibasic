#  test for functions

import unittest

import expressions
import functions
import data

class TestFunctions(unittest.TestCase):

# test square root

  def testSqr (self):
    [value, msg] = expressions.evaluate('SQR(4)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)


if __name__ == '__main__':  
    unittest.main()
    