#  test for expression parser

import unittest

import data
import expressions

class TestExpressions(unittest.TestCase):

# test split parts 

  def testSplitLine1 (self):
    [parts, msg] = expressions.splitLine('1')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['1'])

  def testSplitLine2 (self):
    [parts, msg] = expressions.splitLine('A + B')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['A', '+', 'B'])

  def testSplitLine3 (self):
    [parts, msg] = expressions.splitLine('(THIS + THAT) / 10')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['(', 'THIS', '+', 'THAT', ')', '/', '10'])

  def testSplitLine5 (self):
    [parts, msg] = expressions.splitLine('"We three kings " & of orient are..."')
    self.assertEqual(msg, 'Missing quote')

  def testSplitLine6 (self):
    [parts, msg] = expressions.splitLine('3.1416 * R ^ 2')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['3.1416', '*', 'R', '^', '2'])

  def testSplitLine4 (self):
    [parts, msg] = expressions.splitLine('"We three kings " & "of orient are..."')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['"We three kings "', '&', '"of orient are..."'])
   

   
   #  test create tree
   
  def testCreateTree1 (self):
    [parts, msg] = expressions.splitLine('3.1416 * R ^ 2')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['3.1416', '*', 'R', '^', '2'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 2)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['3.1416', '*', 'R', '^', '2'], 'value': 0,'id': 0,  'parent': -1})
   
  def testCreateTree2 (self):
    [parts, msg] = expressions.splitLine('3 * ( 2 + 3)')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 3)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['3', '*', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['2', '+', '3'], 'value': 0, 'id': 1, 'parent': 0})
   
  def testCreateTree3 (self):
    [parts, msg] = expressions.splitLine('(1 + 2) / (3 * 4)')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1', '/', '~2'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['1', '+', '2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['3', '*', '4'], 'value': 0, 'id': 2, 'parent': 0})

   
  def testCreateTree4 (self):
    [parts, msg] = expressions.splitLine('2 * (3 / (4 + 5))')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['2', '*', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['3', '/', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['4', '+', '5'], 'value': 0, 'id': 2, 'parent': 1})
   
  def testCreateTree5 (self):
    [parts, msg] = expressions.splitLine('4 <> 5')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['4', '<>', '5'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 2)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['4', '<>', '5'], 'value': 0, 'id': 0,  'parent': -1})
    
  def testCreateTreeFail (self):
    [parts, msg] = expressions.splitLine('2 * (3 / (4 + 5)')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'Missing )')

#  test tree with function

  def testCreateTreeWithFunction (self):
    [parts, msg] = expressions.splitLine('SQR(4)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(parts), 4)
    self.assertEqual(parts, ['SQR', '(', '4', ')'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['SQR', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['4'], 'value': 0, 'id': 2, 'parent': 1})

#  test tree with function - no parameters

  def testCreateTreeWithFunction2 (self):
    [parts, msg] = expressions.splitLine('RND()')
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(parts), 3)
    self.assertEqual(parts, ['RND', '(', ')'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['RND', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': [], 'value': 0, 'id': 2, 'parent': 1})

#  test tree with function, multiple parameters

  def testCreateTreeWithFunction2 (self):
    [parts, msg] = expressions.splitLine('STR$("Hello", 2, 1)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(parts), 8)
    self.assertEqual(parts, ['STR$', '(', '"Hello"', ',', '2', ',', '1', ')'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 6)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['STR$', '~2', '~3', '~4'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['"Hello"'], 'value': 0, 'id': 2, 'parent': 1})
    self.assertEqual(tree[3], {'type': 'expr', 'parts': ['2'], 'value': 0, 'id': 3, 'parent': 1})
    self.assertEqual(tree[4], {'type': 'expr', 'parts': ['1'], 'value': 0, 'id': 4, 'parent': 1})

#  test set variables

  def testSetVariables (self):
    parts = ['2', '+', '3']
    parts = expressions.setVariables(parts, {})
    self.assertEqual(parts, [2, '+', 3])

#  test entire function

  def testEvaluate (self):
    [value, msg] = expressions.evaluate('2 + 3')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 5)

  def testEvaluate2 (self):
    [value, msg] = expressions.evaluate('2 + 3 * 4')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 14)

  def testEvaluate3 (self):
    [value, msg] = expressions.evaluate('2 + 3 / 4')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 2.75)

  def testEvaluate4 (self):
    [value, msg] = expressions.evaluate('2 * (1 + 2) ^ 2') 
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 18)

  def testEvaluate5 (self):
    [value, msg] = expressions.evaluate('(1 + 2) ^ 2 - (2 * 3)') 
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 3)

  def testEvaluate6 (self):
    [value, msg] = expressions.evaluate('-1')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, -1)

  def testEvaluate7 (self):
    [value, msg] = expressions.evaluate('2 = (3 - 1)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, True)

  def testEvaluate8 (self):
    data.variables = {}
    [value, msg] = expressions.evaluate('Z')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 0)
    

  def testEvaluate9 (self):
    [value, msg] = expressions.evaluate('3 * -5 + 1')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, -14)

  def testEvaluate10 (self):
    [value, msg] = expressions.evaluate('4 <> 4')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, False)


  def testEvaluate11 (self):
    [value, msg] = expressions.evaluate('4 <> 5')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, True)
    
    
    
    #   test bad expressions
    
  def testEvaluateBad (self):
    [value, msg] = expressions.evaluate('5 + * 4')
    self.assertEqual(msg, 'Bad expression')

# test bug with if statement
    
  def testEvaluateBadIf (self):
    [value, msg] = expressions.evaluate('INT(RND() * 100) + 1')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value > 0, True)
    self.assertEqual(value < 101, True)
    
    #  test matrix expression
       
  def testCreateTreeMatrix (self):
    data.matrixList = {'A': {'x': 5, 'y': 0, 'z': 0}}
    data.variables['A'] = [1, 2, 3, 4, 5]    
    [parts, msg] = expressions.splitLine('A(3)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(parts, ['A', '(', '3', ')'])
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0,'id': 0, 'parent': -1})
    self.assertEqual(tree[1], {'type': 'mat', 'parts': ['A', '~2'], 'value': 0,'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['3'], 'value': 0,'id': 2, 'parent': 1})
       
  def testEvaluateMatrix (self):
    data.matrixList = {'A': {'x': 5, 'y': 0, 'z': 0}}
    data.variables['A'] = [1, 2, 3, 4, 5]    
    [value, msg] = expressions.evaluate('A(3)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 4)




  
if __name__ == '__main__':  
    unittest.main()
    