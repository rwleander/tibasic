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


 
  
if __name__ == '__main__':  
    unittest.main()
    