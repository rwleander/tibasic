#  test for helpers module

import unittest

import helpers

class TestHelper(unittest.TestCase):

# test isnumeric  

  def testIsNumeriQuit (self):
    rslt = helpers.isnumeric('12345')
    self.assertEqual(rslt, True)
    rslt = helpers.isnumeric('123xx')
    self.assertEqual(rslt, False)

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



 
  
if __name__ == '__main__':  
    unittest.main()
    