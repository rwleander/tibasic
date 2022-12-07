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

# test if statement

  def testRunIf (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('20 Let A = A + 1')
    rslt = commands.executeCommand('30 IF A < 11 THEN 20')
    rslt = commands.executeCommand('40 LET B = A') 
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['B'], 11)

# test goto

  def testRunGoTo (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 1')
    rslt = commands.executeCommand('20 GOTO 40')
    rslt = commands.executeCommand('30 LET A = 2')
    rslt = commands.executeCommand('40 END')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test goto with bad line number

  def testRunGoToBad (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 1')
    rslt = commands.executeCommand('20 GOTO 100')
    rslt = commands.executeCommand('30 LET A = 2')
    rslt = commands.executeCommand('40 END')
    rslt = runtime.run()
    self.assertEqual(rslt, '20 GOTO 100\nBad line number')

#  don't allow infinite loop

  def testRunGoToBad2 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 1')
    rslt = commands.executeCommand('20 GOTO 20')
    rslt = commands.executeCommand('30 LET A = 2')
    rslt = commands.executeCommand('40 END')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Infinite loop at line 20')



#  test remark

  def testRunDef (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 REM This is a comment')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'REM')

# test stop statement

  def testRunStop (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 STOP')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'STOP')

# test end

  def testRunEnd (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 END')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'END')

  
if __name__ == '__main__':  
    unittest.main()
    