#  test for monitor module

import unittest

import data
import commands

class TestMonitor(unittest.TestCase):

# test the quit function

  def testQuit (self):
    self.assertEqual(data.quitFlag, False)
    commands.executeCommand('quit')
    self.assertEqual(data.quitFlag, True)
  
  def testNew (self):
    data.codeList = {10: '10 Let A = 1'}
    data.variables = {'I': 10}
    data.strings = {'msg': 'This is a message'}
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(len(data.strings), 1)
    commands.executeCommand('NEW')
    self.assertEqual(len(data.codeList), 0)
    self.assertEqual(len(data.variables), 0)
    self.assertEqual(len(data.strings), 0)
  
  
if __name__ == '__main__':  
    unittest.main()
    