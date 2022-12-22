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

  def testSqr2 (self):
    [value, msg] = expressions.evaluate(' 2 * SQR(2 * 2) + 2')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 6)

#  test absolute value function

  def testAbs (self):
    [value, msg] = expressions.evaluate('ABS(2)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)
    [value, msg] = expressions.evaluate('ABS(-2)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)

#  test int function

  def testInt (self):
    [value, msg] = expressions.evaluate('INT(3.1415)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 3)
    [value, msg] = expressions.evaluate('INT(-2.5)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , -3)

# test sgn function

  def testSgn (self):
    [value, msg] = expressions.evaluate('SGN(3.1415)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 1)
    [value, msg] = expressions.evaluate('SGN(0)')
    self.assertEqual(value , -0)
    [value, msg] = expressions.evaluate('SGN(-3)')
    self.assertEqual(value , -1)


if __name__ == '__main__':  
    unittest.main()
    