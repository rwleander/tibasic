#  test for helpers module

import unittest

import helpers
import commands
import data

class TestHelper(unittest.TestCase):

# test isnumeric  

  def testIsNumericQuit (self):
    rslt = helpers.isnumeric('12345')
    self.assertEqual(rslt, True)
    rslt = helpers.isnumeric('123xx')
    self.assertEqual(rslt, False)
    rslt = helpers.isnumeric('-1')
    self.assertEqual(rslt, True)

# test parse file name function

  def testParseFiile (self):
    [fileName, rslt] = helpers.parseFileName('OPEN TESTFILE')
    self.assertEqual(rslt, 'OK')
    self.assertEqual(fileName, 'TESTFILE.ti')

  def testParseMissingFiile (self):
    [fileName, rslt] = helpers.parseFileName('OPEN')
    self.assertEqual(rslt, 'Missing file name')
    self.assertEqual(fileName, '')

  def testParseTooManyFiles (self):
    [fileName, rslt] = helpers.parseFileName('OPEN TEST1 TEST2')
    self.assertEqual(rslt, 'Too many arguments')
    self.assertEqual(fileName, '')

# test file exists function

  def testExists (self):
    rslt = commands.executeCommand('New')
    rslt = commands.executeCommand('10 Let A = 1')
    rslt = commands.executeCommand('20 Let B = 2')
    rslt = commands.executeCommand('30 Let C = A+ B')
    rslt = commands.executeCommand('Save TESTFILE1')
    self.assertEqual(rslt, 'OK')    
    rslt = helpers.fileExists('TESTFILE1.ti')
    self.assertEqual(rslt, True)

# test valid variable name

  def testValidVariable (self):
    rslt = helpers.isValidVariable('AB2')
    self.assertEqual(rslt, True)
    rslt = helpers.isValidVariable('12A')
    self.assertEqual(rslt, False)
    rslt = helpers.isValidVariable('$ABC')
    self.assertEqual(rslt, False)
    rslt = helpers.isValidVariable('ABC$')
    self.assertEqual(rslt, True)
    rslt = helpers.isValidVariable('')
    self.assertEqual(rslt, False)


if __name__ == '__main__':  
    unittest.main()
    