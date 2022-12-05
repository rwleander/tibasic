#  low level test for parser functions

import unittest

import parser
import data

class TestParserUnits(unittest.TestCase):

# test add expression function using print statement

  def testAddExpressions (self):
    item = {'code': 'PRINT X'}
    ruleParts = ['PRINT', 'expr']    
    codeParts = ['PRINT', 'X']
    newItem = parser.addExpressions(item, ruleParts, codeParts)    
    self.assertEqual(len(newItem), 2)
    self.assertEqual(newItem, {'code': 'PRINT X', 'expr': 'X'})

# test add expressions using let statement

  def testAddExpressions2 (self):
    item = {'code': 'LET A = B + 2'}
    ruleParts = ['LET', 'var', '=', 'expr']
    codeParts = ['LET', 'A', '=','B + 2']
    newItem = parser.addExpressions(item, ruleParts, codeParts)    
    self.assertEqual(len(newItem), 3)
    self.assertEqual(newItem, {'code': 'LET A = B + 2', 'var': 'A', 'expr': 'B + 2'})

# test split code functions uisng prrint statement 

  def testSplitCode (self):
    code = '10 PRINT X'
    ruleParts = ['PRINT', 'expr']    
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 2)
    self.assertEqual(codeParts, ['PRINT', 'X'])

# test with let statement

  def testSplitCode2 (self):
    code = '10 LET A = B + 2'
    ruleParts = ['LET', 'var', '=', 'expr']    
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 4)
    self.assertEqual(codeParts, ['LET', 'A', '=', 'B + 2'])





  
if __name__ == '__main__':  
    unittest.main()
    