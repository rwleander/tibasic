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
    result = commands.executeCommand('NEW')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 0)
    self.assertEqual(len(data.variables), 0)    
    self.assertEqual(len(data.parseList), 0)
    self.assertEqual(len(data.gosubStack), 0)
    self.assertEqual(len(data.forNextStack), 0)
    self.assertEqual(len(data.dataList), 0)
    self.assertEqual(data.dataPointer, 0)
    

#  list - lists code to screen
  
  def testList (self):
    data.codeList = {10: '10 Let A = 1', 20: '20 Let B = 30', 30: '30 Let C = A + B'}
    result = commands.executeCommand('LIST')
    self.assertEqual(result, '10 Let A = 1\n20 Let B = 30\n30 Let C = A + B')    
    
  def testListUnordered (self):
    data.codeList = {20: '20 Let A = 1', 10: '10 Let B = 30', 30: '30 Let C = A + B'}
    result = commands.executeCommand('LIST')
    self.assertEqual(result, '10 Let B = 30\n20 Let A = 1\n30 Let C = A + B')

#  partial lists
  
  def testListPartial (self):
    data.codeList = {10: '10 Let A = 1', 20: '20 Let B = 30', 30: '30 Let C = A + B', 40: '40 PRINT C' }
    result = commands.executeCommand('LIST')
    self.assertEqual(result, '10 Let A = 1\n20 Let B = 30\n30 Let C = A + B\n40 PRINT C')
    result = commands.executeCommand('LIST 20')
    self.assertEqual(result, '20 Let B = 30')
    result = commands.executeCommand('LIST -20')
    self.assertEqual(result, '10 Let A = 1\n20 Let B = 30')
    result = commands.executeCommand('LIST 30-')
    self.assertEqual(result, '30 Let C = A + B\n40 PRINT C')
    result = commands.executeCommand('LIST 20 - 30')
    self.assertEqual(result, '20 Let B = 30\n30 Let C = A + B')

  def testListNone (self):
    data.codeList = {} 
    result = commands.executeCommand('LIST')
    self.assertEqual(result, 'Can\'t do that')

  def testListBad (self):
    data.codeList = {10: '10 FOR I = 1 TO 10', 20: '20 PRINT I;',30: '30 NEXT'} 
    result = commands.executeCommand('LIST xx')
    self.assertEqual(result, 'Incorrect statement')

  def testListBad2 (self):
    data.codeList = {10: '10 FOR I = 1 TO 10', 20: '20 PRINT I;',30: '30 NEXT'} 
    result = commands.executeCommand('LIST -')
    self.assertEqual(result, 'Incorrect statement')


  def testListBad2 (self):
    data.codeList = {10: '10 FOR I = 1 TO 10', 20: '20 PRINT I;',30: '30 NEXT'} 
    result = commands.executeCommand('LIST 40')
    self.assertEqual(result, 'Bad line number')
    
#  code lines add, replace or delete

  def testAddLine (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('10 Let A = 1')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 1)
    result = commands.executeCommand('list')
    self.assertEqual(result, '10 LET A = 1')
 
  def testAddTwoLines (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('10 Let A = 1')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 2)
    result = commands.executeCommand('list')
    self.assertEqual(result, '10 LET A = 1\n20 LET B = 2')

  def testDeleteLines (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('20')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 1)
    result = commands.executeCommand('list')
    self.assertEqual(result, '10 LET A = 1')
  
  def testDeleteMissingLines (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('25')
    self.assertEqual(result, 'Bad line number')
  
  def testAddBadLines (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('10x Let A = 1')
    self.assertEqual(result, 'Bad line number')

# resequence list
  
  def testResequence1 (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let A = 1')
    result = commands.executeCommand('50 Let B = 2')    
    result = commands.executeCommand('72 Let C = A + B')
    result = commands.executeCommand('Resequence')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('List')
    self.assertEqual(result, '100 LET A = 1\n110 LET B = 2\n120 LET C = A + B') 
  
  def testResequence2 (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let A = 1')
    result = commands.executeCommand('50 IF A > 1 THEN 80')
    result = commands.executeCommand('70 GOSUB 100')
    result = commands.executeCommand('80 GOTO 10')
    result = commands.executeCommand('100 RETURN')
    result = commands.executeCommand('80 GOTO 20')
    result = commands.executeCommand('Resequence')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList[100], '100 LET A = 1')
    self.assertEqual(data.codeList[110], '110 IF A > 1 THEN 130')
    self.assertEqual(data.codeList[120], '120 GOSUB 140')
    self.assertEqual(data.codeList[130], '130 GOTO 100')
    self.assertEqual(data.codeList[140], '140 RETURN')
  
  def testResequence3 (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('20 Let A = 1')
    result = commands.executeCommand('50 IF A > 1 THEN 810')
    result = commands.executeCommand('70 GOSUB 100')
    result = commands.executeCommand('80 GOTO 10')
    result = commands.executeCommand('100 RETURN')
    result = commands.executeCommand('80 GOTO 20')
    result = commands.executeCommand('Resequence 200, 20')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList[200], '200 LET A = 1')
    self.assertEqual(data.codeList[220], '220 IF A > 1 THEN 32767')
    self.assertEqual(data.codeList[240], '240 GOSUB 280')
    self.assertEqual(data.codeList[260], '260 GOTO 200')
    self.assertEqual(data.codeList[280], '280 RETURN')
 
  
  def testResequenceBad (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('Resequence')
    self.assertEqual(result, 'Can\'t do that')
  
  def testResequenceBad2 (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('10 A = 1')
    result = commands.executeCommand('Resequence xx')
    self.assertEqual(result, 'Incorrect statement')
  
  def testResequenceBad3 (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('10 A = 1')
    result = commands.executeCommand('20 B = 2')
    result = commands.executeCommand('30 C = 3')
    result = commands.executeCommand('Resequence 30000, 1000')
    self.assertEqual(result, 'Bad line number\nNo line numbers in this program are change')
    
#------------------------
#  file operations

#save then reload a file

  def testSave (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('30 Let C = A+ B')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    oldList  = commands.executeCommand('LIST TESTFILE1')
    
    result = commands.executeCommand('Save TESTFILE1')
    self.assertEqual(result, 'OK')
    
    result = commands.executeCommand('New')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 0)
    
    result = commands.executeCommand('OLD TESTFILE1')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    newList  = commands.executeCommand('LIST TESTFILE1')
    self.assertEqual(newList, oldList)
    
# save without file name

  def testSaveWithoutFile (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('SAVE TEST')
    self.assertEqual(result, 'Can\'t do that')
    result = commands.executeCommand('10 A = 1')
    result = commands.executeCommand('SAVE')
    self.assertEqual(result, 'Incorrect statement')
    result = commands.executeCommand('SAVE TEST, TEST1')
    self.assertEqual(result, 'Incorrect statement')

# open file with missing name

  def testOldWithoutFile (self):
    result = commands.executeCommand('OLD')
    self.assertEqual(result, 'Incorrect statement');

# open with too many args
    
  def testOldTooManyArgs (self):  
    result = commands.executeCommand('OLD test test2')
    self.assertEqual(result, 'Incorrect statement')
    result = commands.executeCommand('DELETE TEST')
    result = commands.executeCommand('OLD  TEST')
    self.assertEqual(result, 'No data found')

# list files
    
  def testFiles (self):  
    result = commands.executeCommand('FILES')
    self.assertNotEqual(result, '') 

# delete a file
    
  def testDeleteFiles (self):  
    result = commands.executeCommand('10 let a = 1')
    result = commands.executeCommand('Save testDelete')
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('Delete TestDelete')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('OLD TestDelete')
    self.assertEqual(result, 'No data found')

# test delete when file doesn't exist

  def testDeleteMissingFiles (self):  
    result = commands.executeCommand('Delete TestXYZ')
    self.assertEqual(result, 'No data found')
    
    #----------------------
    #   test other commands
    
    # test let command

  def testLet (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('LET A = 1')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(data.variables['A'], 1)

  def testLetWithVariable (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('LET A = 1')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('LET B = A + 1')
    self.assertEqual(len(data.variables), 2)
    self.assertEqual(data.variables['B'], 2)

# test let with bad input

  def testLetWithError (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('LET A = 1 +* 1')
    self.assertEqual(result, 'Bad expression')

#  test let with bad variable name

  def testLetWitBadVariable (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('LET @A12 = 1')
    self.assertEqual(result, 'Bad name')

#  test run command with errors

  def testRunBad (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('Run')
    self.assertEqual(result, 'Can\'t do that')


# test print statement


if __name__ == '__main__':  
    unittest.main()
    