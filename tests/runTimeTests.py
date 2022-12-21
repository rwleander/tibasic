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

# test let without keyword


  def testRunImpliedLet (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 A = 1')
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

#  test gosub, return

  def testRunGosub (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 1')
    rslt = commands.executeCommand('20 GOSUB 50')
    rslt = commands.executeCommand('30 STOP')
    rslt = commands.executeCommand('50 LET A = 10')
    rslt = commands.executeCommand('60 RETURN')    
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 10)

# test nested gosub

  def testRunGosub (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 10')
    rslt = commands.executeCommand('20 GOSUB 50')
    rslt = commands.executeCommand('30 STOP')
    rslt = commands.executeCommand('50 LET A = 20')
    rslt = commands.executeCommand('60 GOSUB 100')    
    rslt = commands.executeCommand('70 RETURN')
    rslt = commands.executeCommand('100 LET A = 30')
    rslt = commands.executeCommand('110 RETURN')    
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 30)

# test basic for/next

  def testRunForNext (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 0')
    rslt = commands.executeCommand('20 FOR I = 1 TO 5')
    rslt = commands.executeCommand('30 LET A = A * 10 + I')
    rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 12345)

# test for/next with step

  def testRunForNext2 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 0')
    rslt = commands.executeCommand('20 FOR I = 2 TO 8 STEP 2')
    rslt = commands.executeCommand('30 LET A = A * 10 + I')
    rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 2468)

#  test for/next with negative step

  def testRunForNext3 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET A = 0')
    rslt = commands.executeCommand('20 FOR I = 5 TO 1 STEP -1')
    rslt = commands.executeCommand('30 LET A = A * 10 + I')
    rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['A'], 54321)

#  test nested for/next

  def testRunForNext4 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET N = 0')
    rslt = commands.executeCommand('20 FOR I = 1 to 2')
    rslt = commands.executeCommand('30 FOR J = 1 To 5')
    rslt = commands.executeCommand('40 Let N = N + (I * j)')
    rslt = commands.executeCommand('50 NEXT')
    rslt = commands.executeCommand('60 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')
    self.assertEqual(data.variables['N'], 45)

# test missing for

  def testRunForNextBad (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET N = 0')
    #rslt = commands.executeCommand('20 FOR I = 1 To 5')
    rslt = commands.executeCommand('30 Let N = N + 1')
    rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, '40 NEXT\nMissing FOR')

# test bad for expression

  def testRunForNextBad2 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET N = 0')
    rslt = commands.executeCommand('20 FOR I = 1 To 3')
    rslt = commands.executeCommand('30 Let N = N + 1')
    rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(rslt, 'Done')

# missing next

  def testRunForNextBad3 (self):
    rslt = commands.executeCommand('NEW')
    rslt = commands.executeCommand('10 LET N = 0')
    rslt = commands.executeCommand('20 FOR I = 1 To 5')
    rslt = commands.executeCommand('30 Let N = N + 1')
    #rslt = commands.executeCommand('40 NEXT')
    rslt = runtime.run()
    self.assertEqual(len(data.forNextStack), 1)
    self.assertEqual(rslt, 'Missing NEXT')







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





  
if __name__ == '__main__':  
    unittest.main()
    