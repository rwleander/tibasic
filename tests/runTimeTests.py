#  test for run time methods

import unittest

import runtime
import commands
import data

class TestRuntime(unittest.TestCase):

# test run with no code

  def testRunNoCode (self):
    result = commands.executeCommand('NEW')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Can\'t do that')

  def testRunBadLine (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 A = 1')
    result = runtime.run('RUN xx')
    self.assertEqual(result, 'Bad line number')
    result = runtime.run('RUN 20')
    self.assertEqual(result, 'Bad line number - 20')

# run a line of code

  def testRunLet (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 Let A = 1')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

#  test run with line number

  def testRunWithLineNumber (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 A = 10')
    result = commands.executeCommand('20 STOP')
    result = commands.executeCommand('30 A = 30')
    result = runtime.run('RUN')
    self.assertEqual(data.variables['A'], 10)
    result = runtime.run('RUN 30')
    self.assertEqual(data.variables['A'], 30)

# test let with bad expression

  def testRunLet2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 Let A = 4 + * 2')
    result = runtime.run('RUN')
    self.assertEqual(result, '10 LET A = 4 + * 2\nBad expression')


# test let without keyword


  def testRunImpliedLet (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 A = 1')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test if statement

  def testRunIf (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('20 Let A = A + 1')
    result = commands.executeCommand('30 IF A < 11 THEN 20')
    result = commands.executeCommand('40 LET B = A') 
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['B'], 11)

  def testRunIfZero (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 IF 0 THEN 30')
    result = commands.executeCommand('20 LET A = 1') 
    result = commands.executeCommand('25 STOP')
    result = commands.executeCommand('30 LET A = 2') 
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

  def testRunIfLogic(self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 IF ( 5 > 3) * ( 4 > 2) THEN 30')
    result = commands.executeCommand('20 LET A = 1') 
    result = commands.executeCommand('25 STOP')
    result = commands.executeCommand('30 LET A = 2') 
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 2)



# test goto

  def testRunGoTo (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 40')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test goto with bad line number

  def testRunGoToBad (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 100')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run('RUN')
    self.assertEqual(result, '20 GOTO 100\nBad line number')

#  don't allow infinite loop

  def testRunGoToBad2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 20')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run('RUN')
    self.assertEqual(result, '20 GOTO 20\nInfinite loop')

# test GO TO (separate words)

  def testRunGoTo2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GO TO 40')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run('RUN')    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

#  test gosub, return

  def testRunGosub (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOSUB 50')
    result = commands.executeCommand('30 STOP')
    result = commands.executeCommand('50 LET A = 10')
    result = commands.executeCommand('60 RETURN')    
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 10)

# test nested gosub

  def testRunGosub (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 10')
    result = commands.executeCommand('20 GOSUB 50')
    result = commands.executeCommand('30 STOP')
    result = commands.executeCommand('50 LET A = 20')
    result = commands.executeCommand('60 GOSUB 100')    
    result = commands.executeCommand('70 RETURN')
    result = commands.executeCommand('100 LET A = 30')
    result = commands.executeCommand('110 RETURN')    
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 30)

#  test go sub (two words)

  def testRunGosub2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GO SUB 50')
    result = commands.executeCommand('30 STOP')
    result = commands.executeCommand('50 LET A = 10')
    result = commands.executeCommand('60 RETURN')        
    result = runtime.run('RUN')    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 10)

  def testRunGosubBadLine (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GO SUB 50')
    result = runtime.run('RUN')    
    self.assertEqual(result, '20 GO SUB 50\nBad line number')


# test basic for/next

  def testRunForNext (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 1 TO 5')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 12345)

# test for/next with step

  def testRunForNext2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 2 TO 8 STEP 2')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 2468)

#  test for/next with negative step

  def testRunForNext3 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 5 TO 1 STEP -1')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 54321)

#  test nested for/next

  def testRunForNext4 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 to 2')
    result = commands.executeCommand('30 FOR J = 1 To 5')
    result = commands.executeCommand('40 Let N = N + (I * j)')
    result = commands.executeCommand('50 NEXT')
    result = commands.executeCommand('60 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 45)

# test missing for

  def testRunForNextBad (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    #result = commands.executeCommand('20 FOR I = 1 To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'For-next error')

# test bad for expression

  def testRunForNextBad2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 To 3 STEP 0')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, '20 FOR I = 1 TO 3 STEP 0\nBad value')

# missing next

  def testRunForNextBad3 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    result = runtime.run('RUN')
    self.assertEqual(result, 'For-next error')

#  when starting value exceeds max, skip the loop

  def testRunForNextIndexOutOfRange (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('15 LET X = 10')
    result = commands.executeCommand('20 FOR I = X To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 0) 

#  for/next mismatch

  def testRunForNextMismatch (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 To 5')
    result = commands.executeCommand('25 FOR J = 1 To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('35 IF N > 10 then 50')
    result = commands.executeCommand('40 NEXT J')
    result = commands.executeCommand('50 NEXT I')
    result = runtime.run('RUN')
    self.assertEqual(result, '50 NEXT I\nCan\'t do that')
    


#  test remark

  def testRunDef (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 REM This is a comment')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'REM')

# test stop statement

  def testRunStop (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 STOP')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'STOP')

# test end

  def testRunEnd (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 END')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'END')


#---------------------
#  test helper functions

# test getstring


  def testRunGetString (self):
    item = {'expr': 'A < B', 'error': 'OK'}
    expr = runtime.getString(item, 'expr')    
    self.assertEqual(expr, 'A < B')
    self.assertEqual(item['error'], 'OK')

#  test get string with missing item

  def testRunGetStringWithError (self):
    item = {'expr1': 'A < B', 'error': 'OK'}
    expr = runtime.getString(item, 'expr')    
    self.assertEqual(expr, 'error')
    self.assertEqual(item['error'], 'Missing expr')

#  test get line number

  def testRunGetLine (self):
    item = {'line': '10', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B'}
    line = runtime.getLine(item, 'line')
    self.assertEqual(line, 10)
    self.assertEqual(item['error'], 'OK')

# get line with missing item

#  test get line number

  def testRunGetLineMissing (self):
    item = {'line1': '10', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B'}
    line = runtime.getLine(item, 'line')
    self.assertEqual(line, -1)
    self.assertEqual(item['error'], 'Missing line')

#  test with bad line number

  def testRunGetLineBad (self):
    item = {'line': '1X', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B'}
    line = runtime.getLine(item, 'line')
    self.assertEqual(line, -1)
    self.assertEqual(item['error'], 'Bad line number - 1X')

#  test get line with line not in program

  def testRunGetLineMissing2 (self):
    item = {'line': '20', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B'}
    line = runtime.getLine(item, 'line')
    self.assertEqual(line, 20)
    self.assertEqual(item['error'], 'Bad line number')

# test get line optional

  def testRunGetLineOptional (self):
    item = {'line': '10', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B', 20: '20 LET B = 1'}
    line = runtime.getLineOptional(item, 'line', 20)
    self.assertEqual(line, 10)
    self.assertEqual(item['error'], 'OK')

#  get optional line not in item

  def testRunGetLineOptionalMissing (self):
    item = {'line1': '10', 'error': 'OK'}
    data.parseList = {10: '10 LET A = B', 20: '20 LET B = 1'}
    line = runtime.getLineOptional(item, 'line2', 20)
    self.assertEqual(line, 20)
    self.assertEqual(item['error'], 'OK')

#  test randomize

  def testRunRandomize (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 RANDOMIZE')
    result = commands.executeCommand('20 R = RND()')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['R'] > 0, True)

#  test string join

  def testRunStringCat (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 S$ = "Hello " & "world"')
    result = runtime.run('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['S$'], '"Hello world"')
    
#  test process input function

  def testProcessInput (self):
    vars = ['A', 'B', 'C']
    values = [1, 2, 3]
    result = runtime.processInputs(vars, values)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)

  def testProcessInput2 (self):
    vars = ['A$', 'B$', 'C']
    values = ['Red', '"Blue"', '3']
    result = runtime.processInputs(vars, values)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A$'], '"Red"')
    self.assertEqual(data.variables['B$'], '"Blue"')
    self.assertEqual(data.variables['C'], 3)


# test input from string

  def testProcessInput3 (self):
    vars = ['A$', 'B$', 'C']    
    result = runtime.processInputsFromString(vars, 'Red, "Blue", 3')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A$'], '"Red"')
    self.assertEqual(data.variables['B$'], '"Blue"')
    self.assertEqual(data.variables['C'], 3)

# test split values function

  def testSplitValues (self):
    result = runtime.splitValues('1, 2, 3')
    self.assertEqual(result, ['1', '2', '3'])
    result = runtime.splitValues('Red, "Blue", 3')
    self.assertEqual(result, ['Red', '"Blue"', '3'])

#  test initial load of data items

  def testLoadData (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 DATA 1, 2, 3, 4, 5')
    result = commands.executeCommand('20 DATA red, blue, green')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.dataList, ['1', '2', '3', '4', '5', 'RED', 'BLUE', 'GREEN'])
    self.assertEqual(data.dataPointer, 0)

#  test read statement

  def testReadData (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 READ A$, B$, C$')
    result = commands.executeCommand('20 DATA red, blue, green')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A$'], '"RED"')
    self.assertEqual(data.variables['B$'], '"BLUE"')    
    self.assertEqual(data.variables['C$'], '"GREEN"')    

#  test restore statement

  def testRestore (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 READ A')
    result = commands.executeCommand('20 RESTORE')
    result = commands.executeCommand('30 READ B')
    result = commands.executeCommand('40 RESTORE 90')
    result = commands.executeCommand('60 READ C')
    result = commands.executeCommand('70 DATA 1')
    result = commands.executeCommand('80 DATA 2')
    result = commands.executeCommand('90 DATA 3')        
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 1)
    self.assertEqual(data.variables['C'], 3)

#  test option base

  def testOption (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 OPTION BASE 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 1)

# test dim statement

  def testDim (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 DIM A(5)')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 0)
    self.assertEqual(len(data.matrixList), 1)
    self.assertEqual(data.matrixList['A'], {'x': 5, 'y': 0, 'z': 0})
    self.assertEqual(data.variables['A'], [0, 0, 0, 0, 0])

  def testDim2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 OPTION BASE 1')    
    result = commands.executeCommand('20 DIM A(5, 5)')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 1)
    self.assertEqual(len(data.matrixList), 1)
    self.assertEqual(data.matrixList['A'], {'x': 5, 'y': 5, 'z': 0})
    self.assertEqual(len(data.variables['A']), 25)

  def testDim3 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 DIM A(5, 5, 5)')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 0)
    self.assertEqual(len(data.matrixList), 1)
    self.assertEqual(data.matrixList['A'], {'x': 5, 'y': 5, 'z': 5})
    self.assertEqual(len(data.variables['A']), 125)

  def testDim4 (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 DIM A(5)')
    result = commands.executeCommand('20 FOR I = 0 TO 4')
    result = commands.executeCommand('30 A(I) = I')
    result = commands.executeCommand('40 NEXT')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 0)
    self.assertEqual(len(data.matrixList), 1)
    self.assertEqual(data.matrixList['A'], {'x': 5, 'y': 0, 'z': 0})
    self.assertEqual(data.variables['A'], [0, 1, 2, 3, 4])

  def testDim5 (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('5 OPTION BASE 1')
    result = commands.executeCommand('10 DIM A(5), B(5)')
    result = commands.executeCommand('20 FOR I = 1 TO 5')
    result = commands.executeCommand('30 A(I) = I')
    result = commands.executeCommand('35 B(I) = I * 2')
    result = commands.executeCommand('40 NEXT')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 1)
    self.assertEqual(len(data.matrixList), 2)
    self.assertEqual(data.matrixList['A'], {'x': 5, 'y': 0, 'z': 0})
    self.assertEqual(data.matrixList['B'], {'x': 5, 'y': 0, 'z': 0})
    self.assertEqual(data.variables['A'], [1, 2, 3, 4, 5])
    self.assertEqual(data.variables['B'], [2, 4, 6, 8, 10])

  def testDim6 (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('5 OPTION BASE 1')
    result = commands.executeCommand('10 DIM A(3, 3)')
    result = commands.executeCommand('20 FOR I = 1 TO 3')
    result = commands.executeCommand('25 FOR J = 1 TO 3')
    result = commands.executeCommand('30 LET A(I, J) = I + J')
    result = commands.executeCommand('40 NEXT')
    result = commands.executeCommand('45 NEXT')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.matrixBase, 1)
    self.assertEqual(len(data.matrixList), 1)
    self.assertEqual(data.matrixList['A'], {'x': 3, 'y': 3, 'z': 0})
    self.assertEqual(data.variables['A'], [2, 3, 4, 3, 4, 5, 4, 5, 6])


#  test option base after dim

  def testOption2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 DIM A(5, 5, 5)')
    result = commands.executeCommand('20 OPTION BASE 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '20 OPTION BASE 1\nOption must be before dim')

#  test array values within expressions

  def testArrayExpression (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 DIM A(5)')
    result = commands.executeCommand('20 FOR I = 0 To 4')
    result = commands.executeCommand('30 LET A(I) = I + 1')
    result = commands.executeCommand('40 NEXT')
    result = commands.executeCommand('50 B = A(3)')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.variables['A'], [1, 2, 3, 4, 5])
    self.assertEqual(data.variables['B'], 4)

#  test on goto


  def testOnGoto (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 2')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOTO 30, 40, 50')
    result = commands.executeCommand('30 N = N + 1')
    result = commands.executeCommand('40 N = N + 2')
    result = commands.executeCommand('50 N = N + 3') 
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.variables['N'], 5)

  def testOnGotoBadIndex (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 20')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOTO 30, 40, 50')
    result = commands.executeCommand('30 N = N + 1')
    result = commands.executeCommand('40 N = N + 2')
    result = commands.executeCommand('50 N = N + 3') 
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '20 ON A GOTO 30, 40, 50\nBad value')

  def testOnGotoBadLine (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 2')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOTO 30, 400, 50')
    result = commands.executeCommand('30 N = N + 1')
    result = commands.executeCommand('40 N = N + 2')
    result = commands.executeCommand('50 N = N + 3') 
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '20 ON A GOTO 30, 400, 50\nBad line number - 400')

#  test on gosub

  def testOnGosub (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 2')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOSUB 30, 40, 50')
    result = commands.executeCommand('25 STOP')
    result = commands.executeCommand('30 N = 5')
    result = commands.executeCommand('35 RETURN')
    result = commands.executeCommand('40 N = 10')
    result = commands.executeCommand('45 RETURN')
    result = commands.executeCommand('50 N = 25')
    result = commands.executeCommand('55 RETURN')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')        
    self.assertEqual(data.variables['N'], 10)

  def testOnGosubBadIndex (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 20')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOSUB 30, 40, 50')
    result = commands.executeCommand('25 STOP')
    result = commands.executeCommand('30 N = 5')
    result = commands.executeCommand('35 RETURN')
    result = commands.executeCommand('40 N = 10')
    result = commands.executeCommand('45 RETURN')
    result = commands.executeCommand('50 N = 25')
    result = commands.executeCommand('55 RETURN')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '20 ON A GOSUB 30, 40, 50\nBad index')

  def testOnGosubBadLine (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 A = 2')
    result = commands.executeCommand('15 N = 0')
    result = commands.executeCommand('20 ON A GOSUB 30, 41, 50')
    result = commands.executeCommand('25 STOP')
    result = commands.executeCommand('30 N = 5')
    result = commands.executeCommand('35 RETURN')
    result = commands.executeCommand('40 N = 10')
    result = commands.executeCommand('45 RETURN')
    result = commands.executeCommand('50 N = 25')
    result = commands.executeCommand('55 RETURN')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '20 ON A GOSUB 30, 41, 50\nBad line number - 41')

#  test break, unbreak

  def testBreakpoint (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('10 BREAK 40')
    result = commands.executeCommand('20 N = 0')
    result = commands.executeCommand('30 FOR I = 1 to 5')
    result = commands.executeCommand('40 N = N + 1')
    result = commands.executeCommand('60 NEXT')
    result = commands.executeCommand('70 REM PRINT N')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Breakpoint at 40\n40 N = N + 1')
    self.assertEqual(data.variables['N'], 0)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 5)
    
  def testBreakpoint2 (self):
    result = commands.executeCommand('NEW')    
    result = commands.executeCommand('BREAK 40')
    self.assertEqual(result, 'Bad line number - 40')
    result = commands.executeCommand('20 N = 0')
    result = commands.executeCommand('30 FOR I = 1 to 5')
    result = commands.executeCommand('40 N = N + 1')
    result = commands.executeCommand('60 NEXT')
    result = commands.executeCommand('70 REM PRINT N')
    result = commands.executeCommand('BREAK 40')
    self.assertEqual(result, 'OK')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Breakpoint at 40\n40 N = N + 1')
    self.assertEqual(data.variables['N'], 0)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 5)



if __name__ == '__main__':  
    unittest.main()
    