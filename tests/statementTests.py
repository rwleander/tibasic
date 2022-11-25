#  test for statemens functions

import unittest

import commands
import statements
import data

class TestStatements(unittest.TestCase):

# test let command

  def testLet (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 1')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.variables), 2)
    self.assertEqual(data.variables['A'], 1)

  def testLetWithVariable (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 1')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('LET B = A')
    self.assertEqual(len(data.variables), 3)
    self.assertEqual(data.variables['B'], 1)
    
    

 
  
if __name__ == '__main__':  
    unittest.main()
    