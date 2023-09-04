#  test for functions

import unittest
import math

import expressions
import functions
import scanner
import data

class TestFunctions(unittest.TestCase):

# test square root

  def testSqr (self):
    tokens = scanner.findTokens('SQR(4)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)

  def testSqr2 (self):
    tokens = scanner.findTokens('2 * SQR(2 * 2) + 2')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 6)

#  test absolute value function

  def testAbs (self):
    tokens = scanner.findTokens('ABS(2)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)
    tokens = scanner.findTokens('ABS(-2)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 2)

#  test int function

  def testInt (self):
    tokens = scanner.findTokens('INT(3.1415)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 3)
    tokens = scanner.findTokens('INT(-2.5)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , -3)

# test sgn function

  def testSgn (self):
    tokens = scanner.findTokens('SGN(3.1415)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value , 1)
    tokens = scanner.findTokens('SGN(0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , -0)
    tokens = scanner.findTokens('SGN(-3)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , -1)

# test arc tangent function

  def testAtn (self):
    tokens = scanner.findTokens('ATN(1.0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , math.pi / 4)
    tokens = scanner.findTokens('ATN(0.0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , 0)

#  test cosin

  def testCOS (self):
    n = math.pi / 4
    tokens = scanner.findTokens('COS(' + str(n) + ')')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , (2 ** 0.5) / 2)
    tokens = scanner.findTokens('COS(0.0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , 1.0)

# test sine

  def testSin (self):
    n = math.pi / 4
    tokens = scanner.findTokens('SIN(' + str(n) + ')')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , (2 ** 0.5) / 2)
    tokens = scanner.findTokens('SIN(0.0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , 0.0)

#  test tangent

  def testTAN (self):
    n = math.pi / 4
    tokens = scanner.findTokens('TAN(' + str(n) + ')')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , 0.9999999999999999)
    tokens = scanner.findTokens('TAN(0.0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value , 0.0)

#  test log function

  def testLog (self):
    tokens = scanner.findTokens('LOG(' + str(math.e) + ')')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , 1)
    tokens = scanner.findTokens('LOG(0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'Bad value')

#  test exponent function

  def testExp (self):
    tokens = scanner.findTokens('EXP(1)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value , math.e)
    tokens = scanner.findTokens('EXP(0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 1)

# test random function

  def testRnd (self):
    tokens = scanner.findTokens('RND()')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value >= 0, True)
    self.assertEqual(value < 1, True)

#  test ascii function

  def testAsc (self):
    tokens = scanner.findTokens('ASC("A")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 65)

#  test chr$ function

  def testChr (self):
    tokens = scanner.findTokens('CHR$(65)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, '"A"')

#  string length function


  def testLen (self):
    tokens = scanner.findTokens('LEN("Hello world")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 11)

#  test str function

  def testStr (self):
    tokens = scanner.findTokens('STR$(123.45)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, '"123.45"')
    tokens= scanner.findTokens('STR$(-12)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, '"-12"')
    tokens= scanner.findTokens('STR$(0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, '"0"')

#  test value function

  def testVal (self):
    tokens = scanner.findTokens('VAL("123.45")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 123.45)
    tokens = scanner.findTokens('VAL("-12")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, -12)
    tokens = scanner.findTokens('VAL("abcd")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'Bad value')

#  test segment function

  def testSeg (self):
    tokens = scanner.findTokens('SEG$("1234567890", 3)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, '"3"')
    tokens = scanner.findTokens('SEG$("1234567890", 3, 4)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, '"3456"')
    tokens = scanner.findTokens('SEG$("1234567890", 6, 10)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, '"67890"')
    tokens = scanner.findTokens('SEG$("1234567890", 0)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'Bad value')
    tokens = scanner.findTokens('SEG$("1234567890", 3, -1)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'Bad value')

#  test position function

  def testPos (self):
    tokens = scanner.findTokens('POS("ABCDEFG", "C")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 3)
    tokens = scanner.findTokens('POS("ABCDEFGABCDEFG", "C", 7)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 10)
    tokens = scanner.findTokens('POS("ABCDEFG", "DEF")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 4)
    tokens = scanner.findTokens('POS("ABCDEFG", "XYZ")')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 0)

#  test tab function

  def testTab (self):
    tokens = scanner.findTokens('TAB(2)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, '"  "')
    tokens = scanner.findTokens('TAB(5)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, '"     "')

    #  test min function
    
  def testMin (self):
    tokens = scanner.findTokens('MIN(5, 3)')
    self.assertEqual(tokens[0], 'MIN')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 3)    
    tokens = scanner.findTokens('MIN (2, 8)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 2)    
    tokens = scanner.findTokens('MIN (8, 8)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 8)
    
    #  test max function
    
  def testMax (self):
    tokens = scanner.findTokens('MAX(5, 3)')
    self.assertEqual(tokens[0], 'MAX')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')    
    self.assertEqual(value, 5)    
    tokens = scanner.findTokens('MAX (2, 8)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 8)    
    tokens = scanner.findTokens('MAX (8, 8)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(value, 8)
    
    #  test pi function
        
  def testPi (self):
    tokens = scanner.findTokens('PI()')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')        
    self.assertEqual(int(value * 10000), 31415)

#  test rpt$ function

  def testRpt (self):
    tokens = scanner.findTokens('RPT$("Hello", 3)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')        
    self.assertEqual(value, '"HelloHelloHello"')

    
    
if __name__ == '__main__':  
    unittest.main()
    