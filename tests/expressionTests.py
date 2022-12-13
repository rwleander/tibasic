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
    self.assertEqual(tree[0], {'parts': ['3.1416', '*', 'R', '^', '2'], 'value': 0,'id': 0,  'parent': -1})
   
  def testCreateTree2 (self):
    [parts, msg] = expressions.splitLine('3 * ( 2 + 3)')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 3)
    self.assertEqual(tree[0], {'parts': ['3', '*', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'parts': ['2', '+', '3'], 'value': 0, 'id': 1, 'parent': 0})
   
  def testCreateTree3 (self):
    [parts, msg] = expressions.splitLine('(1 + 2) / (3 * 4)')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'parts': ['~1', '/', '~2'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'parts': ['1', '+', '2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'parts': ['3', '*', '4'], 'value': 0, 'id': 2, 'parent': 0})

   
  def testCreateTree4 (self):
    [parts, msg] = expressions.splitLine('2 * (3 / (4 + 5))')
    self.assertEqual(msg, 'OK')
    [tree, msg] = expressions.buildTree(parts)
    self.assertEqual(msg, 'OK')
    self.assertEqual(len(tree), 4)
    self.assertEqual(tree[0], {'parts': ['2', '+', '~1'], 'value': 0, 'id': 0,  'parent': -1})
    self.assertEqual(tree[1], {'parts': ['3', '/', '~2'], 'value': 0, 'id': 1, 'parent': 0})
    self.assertEqual(tree[2], {'parts': ['4', '+', '5'], 'value': 0, 'id': 2, 'parent': 1})

    
 
  
if __name__ == '__main__':  
    unittest.main()
    