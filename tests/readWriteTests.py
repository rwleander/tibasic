#  test for read and write functions 

import unittest

import readWrite
import commands
import scanner
import data

class TestReadWrite(unittest.TestCase):

# test save then load code file

  def testSaveCodeFile (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 REM TEST File')
    commands.executeCommand('20 LET A = 1')
    commands.executeCommand('30 LET B = 2')
    result = readWrite.saveCodeFile('TESTFILE.ti')    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    
    commands.cmdNew('NEW')
    result = readWrite.loadCodeFile('TESTFILE.ti')
    self.assertEqual(len(data.codeList), 3)
    
    result = readWrite.deleteCodeFile('TESTFILE.ti')
    self.assertEqual(result, 'OK')
    
    commands.cmdNew('NEW')
    result = readWrite.loadCodeFile('TESTFILE.ti')
    self.assertEqual(result, 'No data found')
    
    #  test print initializer

  def testInitPrint (self):    
    item = readWrite.initPrint(56, 14)
    self.assertEqual(item['buff'], '')
    self.assertEqual(item['lines'], [])
    self.assertEqual(item['width'], 56)
    self.assertEqual(item['tab'], 14)
       
    
#  test print formatter

  def testFormatPrint (self):    
    pWork = readWrite.initPrint(56, 14)
    item = scanner.parseCommand('10 Print 1 + 2; 3 + 4')
    list = item['list']
    self.assertEqual(list, ['1', '+', '2', ';', '3', '+', '4'])
    result = readWrite.formatPrint(pWork, list)
    self.assertEqual(result[0], '3 7')

#  test comma delimiters in print

  def testFormatPrint2 (self):    
    pWork = readWrite.initPrint(15, 5)
    item = scanner.parseCommand('10 Print 1, 2, 3, 4, 5')
    list = item['list']
    lines = readWrite.formatPrint(pWork, list)
    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], '1    2    3')
    self.assertEqual(lines[1], '4    5')

#  test strings with commas

  def testFormatPrint3 (self):    
    pWork = readWrite.initPrint(15, 5)
    item = scanner.parseCommand('10 Print "1234567", "890"')
    list = item['list']
    lines = readWrite.formatPrint(pWork, list)
    self.assertEqual(len(lines), 1)
    self.assertEqual(lines[0], '1234567   890')

#  test trailing comma

  def testFormatPrint4 (self):    
    pWork = readWrite.initPrint(15, 5)
    item = scanner.parseCommand('10 Print 1, 2, 3, 4,')
    list = item['list']
    lines = readWrite.formatPrint(pWork, list)
    self.assertEqual(len(lines), 1)
    self.assertEqual(lines[0], '1    2    3')
    lines = readWrite.formatPrint(pWork, [])
    self.assertEqual(len(lines), 1)
    self.assertEqual(lines[0], '4    ')

#  test load input function

  def testFormatPrint5 (self):    
    pWork = readWrite.initPrint(15, 5)
    item = scanner.parseCommand('10 Print 5 > 2')
    list = item['list']
    lines = readWrite.formatPrint(pWork, list)
    self.assertEqual(len(lines), 1)
    self.assertEqual(lines[0], 'True')

#  test file list

  def testLoadInput (self):    
    commands.executeCommand('NEW')
    vars = ['A', ',', 'B', ',', 'C']
    txt = '1, 2, 3'
    result = readWrite.loadInput(vars, txt)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)

#  test string input

  def testLoadInputString (self):    
    commands.executeCommand('NEW')
    vars = ['C$']
    txt = 'a' 
    result = readWrite.loadInput(vars, txt)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['C$'], 'a')

  def testListFiles (self):    
    printArea = readWrite.listFiles()
    self.assertEqual(printArea['error'], 'OK')
    self.assertTrue(len(printArea['lines']) > 0)
    



  
if __name__ == '__main__':  
    unittest.main()
    