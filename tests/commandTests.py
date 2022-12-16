#  test for commands module

import unittest

import data
import commands

class TestCommands(unittest.TestCase):

# test the quit function

  def testQuit (self):
    data.quitFlag = False
    commands.executeCommand('quit')
    self.assertEqual(data.quitFlag, True)

# test the bye function

  def testBye (self):
    data.quitFlag = False
    commands.executeCommand('BYE')
    self.assertEqual(data.quitFlag, True)

#---------------------------
#  code editing commands

#  new - clears code and variables
  
  def testNew (self):
    data.codeList = ['10 Let A = 1']
    data.variables = {'I': 10}    
    data.parseList = {10: 'not a structure'}
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(len(data.variables), 1)    
    self.assertEqual(len(data.parseList), 1)
    rslt = commands.executeCommand('NEW')
    self.assertEqual(len(data.codeList), 0)
    self.assertEqual(len(data.variables), 0)    
    self.assertEqual(len(data.parseList), 0)
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

# resequence list
  
  def testResequence1 (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let A = 1')
    rslt = commands.executeCommand('50 Let B = 2')    
    rslt = commands.executeCommand('72 Let C = A + B')
    rslt = commands.executeCommand('Resequence')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('List')
    self.assertEqual(rslt, '10 LET A = 1\n20 LET B = 2\n30 LET C = A + B') 
  
  def testResequence2 (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('20 Let A = 1')
    rslt = commands.executeCommand('50 IF A > 1 THEN 80')
    rslt = commands.executeCommand('70 GOSUB 100')
    rslt = commands.executeCommand('80 GOTO 10')
    rslt = commands.executeCommand('100 RETURN')
    rslt = commands.executeCommand('80 GOTO 20')
    rslt = commands.executeCommand('Resequence')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(data.codeList[10], '10 LET A = 1')
    self.assertEqual(data.codeList[20], '20 IF A > 1 THEN 40')
    self.assertEqual(data.codeList[30], '30 GOSUB 50')
    self.assertEqual(data.codeList[40], '40 GOTO 10')
    self.assertEqual(data.codeList[50], '50 RETURN')

#------------------------
#  file operations

#save then reload a file

  def testSave (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('30 Let C = A+ B')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 3)
    oldList  = commands.executeCommand('LIST TESTFILE1')
    
    rslt = commands.executeCommand('Save TESTFILE1')
    self.assertEqual(rslt, 'OK')
    
    rslt = commands.executeCommand('New')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 0)
    
    rslt = commands.executeCommand('OLD TESTFILE1')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 3)
    newList  = commands.executeCommand('LIST TESTFILE1')
    self.assertEqual(newList, oldList)
    
# save without file name

  def testSaveWithoutFile (self):
    rslt = commands.executeCommand('SAVE')
    self.assertEqual(rslt, 'Missing file name');

#   save with too many args

  def testSaveTooManyArgs (self):  
    rslt = commands.executeCommand('SAVE test test2')
    self.assertEqual(rslt, 'Too many arguments')


# open file with missing name

  def testOldWithoutFile (self):
    rslt = commands.executeCommand('OLD')
    self.assertEqual(rslt, 'Missing file name');

# open with too many args
    
  def testOldTooManyArgs (self):  
    rslt = commands.executeCommand('OLD test test2')
    self.assertEqual(rslt, 'Too many arguments')

# list files
    
  def testFiles (self):  
    rslt = commands.executeCommand('FILES')
    self.assertNotEqual(rslt, '') 

# delete a file
    
  def testDeleteFiles (self):  
    rslt = commands.executeCommand('10 let a = 1')
    rslt = commands.executeCommand('Save testDelete')
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('Delete TestDelete')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('OLD TestDelete')
    self.assertEqual(rslt, 'File not found')

# test delete when file doesn't exist

  def testDeleteMissingFiles (self):  
    rslt = commands.executeCommand('Delete TestXYZ')
    self.assertEqual(rslt, 'File not found')
    
    #----------------------
    #   test other commands
    
    # test let command

  def testLet (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 1')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(data.variables['A'], 1)

  def testLetWithVariable (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 1')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('LET B = A + 1')
    self.assertEqual(len(data.variables), 2)
    self.assertEqual(data.variables['B'], 2)

# test let with bad yntax

  def testLetWithError (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 1 +* 1')
    self.assertEqual(rslt, 'Syntax error')

# test print statement

  def testPrint (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 100')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('Print A')
    self.assertEqual(rslt, '100.0')
    
    # test print with expression
    
  def testPrintWithExpression (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('LET A = 100')
    self.assertEqual(rslt, 'OK')
    rslt = commands.executeCommand('Print A + 1')
    self.assertEqual(rslt, '101.0')
    
    


if __name__ == '__main__':  
    unittest.main()
    