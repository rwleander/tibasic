#  test for helpers module

import unittest

import helpers
import commands
import data

class TestHelper(unittest.TestCase):

# test isnumeric  

  def testIsNumericQuit (self):
    result = helpers.isnumeric('12345')
    self.assertEqual(result, True)
    result = helpers.isnumeric('123xx')
    self.assertEqual(result, False)
    result = helpers.isnumeric('-1')
    self.assertEqual(result, True)

# test parse file name function

  def testParseFiile (self):
    [fileName, result] = helpers.parseFileName('OPEN TESTFILE')
    self.assertEqual(result, 'OK')
    self.assertEqual(fileName, 'TESTFILE.ti')

  def testParseMissingFiile (self):
    [fileName, result] = helpers.parseFileName('OPEN')
    self.assertEqual(result, 'Missing file name')
    self.assertEqual(fileName, '')

  def testParseTooManyFiles (self):
    [fileName, result] = helpers.parseFileName('OPEN TEST1 TEST2')
    self.assertEqual(result, 'Too many arguments')
    self.assertEqual(fileName, '')

# test file exists function

  def testExists (self):
    result = commands.executeCommand('New')
    result = commands.executeCommand('10 Let A = 1')
    result = commands.executeCommand('20 Let B = 2')
    result = commands.executeCommand('30 Let C = A+ B')
    result = commands.executeCommand('Save TESTFILE1')
    self.assertEqual(result, 'OK')    
    result = helpers.fileExists('TESTFILE1.ti')
    self.assertEqual(result, True)

# test valid variable name

  def testValidVariable (self):
    result = helpers.isValidVariable('AB2')
    self.assertEqual(result, True)
    result = helpers.isValidVariable('12A')
    self.assertEqual(result, False)
    result = helpers.isValidVariable('$ABC')
    self.assertEqual(result, False)
    result = helpers.isValidVariable('ABC$')
    self.assertEqual(result, True)
    result = helpers.isValidVariable('THIS_NAME')
    self.assertEqual(result, True)
    result = helpers.isValidVariable('A@2')
    self.assertEqual(result, True)
    result = helpers.isValidVariable('STOP')
    self.assertEqual(result, False)
    result = helpers.isValidVariable('THIS_IS_TOO_LONG')
    self.assertEqual(result, False)
    result = helpers.isValidVariable('')
    self.assertEqual(result, False)

# variable ok if already in list

  def testValidVariable2 (self):
    data.variables['@BADNAME'] = 123    
    result = helpers.isValidVariable('@BADNAME')
    self.assertEqual(result, True)

#  test set variable function

  def testSetVariable (self):
    data.variables= {}
    result = helpers.setVariable('A', 2)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 2)
    result = helpers.setVariable('B', 3.1415)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['B'], 3.1415)
    result = helpers.setVariable('M$', 'Hello')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['M$'], 'Hello')

# test bad variable data

  def testSetBadVariable (self):
    data.variables= {}
    result = helpers.setVariable('A$', 2)
    self.assertEqual(result, 'Bad type')
    result = helpers.setVariable('B$', 3.1415)
    self.assertEqual(result, 'Bad type')
    result = helpers.setVariable('M', 'Hello')
    self.assertEqual(result, 'Bad type')

#  test upshift function


  def testUpshift (self):
    result = helpers.upshift ('10 let a = 100')    
    self.assertEqual(result, '10 LET A = 100')
    result = helpers.upshift('20 let s$ = "Hello world"')
    self.assertEqual(result, '20 LET S$ = "Hello world"')

# test addQuotes function

  def testAddQuotes (self):
    result = helpers.addQuotes('ABCDEFG')
    self.assertEqual(result, '"ABCDEFG"')
    result = helpers.addQuotes('')
    self.assertEqual(result, '""')

#  test strip quotes function

  def testStripQuotes (self):
    result = helpers.stripQuotes('"ABCDEFG"')
    self.assertEqual(result, 'ABCDEFG')
    result = helpers.stripQuotes(""'')
    self.assertEqual(result, '')





if __name__ == '__main__':  
    unittest.main()
    