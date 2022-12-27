#  test for run time methods

import unittest

import runtime
import commands
import data

class TestRuntime(unittest.TestCase):

# test run with no code

  def testRunNoCode (self):
    result = commands.executeCommand('NEW')
    result = runtime.run()
    self.assertEqual(result, 'No code')

# run a line of code

  def testRunLet (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 Let A = 1')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test let without keyword


  def testRunImpliedLet (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 A = 1')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test if statement

  def testRunIf (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('20 Let A = A + 1')
    result = commands.executeCommand('30 IF A < 11 THEN 20')
    result = commands.executeCommand('40 LET B = A') 
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['B'], 11)

# test goto

  def testRunGoTo (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 40')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 1)

# test goto with bad line number

  def testRunGoToBad (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 100')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run()
    self.assertEqual(result, '20 GOTO 100\nBad line number')

#  don't allow infinite loop

  def testRunGoToBad2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GOTO 20')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run()
    self.assertEqual(result, 'Infinite loop at line 20')

# test GO TO (separate words)

  def testRunGoTo2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 1')
    result = commands.executeCommand('20 GO TO 40')
    result = commands.executeCommand('30 LET A = 2')
    result = commands.executeCommand('40 END')
    result = runtime.run()    
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
    result = runtime.run()
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
    result = runtime.run()
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
    result = runtime.run()    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 10)


# test basic for/next

  def testRunForNext (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 1 TO 5')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 12345)

# test for/next with step

  def testRunForNext2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 2 TO 8 STEP 2')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['A'], 2468)

#  test for/next with negative step

  def testRunForNext3 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET A = 0')
    result = commands.executeCommand('20 FOR I = 5 TO 1 STEP -1')
    result = commands.executeCommand('30 LET A = A * 10 + I')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run()
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
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 45)

# test missing for

  def testRunForNextBad (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    #result = commands.executeCommand('20 FOR I = 1 To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run()
    self.assertEqual(result, '40 NEXT\nMissing FOR')

# test bad for expression

  def testRunForNextBad2 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 To 3')
    result = commands.executeCommand('30 Let N = N + 1')
    result = commands.executeCommand('40 NEXT')
    result = runtime.run()
    self.assertEqual(result, 'Done')

# missing next

  def testRunForNextBad3 (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 LET N = 0')
    result = commands.executeCommand('20 FOR I = 1 To 5')
    result = commands.executeCommand('30 Let N = N + 1')
    #result = commands.executeCommand('40 NEXT')
    result = runtime.run()
    self.assertEqual(len(data.forNextStack), 1)
    self.assertEqual(result, 'Missing NEXT')







#  test remark

  def testRunDef (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 REM This is a comment')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'REM')

# test stop statement

  def testRunStop (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 STOP')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['statement'], 'STOP')

# test end

  def testRunEnd (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 END')
    result = runtime.run()
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
    self.assertEqual(item['error'], 'Bad line number')

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
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['R'] > 0, True)

#  test string join

  def testRunStringCat (self):
    result = commands.executeCommand('NEW')
    result = commands.executeCommand('10 S$ = "Hello " & "world"')
    result = runtime.run()
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['S$'], '"Hello world"')




  
if __name__ == '__main__':  
    unittest.main()
    