#  test for runtime  module

import unittest

import runtime
import commands
import scanner
import data

class TestRuntime(unittest.TestCase):

#  test matrix and function operations from primes.py

  def testRunExpression (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 OPTION BASE 1')
    commands.executeCommand('20 DIM PRIMES(10)')
    commands.executeCommand('30  PRIMES(1) = 2')
    commands.executeCommand('40 LET N = 5')
    commands.executeCommand('50 LET R = N - int(N / PRIMES(1)) * PRIMES(1)')    
    result = commands.executeCommand('RUN')    
    self.assertEqual(result, 'Done')    
    self.assertEqual(data.matrixList['PRIMES']['dim'], [10])
    self.assertEqual(data.variables['PRIMES'], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    self.assertEqual(data.variables['R'], 1)



if __name__ == '__main__':  
    unittest.main()
    