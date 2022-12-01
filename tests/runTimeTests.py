#  test for run time methods

import unittest

import runtime
import commands
import data

class TestRuntime(unittest.TestCase):

# test run with no code

  def testRunNoCode (self):
    rslt = commands.executeCommand('NEW')
    rslt = runtime.run()
    self.assertEqual(rslt, 'No code')

# run a line of code

  def testRunLet (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 1)

 
  
if __name__ == '__main__':  
    unittest.main()
    