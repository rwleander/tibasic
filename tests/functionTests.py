#  test for functions

import unittest
import math

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

# test arc tangent function

  def testAtn (self):
    [value, msg] = expressions.evaluate('ATN(1.0)')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , math.pi / 4)
    [value, msg] = expressions.evaluate('ATN(0.0)')
    self.assertEqual(value , 0)

#  test cosin

  def testCOS (self):
    n = math.pi / 4
    [value, msg] = expressions.evaluate('COS(' + str(n) + ')')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , (2 ** 0.5) / 2)
    [value, msg] = expressions.evaluate('COS(0.0)')
    self.assertEqual(value , 1.0)

# test sine

  def testSin (self):
    n = math.pi / 4
    [value, msg] = expressions.evaluate('SIN(' + str(n) + ')')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , (2 ** 0.5) / 2)
    [value, msg] = expressions.evaluate('SIN(0.0)')
    self.assertEqual(value , 0.0)

#  test tangent

  def testTAN (self):
    n = math.pi / 4
    [value, msg] = expressions.evaluate('TAN(' + str(n) + ')')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , 0.9999999999999999)
    [value, msg] = expressions.evaluate('TAN(0.0)')
    self.assertEqual(value , 0.0)

#  test log function

  def testLog (self):
    [value, msg] = expressions.evaluate('LOG(' + str(math.e) + ')')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , 1)
    [value, msg] = expressions.evaluate('LOG(0)')
    self.assertEqual(msg, 'Bad value')

#  test exponent function

  def testExp (self):
    [value, msg] = expressions.evaluate('EXP(1)')
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , math.e)
    [value, msg] = expressions.evaluate('EXP(0)')
    self.assertEqual(value, 1)



if __name__ == '__main__':  
    unittest.main()
    