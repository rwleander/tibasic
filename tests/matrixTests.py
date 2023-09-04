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
    data.matrixList = {'A': {'dimensions': [5, 5], 'n': 25}}
    data.matrixBase = 0
    result = matrix.setOption(1)
    self.assertEqual(result, 'Option must be before dim')

#  test new variable method

  def testNewVariable (self):
    data.matrixList = {}
    data.matrixBase = 0
    result = matrix.newVariable('A', [10])
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.matrixList), 1)
    matrixItem = data.matrixList['A']
    self.assertEqual(matrixItem['dim'], [10])
    self.assertEqual(matrixItem['len'], 10)
    self.assertEqual(len(data.variables['A']), 10)

    #  test save variable
    
  def testSaveVariable (self):
    data.matrixList = {}
    data.variables = {}
    data.matrixBase = 0
    result = matrix.newVariable('A', [10])
    self.assertEqual(result, 'OK')
    result = matrix.saveVariable(['A', '(', '3', ')'], 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'][3], 10)
    #  test save variable with three dimensions
        
  def testSaveVariable2 (self):
    data.matrixList = {}
    data.variables = {}
    data.matrixBase = 0
    result = matrix.newVariable('A', [3, 3, 3])
    self.assertEqual(result, 'OK')
    result = matrix.saveVariable(['A', '(', '1', ',', '1', ',', '1', ')'], 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'][13], 10)
    
    #  test save variable with subscripts
    
  def testSaveVariable3 (self):
    data.matrixList = {}
    data.variables = {'i': 1, 'j': 1}
    data.matrixBase = 0
    result = matrix.newVariable('A', [3, 3])
    self.assertEqual(result, 'OK')
    result = matrix.saveVariable(['A', '(', 'i', ',', 'j', ')'], 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'][4], 10)
    
#  test evaluate function
    
    
  def testEvaluate (self):
    data.matrixList = {}
    data.variables = {}
    data.matrixBase = 0
    result = matrix.newVariable('A', [5])
    self.assertEqual(result, 'OK')
    data.variables['A'] = [1, 2, 3, 4, 5]
    [n, msg] = matrix.evaluate(['A', 3])
    self.assertEqual(msg, 'OK')
    self.assertEqual(n, 4)
        
#  test calculate index

  def testCalcIndex (self):
    data.matrixBase = 0    
    i = matrix.calcIndex([3, 3], [1, 2])
    self.assertEqual (i, 5)
    i = matrix.calcIndex([2, 3, 4], [1, 2, 3])
    self.assertEqual(i, 23)     
    data.matrixBase = 1        
    i = matrix.calcIndex([3, 3], [1, 2])
    self.assertEqual (i, 1)
    i = matrix.calcIndex([2, 3, 4], [1, 2, 3])
    self.assertEqual(i, 6)     
    data.matrixBase = 0
    i = matrix.calcIndex([3, 3, 3], [1, 2, 3])
    self.assertEqual(i, -1)
    i = matrix.calcIndex([3, 3, 3], [1, 2])
    self.assertEqual(i, -1)

#  test calc subscripts function

  def testCalcSubscripts (self):
    data.variables = {'I': 1, 'J': 2}
    [values, msg] = matrix.calcSubscripts(['I', ',', 'J'])
    self.assertEqual(msg, 'OK')
    self.assertEqual(values, [1, 2])
    

    
    

if __name__ == '__main__':  
    unittest.main()
    