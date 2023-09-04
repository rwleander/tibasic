#  test for expression scanner

import unittest

import data
import expressions
import commands
import scanner


class TestExpressions(unittest.TestCase):
   
   #  test create tree
   
  def testCreateTree1 (self):
    tokens = scanner.findTokens('3.1416 * R ^ 2')
    self.assertEqual(tokens, ['3.1416', '*', 'R', '^', '2'])
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 2)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['3.1416', '*', 'R', '^', '2'], 'value': 0,'id': 0,  'parent': -1})
      
  def testCreateTree2 (self):
    tokens = scanner.findTokens('3 * ( 2 + 3)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 3)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['3', '*', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['2', '+', '3'], 'value': 0, 'id': 1, 'parent': 0})
   
  def testCreateTree3 (self):
    tokens = scanner.findTokens('(1 + 2) / (3 * 4)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1', '/', '~2'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['1', '+', '2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['3', '*', '4'], 'value': 0, 'id': 2, 'parent': 0})

   
  def testCreateTree4 (self):
    tokens = scanner.findTokens('2 * (3 / (4 + 5))')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['2', '*', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'expr', 'parts': ['3', '/', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['4', '+', '5'], 'value': 0, 'id': 2, 'parent': 1})
   
  def testCreateTree5 (self):
    tokens = scanner.findTokens('4 <> 5')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 2)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['4', '<>', '5'], 'value': 0, 'id': 0,  'parent': -1})
    
  def testCreateTreeFail (self):
    tokens = scanner.findTokens('2 * (3 / (4 + 5)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'Missing )')

#  test tree with function

  def testCreateTreeWithFunction (self):
    tokens = scanner.findTokens('SQR(4)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['SQR', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['4'], 'value': 0, 'id': 2, 'parent': 1})

#  test tree with function - no parameters

  def testCreateTreeWithFunction2 (self):
    tokens = scanner.findTokens('RND()')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['RND', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': [], 'value': 0, 'id': 2, 'parent': 1})

#  test tree with function, multiple parameters

  def testCreateTreeWithFunction3 (self):
    tokens = scanner.findTokens('STR$("Hello", 2, 1)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 6)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'func', 'parts': ['STR$', '~2', '~3', '~4'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['"Hello"'], 'value': 0, 'id': 2, 'parent': 1})
    self.assertEqual(tree[3], {'type': 'expr', 'parts': ['2'], 'value': 0, 'id': 3, 'parent': 1})
    self.assertEqual(tree[4], {'type': 'expr', 'parts': ['1'], 'value': 0, 'id': 4, 'parent': 1})

#  build tree substituting user defined function

  def testCreateTreeWithUserFunction (self):
    commands.executeCommand('New')
    data.userFunctionList = {'SQUARE': {'arg': 'N', 'expr': 'N * N'}}    
    tokens = scanner.findTokens('SQUARE(4)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'type': 'udf', 'parts': ['SQUARE', '~2'], 'value': 0, 'id': 1, 'parent': 0})    
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['4'], 'value': 0, 'id': 2, 'parent': 1})    
    
#  test set variables

  def testSetVariables (self):
    parts = ['2', '+', '3']
    parts = expressions.setVariables(parts, {})
    self.assertEqual(parts, [2, '+', 3])

#  test entire function

  def testEvaluate (self):
    tokens = scanner.findTokens('2 + 3')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 5)

  def testEvaluate2 (self):
    tokens = scanner.findTokens('2 + 3 * 4')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 14)

  def testEvaluate3 (self):
    tokens = scanner.findTokens('2 + 3 / 4')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 2.75)

  def testEvaluate4 (self):
    tokens = scanner.findTokens('2 * (1 + 2) ^ 2') 
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 18)

  def testEvaluate5 (self):
    tokens = scanner.findTokens('(1 + 2) ^ 2 - (2 * 3)') 
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 3)

  def testEvaluate6 (self):
    tokens = scanner.findTokens('-1')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, -1)

  def testEvaluate7 (self):
    tokens = scanner.findTokens('2 = (3 - 1)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, True)

  def testEvaluate8 (self):
    data.variables = {}
    [value, msg] = expressions.evaluate(['Z'])
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 0)
    
  def testEvaluate9 (self):
    tokens = scanner.findTokens('3 * -5 + 1')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, -14)

  def testEvaluate10 (self):
    tokens = scanner.findTokens('4 <> 4')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, False)

  def testEvaluate11 (self):
    tokens = scanner.findTokens('4 <> 5')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, True)

    #  test problem from primes.bas example
    
  def testEvaluate12 (self):
    data.variables = {'R': 5 % 2}    
    self.assertEqual(data.variables['R'], 1)
    tokens = scanner.findTokens('R > 0')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, True)
    

    #   test bad expressions
    
  def testEvaluateBad (self):
    tokens = scanner.findTokens('5 + * 4')
    self.assertEqual(tokens, ['5', '+', '*', '4'])
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'Bad expression')

# test bug with if statement
    
  def testEvaluateBadIf (self):
    tokens = scanner.findTokens('INT(RND() * 100) + 1')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value > 0, True)
    self.assertEqual(value < 101, True)
    
    #  test matrix expression
       
  def testCreateTreeMatrix (self):
    data.matrixList = {'A': {'x': 5, 'y': 0, 'z': 0}}
    data.variables['A'] = [1, 2, 3, 4, 5]    
    tokens = scanner.findTokens('A(3)')
    [tree, msg] = expressions.buildTree(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'type': 'expr', 'parts': ['~1'], 'value': 0,'id': 0, 'parent': -1})
    self.assertEqual(tree[1], {'type': 'mat', 'parts': ['A', '~2'], 'value': 0,'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'type': 'expr', 'parts': ['3'], 'value': 0,'id': 2, 'parent': 1})
       
  def testEvaluateMatrix2 (self):
    data.matrixList = {'A': {'name': 'A', 'dim': [5]}}
    data.variables['A'] = [1, 2, 3, 4, 5]    
    data.matrixBase = 0
    tokens = scanner.findTokens('A(3)')
    [value, msg] = expressions.evaluate(tokens)
    self.assertEqual(msg, 'OK')
    self.assertEqual(value, 4)
  
if __name__ == '__main__':  
    unittest.main()
    