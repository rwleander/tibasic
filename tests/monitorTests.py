#  test for monitor module

import unittest

import data
import monitor

class TestMonitor(unittest.TestCase):

# test the quit function

  def testQuit (self):
    self.assertEqual(data.quitFlag, False)
    monitor.executeCommand('quit')
    self.assertEqual(data.quitFlag, True)
  
  
  
if __name__ == '__main__':  
    unittest.main()
    