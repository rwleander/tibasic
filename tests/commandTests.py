#  test for command module

import unittest

import commands
import data
import language


class TestCommands(unittest.TestCase):

# test  quit command

  def testQuit (self):
    result = commands.executeCommand('QUIT')
    self.assertEqual(result, 'Bye')
    self.assertEqual(data.quitFlag, True)

#  test new

  def testNew (self):
    result = commands.executeCommand('NEW')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 0)

#  test version

  def testVersion (self):
    result = commands.executeCommand('VERSION')
    self.assertEqual(result, language.title + '\n' + language.version)


#  test to add a line of code

  def testAddLine (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 10')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(data.codeList[10], {'code': '10 LET A = 10', 'next': -1}) 

#  add then delete lines

  def testDeleteLine (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('20 LET B = 20')
    result = commands.executeCommand('10')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 1)
    result = commands.executeCommand('10')
    self.assertEqual(result, 'Bad line number')

#  test list command

  def testList (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('30 LET C = A + B')
    commands.executeCommand('20 LET B = 20')
    result = commands.executeCommand('LIST')
    self.assertEqual(result, '10 LET A = 10\n20 LET B = 20\n30 LET C = A + B\nOK')
    self.assertEqual(len(data.codeList), 3)
    result = commands.executeCommand('LIST 20')
    self.assertEqual(result, '20 LET B = 20\nOK')

#  save then load a test file

#  test clear statement

  def testClear (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 10')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 1)
    data.variables = {'A': 10}
    result = commands.executeCommand('CLEAR')
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(len(data.variables), 0)
    
  def testSaveLoad (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('30 LET C = A + B')
    commands.executeCommand('20 LET B = 20')
    self.assertEqual(len(data.codeList), 3)
    result = commands.executeCommand('SAVE TEST')
    self.assertEqual(result, 'OK')
    
    commands.executeCommand('NEW')
    self.assertEqual(len(data.codeList), 0)
    result = commands.executeCommand('OLD TEST')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    
    result = commands.executeCommand('LIST')
    self.assertEqual(result, '10 LET A = 10\n20 LET B = 20\n30 LET C = A + B\nOK')
    
    result = commands.executeCommand('DELETE TEST')    
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('OLD TEST')
    self.assertEqual(result, 'No data found')
    
    #  test run command
       
# test run command
   
  def testRun (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('30 LET C = A + B')
    commands.executeCommand('20 LET B = 20')
    self.assertEqual(len(data.codeList), 3)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['C'], 30)

#  test run command with line number
   
  def testRun2 (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('20 STOP')
    commands.executeCommand('30 LET A = 20')
    commands.executeCommand('40 STOP')
    self.assertEqual(len(data.codeList), 4)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 10)
    result = commands.executeCommand('RUN 30')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 20)

#  test merge - create and save two files, then load and merge
       
  def testMerge (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('20 LET B = 20')
    commands.executeCommand('30 LET C = A + B')
    result = commands.executeCommand('SAVE TEST1')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    commands.executeCommand('NEW')
    commands.executeCommand('100 LET D = C + 10')
    commands.executeCommand('110 LET E = D + A')
    result = commands.executeCommand('SAVE TEST2')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 2)
    commands.executeCommand('NEW')
    commands.executeCommand('OLD TEST1')
    result = commands.executeCommand('MERGE TEST2')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 5)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.variables), 5)
    self.assertEqual(data.variables['E'], 50)
   
   #  test resequence
   
  def testResequence1 (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 1')
    commands.executeCommand('20 IF A > 4 THEN 80')
    commands.executeCommand('30 ON A GOTO 40, 50, 60, 70')    
    commands.executeCommand('40 A = A + 1')
    commands.executeCommand('50 A = A + 1')
    commands.executeCommand('60 A = A + 1')
    commands.executeCommand('70 GOTO 30')
    commands.executeCommand('80 STOP')    
    result = commands.executeCommand('RESEQUENCE 110, 10')
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 8)
    self.assertEqual(data.codeList[110], {'code': '110 LET A = 1', 'next': -1})
    self.assertEqual(data.codeList[120], {'code': '120 IF A > 4 THEN 180', 'next': -1})
    self.assertEqual(data.codeList[130], {'code': '130 ON A GOTO 140, 150, 160, 170', 'next': -1})
    

    #  test let command
            
  def testLet (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('LET A = 1')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)

#  test let with bad variable name

  def testLetBad (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('LET MAX = 1')
    self.assertEqual(result, 'Bad variable')
        
#  test randomize command

  def testRandomize (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('RANDOMIZE')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('LET R = RND(10)')
    self.assertEqual(result, 'OK')
    r = data.variables['R']
    self.assertTrue(r >= 0)
    self.assertTrue(r < 10)

 #  test data statements
 
  def testRead (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 READ A, B')
    commands.executeCommand('20 READ C, D')
    commands.executeCommand('30 STOP')
    commands.executeCommand('40 DATA 1, 2, 3, 4')        
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)
    self.assertEqual(data.variables['D'], 4)

#  test read with restore
 
  def testRestore (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 READ A, B')
    commands.executeCommand('15 RESTORE')
    commands.executeCommand('20 READ C, D')
    commands.executeCommand('30 STOP')
    commands.executeCommand('40 DATA 1, 2, 3, 4')        
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 1)
    self.assertEqual(data.variables['D'], 2)

#  test read, data and restore from the command prompt
 
  def testDataCommand (self):
    commands.executeCommand('NEW')
    result = commands.executeCommand('DATA 1, 2, 3, 4')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('READ A, B')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('RESTORE')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('READ C, D')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 1)
    self.assertEqual(data.variables['D'], 2)

#  test on gosub
 
  def testRunOnGosub (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 N = 0')
    commands.executeCommand('20 I = 2')
    commands.executeCommand('30 ON I GOSUB 50, 60, 70')
    commands.executeCommand('40 STOP')
    commands.executeCommand('50 N = N + 1')
    commands.executeCommand('60 N = N + 1')
    commands.executeCommand('70 N = N + 1')
    commands.executeCommand('80 RETURN')    
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 2)

    #  test on goto
     
  def testRunOnGoto (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 N = 0')
    commands.executeCommand('20 I = 2')
    commands.executeCommand('30 ON I GOTO 50, 60, 70')
    commands.executeCommand('40 N = n + 1')
    commands.executeCommand('50 N = N + 1')
    commands.executeCommand('60 N = N + 1')
    commands.executeCommand('70 N = N + 1')
    commands.executeCommand('80 END')    
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 2)

#  test trace / untrace commands

  def testTrace (self):
    commands.executeCommand('NEW')    
    result = commands.executeCommand('TRACE')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.traceFlag, True)
    result = commands.executeCommand('UNTRACE')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.traceFlag, False)

    #  test break command
    
  def testBreak (self):
    commands.executeCommand('NEW')    
    result = commands.executeCommand('BREAK 50')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(data.breakList, [50])

#  test break without line number

  def testBreakFail (self):
    commands.executeCommand('NEW')    
    result = commands.executeCommand('BREAK')
    self.assertEqual(result, 'Missing line number')

#  test unbreak

  def testUnbreak (self):
    commands.executeCommand('NEW')
    commands.executeCommand('BREAK 50')
    result = commands.executeCommand('BREAK 70')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakList, [50, 70])    
    result = commands.executeCommand('UNBREAK 50')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(data.breakList, [70])

#  test unbreak all

  def testUnbreakAll (self):
    commands.executeCommand('NEW')
    commands.executeCommand('BREAK 50')
    result = commands.executeCommand('BREAK 70')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakList, [50, 70])    
    result = commands.executeCommand('UNBREAK')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(len(data.breakList), 0)

#  test unbreak with bad line number

  def testUnbreakBad (self):
    commands.executeCommand('NEW')
    commands.executeCommand('BREAK 50')
    result = commands.executeCommand('BREAK 70')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakList, [50, 70])    
    result = commands.executeCommand('UNBREAK 60')
    self.assertEqual(result, 'Bad line number')

#  test run from within code

  def testRunStatement (self):    
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 10')
    commands.executeCommand('20 LET B = 20')
    commands.executeCommand('30 LET C = A + B')
    result = commands.executeCommand('SAVE TEST1')
    self.assertEqual(result, 'OK')      
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 0')
    commands.executeCommand('20 LET B = 0')
    commands.executeCommand('30 LET C = 0')
    commands.executeCommand('40 RUN TEST1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['C'], 30)

    

 
if __name__ == '__main__':  
    unittest.main()
    