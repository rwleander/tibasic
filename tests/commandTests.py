#  test for monitor module

import unittest

import data
import commands

class TestMonitor(unittest.TestCase):

# test the quit function

  def testQuit (self):
    self.assertEqual(data.quitFlag, False)
    commands.executeCommand('quit')
    self.assertEqual(data.quitFlag, True)

#---------------------------
#  code editing commands

#  new - clears code and variables
  
  def testNew (self):
    data.codeList = ['10 Let A = 1']
    data.variables = {'I': 10}
    data.strings = {'msg': 'This is a message'}
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(len(data.strings), 1)
    rslt = commands.executeCommand('NEW')
    self.assertEqual(len(data.codeList), 0)
    self.assertEqual(len(data.variables), 0)
    self.assertEqual(len(data.strings), 0)
    self.assertEqual(rslt, 'OK')

#  list - lists code to screen
  
  def testList (self):
    data.codeList = {10: '10 Let A = 1', 20: '20 Let B = 30', 30: '30 Let C = A + B'}
    rslt = commands.executeCommand('LIST')
    self.assertEqual(rslt, '10 Let A = 1\n20 Let B = 30\n30 Let C = A + B')
    
  def testListNotOrdered (self):
    data.codeList = {20: '20 Let A = 1', 10: '10 Let B = 30', 30: '30 Let C = A + B'}
    rslt = commands.executeCommand('LIST')
    self.assertEqual(rslt, '10 Let B = 30\n20 Let A = 1\n30 Let C = A + B')

#  code lines add, replace or delete

  def testAddLine (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('10 Let A = 1')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 1)
    rslt = commands.executeCommand('list')
    self.assertEqual(rslt, '10 LET A = 1')
 
  def testAddTwoLines (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('10 Let A = 1')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 2)
    rslt = commands.executeCommand('list')
    self.assertEqual(rslt, '10 LET A = 1\n20 LET B = 2')
  
  def testDeleteLines (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('20')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 1)
    rslt = commands.executeCommand('list')
    self.assertEqual(rslt, '10 LET A = 1')
  
  def testDeleteMissingLines (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('25')
    self.assertEqual(rslt, 'Not in list')
  
  def testAddBadLines (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('10x Let A = 1')
    self.assertEqual(rslt, 'Bad line number')


#------------------------
#  file operations

#save a file

  def testSave (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('30 Let C = A+ B')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 3)
    rslt = commands.executeCommand('Save TESTFILE1')
    self.assertEqual(rslt, 'OK')
    

 
  
if __name__ == '__main__':  
    unittest.main()
    