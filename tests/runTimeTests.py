#  test for runtime  module

import unittest

import runtime
import commands
import scanner
import data

class TestRuntime(unittest.TestCase):

# test  program execution

  def testRun (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 1')
    commands.executeCommand('20 LET B = 2')
    commands.executeCommand('30 LET C = A + B')
    scanner.createIndex()
    result = runtime.run()    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['C'], 3)
    
#  test if statement

  def testRunIf (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 1')
    commands.executeCommand('20 IF A = 1 Then 40')
    commands.executeCommand('30 LET A = 2')
    commands.executeCommand('40 LET B = A')
    scanner.createIndex()
    result = runtime.run()    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['B'], 1)

    #  test for/next
    
  def testRunForNext (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET N = 0')
    commands.executeCommand('20 FOR I = 1 To 10')    
    commands.executeCommand('30 LET N = N + I')    
    commands.executeCommand('40 NEXT')
    commands.executeCommand('50 LET X = N')
    scanner.createIndex()
    result = runtime.run()    
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['I'], 11)
    self.assertEqual(data.variables['N'], 55)
    
#  test rem and stop/end
    
  def testRemark (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 REM test program')
    commands.executeCommand('20 REM')
    commands.executeCommand('30 STOP')
    commands.executeCommand('40 END')
    scanner.createIndex()
    result = runtime.run()    
    self.assertEqual(result, 'Done')
    
#  test gosub

  def testRunGosub (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET N = 0')
    commands.executeCommand('20 GOSUB 50')
    commands.executeCommand('30 STOP')
    commands.executeCommand('50 LET N = 5')
    commands.executeCommand('60 RETURN')
    self.assertEqual(len(data.codeList), 5)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['N'], 5)

#  test call subroutine

  def testRunCall (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET N = 5')
    commands.executeCommand('20 Call TESTIT (N)')
    commands.executeCommand('30 STOP')
    commands.executeCommand('50 SUB TESTIT(X)')
    commands.executeCommand('60 BREAK')
    commands.executeCommand('70 EXIT SUB')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 70')
    self.assertEqual(data.variables['X'], 5)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(data.variables['N'], 5)

#  test subroutine call with array

  def testRunCall2 (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 DIM A(3, 3)')
    commands.executeCommand('15 A(1, 1) = 11')
    commands.executeCommand('20 Call TESTIT (A)')
    commands.executeCommand('30 STOP')
    commands.executeCommand('50 SUB TESTIT(X)')
    commands.executeCommand('50 SUB TESTIT(X)')
    commands.executeCommand('55 Z = X(1, 1)')
    commands.executeCommand('60 BREAK')
    commands.executeCommand('70 EXIT SUB')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 70')
    self.assertEqual(len(data.stack), 1)
    stackItem = data.stack[0]
    self.assertTrue('mats' in stackItem)
    self.assertEqual(len(data.variables), 2)
    self.assertEqual(data.variables['Z'], 11)
    self.assertEqual(len(data.matrixList), 1)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(len(data.matrixList), 1)




#  test random numbers

  def testRunRandomize (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 RANDOMIZE')
    commands.executeCommand('20 LET R = RND(10)')
    self.assertEqual(len(data.codeList), 2)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    r = data.variables['R']
    self.assertTrue(r >= 0)
    self.assertTrue(r < 10)
    
    #  test matrix operations
    
  def testRunMatrix (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 OPTION BASE 1')
    commands.executeCommand('20 DIM X(3, 3)')
    commands.executeCommand('30 N = 1')
    commands.executeCommand('40 FOR I = 1 TO 3')
    commands.executeCommand('50 FOR J = 1 TO 3')
    commands.executeCommand('60 LET X(I, J) = N')    
    commands.executeCommand('70 N = N + 1')
    commands.executeCommand('80 NEXT')
    commands.executeCommand('90 NEXT')
    self.assertEqual(len(data.codeList), 9)
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')
    self.assertEqual(data.variables['X'], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    self.assertEqual(data.variables['X'], [1, 2, 3, 4, 5, 6, 7, 8, 9])

#  test variables using reserved words
    
  def testRunReserved (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET MIN = 0')
    commands.executeCommand('20 LET MIN = MIN + 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, '10 LET MIN = 0\nBad variable')

#  test matrix and function operations from primes.py

  def testRunExpression (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 OPTION BASE 1')
    commands.executeCommand('20 DIM PRIMES(10)')
    commands.executeCommand('30  PRIMES(1) = 2')
    commands.executeCommand('40 LET N = 5')
    commands.executeCommand('50 LET R = N - int(N / PRIMES(1)) * PRIMES(1)')    
    result = commands.executeCommand('RUN')    
    self.assertEqual(result, 'Done')    
    self.assertEqual(data.matrixList['PRIMES']['dim'], [10])
    self.assertEqual(data.variables['PRIMES'], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    self.assertEqual(data.variables['R'], 1)

#  test load data function

  def testLoadData(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 A = 1')    
    commands.executeCommand('20 STOP')
    commands.executeCommand('30  DATA 1, 2, 3, 4')
    scanner.createIndex()
    result = runtime.loadData()
    self.assertEqual(result, 'OK')    
    self.assertEqual(data.dataList, [1, 2, 3, 4])

#  test break

  def testBreak(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 A = 1')    
    commands.executeCommand('20 BREAK')
    commands.executeCommand('30  B = A + 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 30')    
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(len(data.variables), 1)

#  test break with line number

  def testBreakWithLine(self):
    commands.executeCommand('NEW')
    commands.executeCommand('5 BREAK 20')
    commands.executeCommand('10 A = 1')    
    commands.executeCommand('20 LET B = A + 1')
    commands.executeCommand('30  C = B + 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 20')    
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(len(data.variables), 1)

#  test continue

  def testContinue(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 A = 1')    
    commands.executeCommand('20 BREAK')
    commands.executeCommand('30  B = A + 1')
    commands.executeCommand('40  C = B + 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 30')    
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(data.address, 30)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.variables), 3)
    self.assertEqual(data.variables['C'], 3)

#  test break using line number

  def testBreakContinue(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 BREAK 30')
    commands.executeCommand('20 A = 1')
    commands.executeCommand('30  B = A + 1')
    commands.executeCommand('40  C = B + 1')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Break 30')    
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(data.address, 30)
    result = commands.executeCommand('CONTINUE')
    self.assertEqual(result, 'Done')
    self.assertEqual(len(data.variables), 3)
    self.assertEqual(data.variables['C'], 3)

#  test user defined functions

  def testUserFunction(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 DEF SQK(X) = X * X')
    commands.executeCommand('20 A = SQK(5)')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')    
    self.assertEqual(data.variables['A'], 25)

#  test user defined function with no argument

  def testUserFunction2(self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 DEF PI4() = 3.1416')
    commands.executeCommand('20 P = PI4()')
    result = commands.executeCommand('RUN')
    self.assertEqual(result, 'Done')    
    self.assertEqual(data.variables['P'], 3.1416)



if __name__ == '__main__':  
    unittest.main()
    