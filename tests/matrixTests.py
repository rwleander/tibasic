#  test for matrix  module

import unittest

import matrix
import data

class TestMatrix(unittest.TestCase):

#  test option base

  def testOption (self):
    data.matrixList = {}
    data.matrixBase = 0
    result = matrix.setOption(1)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.matrixBase, 1)

  def testOption2 (self):
    data.matrixList = {'A': {'x': 5}}
    data.matrixBase = 0
    result = matrix.setOption(2)
    self.assertEqual(result, 'Incorrect statement')

  def testOption3 (self):
    data.matrixList = {'A': {'x': 5}}
    data.matrixBase = 0
    result = matrix.setOption(1)
    self.assertEqual(result, 'Option must be before dim')

#  test new variable method

  def testNewVariable (self):
    data.matrixList = {}
    data.matrixBase = 0
    result = matrix.newVariable('A', 10, 0, 0) 
    self.assertEqual(result, 'OK')


#  test parse matrix

  def testparseMatrix (self):
    [var, x, y, z, msg] = matrix.parseVariable('A(10)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(var, 'A')
    self.assertEqual(x, '10')
    self.assertEqual(y, '')
    self.assertEqual(z, '')

  def testParseMatrix2 (self):
    [var, x, y, z, msg] = matrix.parseVariable('A(10, 5, 3)')
    self.assertEqual(msg, 'OK')
    self.assertEqual(var, 'A')
    self.assertEqual(x, '10')
    self.assertEqual(y, '5')
    self.assertEqual(z, '3')

#  set an item in a variable

  def testSetVariable (self):
    data.variables ['A'] = [0, 0, 0, 0, 0, 0]
    data.matrixList['A'] = {'x': 5, 'y': 0, 'z': 0}
    result = matrix.setVariable('A(3)', 12)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], [0, 0, 0, 13, 0, 0])


#  test calculate index

  def testSetVariable (self):
    data.variables ['A'] = [0, 0, 0, 0, 0, 0]
    data.matrixList['A'] = {'x': 5, 'y': 0, 'z': 0}
    [i, msg] = matrix.calculateIndex('A', 4, 0, 0)
    self.assertEqual(msg, 'OK')
    self.assertEqual(i, 4)
    
    

if __name__ == '__main__':  
    unittest.main()
    