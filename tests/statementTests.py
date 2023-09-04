#  test for statement module

import unittest

import statements
import commands
import scanner
import data
import language


class TestStatements(unittest.TestCase):

# test  clear statement

  def testClear (self):
    data.variables = {'A': 1}
    item = scanner.parseCommand('CLEAR')
    self.assertEqual(item['statement'], 'CLEAR')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables, {})

#  test version 

  def testVersion (self):
    item = scanner.parseCommand('VERSION')
    result = statements.executeStatement(item)
    self.assertEqual(result, language.title + '\n' + language.version)

#  test let statement

  def testLet (self):
    commands.executeCommand('NEW')
    item = scanner.parseCommand('LET A = 1')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    item = scanner.parseCommand('LET B = A + 1')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['B'], 2)

#  test bad let

  def testLet2 (self):
    commands.executeCommand('NEW')
    item = scanner.parseCommand('LET A = ')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'Bad expression')
    item = scanner.parseCommand('PI = 3.14')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'Bad variable')

#  test let with matrix

  def testLet3 (self):
    commands.executeCommand('NEW')
    data.matrixBase = 0
    item = scanner.parseCommand('DIM A(5)')
    self.assertEqual(item['error'], 'OK')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.variables['A']), 5)
    self.assertEqual(len(data.matrixList), 1)
    item = scanner.parseCommand('LET A(3) = 1')
    self.assertEqual(item['error'], 'OK')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'][3], 1)


#  test if statement

  def testIf (self):
    commands.executeCommand('NEW')
    data.address = 10
    commands.executeCommand('LET A = 1')
    self.assertEqual(data.variables['A'], 1)
    item = scanner.parseCommand('20 IF A = 1 THEN 50')
    self.assertEqual(item['line1'], ['50'])   
    self.assertEqual(item['line2'], [])
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)

  def testIfFalse (self):
    commands.executeCommand('NEW')
    data.address = 10
    commands.executeCommand('LET A = 1')
    self.assertEqual(data.variables['A'], 1)
    item = scanner.parseCommand('20 IF A = 2 THEN 50 ELSE 70')
    self.assertEqual(item['line1'], ['50'])
    self.assertEqual(item['line2'], ['70'])
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 70)

#  test if with string

  def testIfString (self):
    commands.executeCommand('NEW')
    data.address = 10
    commands.executeCommand('LET C$ = "A"')
    self.assertEqual(data.variables['C$'], '"A"')
    item = scanner.parseCommand('20 IF C$ = "A" THEN 50 ELSE 70')
    self.assertEqual(item['line1'], ['50'])
    self.assertEqual(item['line2'], ['70'])
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)


# test for statement

  def testFor (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 FOR I = 1 TO 10')
    self.assertEqual(item['error'], 'OK')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['I'], 1)
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'], 'FOR')
    self.assertEqual(stackItem['var'], 'I')
    self.assertEqual(stackItem['min'], 1)
    self.assertEqual(stackItem['max'], 10)
    self.assertEqual(stackItem['line'], 10)

#  test for with step

  def testForWithStep (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 FOR I = 1 TO 10 STEP 2')
    self.assertEqual(item['error'], 'OK')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['I'], 1)
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'], 'FOR')
    self.assertEqual(stackItem['var'], 'I')
    self.assertEqual(stackItem['min'], 1)
    self.assertEqual(stackItem['max'], 10)
    self.assertEqual(stackItem['step'], 2)
    self.assertEqual(stackItem['line'], 10)
    
    #  test next
    
  def testNext (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 FOR I = 1 TO 10')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['I'], 1)
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['var'], 'I')
    self.assertEqual(stackItem['step'], 1)
    data.address = 20
    item= scanner.parseCommand('20 NEXT')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 10)
    self.assertEqual(data.variables['I'], 2)

#  test go to

  def testGoto (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10  GO TO 50')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)    

#  test alternate goto

  def testGoto2 (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10  GOTO 50')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)    

#  test gosub

  def testGosub (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10  GO SUB 50')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)    
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'], 'GOSUB')
    self.assertEqual(stackItem['line'], 10)

#  test gosub - return

  def testReturn (self):
    commands.executeCommand('NEW')
    data.address = 20
    item= scanner.parseCommand('10  GO SUB 50')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 50)    
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'], 'GOSUB')
    self.assertEqual(stackItem['line'], 20)
    item= scanner.parseCommand('50 RETURN')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 20)
    self.assertEqual(len(data.stack), 0)

#  test on gosub

  def testOnGosub (self):
    commands.executeCommand('NEW')
    data.variables['I'] = 3 
    data.address = 20
    item= scanner.parseCommand('10  ON I GOSUB 40, 50, 60, 70, 80, 90')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 60)    
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'], 'GOSUB')
    self.assertEqual(stackItem['line'], 20)

#  test on goto

  def testOnGoto (self):
    commands.executeCommand('NEW')
    data.variables['I'] = 3 
    data.address = 20
    item= scanner.parseCommand('10  ON I GOTO 40, 50, 60, 70, 80, 90')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 60)    
    self.assertEqual(len(data.stack), 0)

#  test remark
    
  def testRemark (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 REM test program')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 10)    
    item= scanner.parseCommand('10 REM')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 10)    
    
#  test option base

  def testOptionBase (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 OPTION BASE 1')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.matrixBase, 1)    
    item= scanner.parseCommand('10 OPTION BASE 0')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.matrixBase, 0)    
    item= scanner.parseCommand('10 OPTION BASE 2')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'Incorrect statement')

    #  test dim statement
    
  def testDim (self):
    commands.executeCommand('NEW')
    data.address = 10
    data.matrixBase = 1
    item= scanner.parseCommand('10 DIM A(3, 3)')
    self.assertEqual(item['dims'], ['3', ',', '3'])
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.matrixList), 1)
    matrixItem = data.matrixList['A']
    self.assertEqual(matrixItem['dim'], [3, 3])
    self.assertEqual(matrixItem['len'], 9) 
    self.assertEqual(len(data.variables['A']), 9) 

#  test data statement
#  note: executing the statement does nothing
    
  def testData (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 DATA 1, 2, 3, 4, 5, 6')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.dataList, [])
    self.assertEqual(data.dataPointer, 0)

    #  test read statement
        
  def testRead (self):
    commands.executeCommand('NEW')
    data.address = 10
    data.dataList = [1, 2, 3]
    data.dataPointer = 0
    item= scanner.parseCommand('10 READ A, B, C')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.dataPointer, 3)
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)
#  test restore statement

  def testRestore (self):
    commands.executeCommand('NEW')
    data.address = 10
    data.dataList = [1, 2, 3]
    data.dataPointer = 2
    item= scanner.parseCommand('10 RESTORE')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.dataPointer, 0)

        #  test trace, untrace statements
        
  def testTrace (self):
    commands.executeCommand('NEW')
    data.address = 10    
    item= scanner.parseCommand('10 TRACE')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.traceFlag, True)    
    item= scanner.parseCommand('20 UNTRACE')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.traceFlag, False)
        
        #  test break statement
        
  def testBreak (self):
    commands.executeCommand('NEW')
    data.address = 10    
    item= scanner.parseCommand('10 Break')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, True)
    self.assertEqual(len(data.breakList), 0)

#  test break with line number
        
  def testBreakWithNumber (self):
    commands.executeCommand('NEW')
    data.address = 10    
    item= scanner.parseCommand('10 Break 50')
    item['next'] = 20
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(data.breakList, [50])
    
    #  test unbreak
    
  def testUnbreak (self):
    commands.executeCommand('NEW')
    data.address = 10    
    data.breakList = [30, 50]
    item= scanner.parseCommand('10 UNBreak')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(len(data.breakList), 0)
    
#  test unbreak with line number
    
  def testUnbreakWithLine (self):
    commands.executeCommand('NEW')
    data.address = 10    
    data.breakList = [30, 50, 70]
    item= scanner.parseCommand('10 UNBREAK 50')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.breakFlag, False)
    self.assertEqual(data.breakList, [30, 70])
    
#  test unbreak with bad line number
    
  def testUnbreakWithBadLine (self):
    commands.executeCommand('NEW')
    data.address = 10    
    data.breakList = [30, 50, 70]
    item= scanner.parseCommand('10 UNBreak 60')    
    result = statements.executeStatement(item)
    self.assertEqual(result, 'Bad line number')

#  test user defined function setup
    
  def testDef (self):
    commands.executeCommand('NEW')
    data.address = 10    
    item= scanner.parseCommand('10 DEF SQK(X) = X * X')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.userFunctionList), 1)
    funcData = data.userFunctionList['SQK']
    self.assertEqual(funcData['arg'], 'X')
    self.assertEqual(funcData['expr'], ['X', '*', 'X'])
    
    #  test load subroutine header
    
  def testLoadSub (self):
    commands.executeCommand('NEW')
    item= scanner.parseCommand('10 SUB LISTDATA (FRUITS, N)')    
    result = statements.doSubLoad(item, 20)    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.callList), 1)
    callData = data.callList['LISTDATA']
    self.assertEqual(callData['args'], ['FRUITS', ',', 'N'])
    self.assertEqual(callData['line'], 20)
  
#  test run subroutine (ddo nothing)
    
  def testSub (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 SUB LISTDATA (FRUITS, N)')
    item['next'] = 20
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.callList), 0)

#  test call statement

  def testCallSub (self):  
    commands.executeCommand('NEW')
    data.callList = {'SQK': {'type': 'SUB', 'line': 250, 'args': ['X', ',', 'Y']}} 
    data.variables = {'A': 1, 'B': 2} 
    data.address = 20
    item= scanner.parseCommand('10 CALL SQK (A, B)')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertEqual(stackItem['type'],'SUB')
    self.assertEqual(stackItem['line'], 20)
    self.assertEqual(stackItem['vars'], {'A': 1, 'B': 2})
    self.assertEqual(data.variables['X'], 1)
    self.assertEqual(data.variables['Y'], 2)
    

#  test end 

  def testExitSub (self):  
    commands.executeCommand('NEW')
    data.callList = {'SQK': {'type': 'SUB', 'line': 250, 'args': ['X', ',', 'Y']}} 
    data.stack = [{'type': 'SUB', 'line': 20, 'vars': {'A': 1, 'B': 2}, 'mats': {}}]
    data.variables = {'X': 1, 'Y': 2} 
    data.address = 150
    item= scanner.parseCommand('140 END SUB')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, 20)
    self.assertEqual(len(data.stack), 0)
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    
       #  test save arguments function
       
    #  test stop / end
    
  def testSaveArgs (self):
    commands.executeCommand('NEW')
    args = ['X', ',', 'Y']
    values = ['5', ',', '10']
    [newVars, newMats, msg] = statements.saveArguments(args, values)
    self.assertEqual(msg, 'OK')
    self.assertEqual(newVars['X'], 5)
    self.assertEqual(newVars['Y'], 10)

#  test save args with variables
    
  def testSaveArgs1 (self):
    commands.executeCommand('NEW')
    data.variables={'A': 5, 'B': 10}
    args = ['X', ',', 'Y']
    values = ['A', ',', 'B']
    [newVars, newMats, msg] = statements.saveArguments(args, values)
    self.assertEqual(msg, 'OK')
    self.assertEqual(newVars['X'], 5)
    self.assertEqual(newVars['Y'], 10)
       
       
    
  def testEnd (self):
    commands.executeCommand('NEW')
    data.address = 10
    item= scanner.parseCommand('10 STOP')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, -1)    
    data.address = 10
    item= scanner.parseCommand('10 END')
    result = statements.executeStatement(item)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.address, -1)    
    

if __name__ == '__main__':  
    unittest.main()
    