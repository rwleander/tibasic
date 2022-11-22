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
    data.codeList = ['10 Let A = 1']
    data.variables = {'I': 10}
    data.strings = {'msg': 'This is a message'}
    self.assertEqual(len(data.codeList), 1)
    self.assertEqual(len(data.variables), 1)
    self.assertEqual(len(data.strings), 1)
    rslt = commands.executeCommand('NEW')
    self.assertEqual(len(data.codeList), 0)
    self.assertEqual(len(data.variables), 0)
    self.assertEqual(len(data.strings), 0)
    self.assertEqual(rslt, 'OK')
  
  def testList (self):
    data.codeList = {10: '10 Let A = 1', 20: '20 Let B = 30', 30: '30 Let C = A + B'}
    rslt = commands.executeCommand('LIST')
    self.assertEqual(rslt, '10 Let A = 1\n20 Let B = 30\n30 Let C = A + B')
    
  def testListNotOrdered (self):
    data.codeList = {20: '20 Let A = 1', 10: '10 Let B = 30', 30: '30 Let C = A + B'}
    rslt = commands.executeCommand('LIST')
    self.assertEqual(rslt, '10 Let B = 30\n20 Let A = 1\n30 Let C = A + B')
  

  
if __name__ == '__main__':  
    unittest.main()
    