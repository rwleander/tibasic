#  test for parser functions

import unittest

import parser
import commands
import data

class TestParser(unittest.TestCase):

# test parser - no code

  def testParserNoCode (self):
    commands.executeCommand('NEW')
    rslt = parser.parse()    
    self.assertEqual(rslt, 'No code')

#  test create index

  def testCreateIndex (self):
    commands.executeCommand('NEW')
    data.codeList[10] = '10 LET A = 1'
    data.codeList[20] = '20 LET B = 2'
    data.codeList[30] = '30 LET C = A + B'
    rslt = parser.createIndex()
    self.assertEqual(rslt, 'OK')
    self.assertEqual(data.index, [10, 20, 30]) 
    self.assertEqual(data.firstLine, 10)
    
 # test build parse list
 
  def testBuildParseList (self):
    commands.executeCommand('NEW')
    data.codeList[10] = '10 LET A = 1'
    data.codeList[20] = '20 LET B = 2'
    data.codeList[30] = '30 LET C = A + B'
    rslt = parser.createIndex()
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.index), 3)
    rslt = parser.buildParseList()
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.parseList), 3)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 LET A = 1', 'statement': 'LET', 'nextLine': 20, 'error': 'OK'})
    item2 = data.parseList[20]
    self.assertEqual(item2, {'code': '20 LET B = 2', 'statement': 'LET', 'nextLine': 30, 'error': 'OK'})
    item3 = data.parseList[30]
    self.assertEqual(item3, {'code': '30 LET C = A + B', 'statement': 'LET', 'nextLine': -1, 'error': 'OK'})
 
 # test simple parse 

  def testParserSimple (self):
    commands.executeCommand('NEW')
    data.codeList[10] = '10 LET A = 1'
    data.codeList[20] = '20 LET B = 2'
    data.codeList[30] = '30 LET C = A + B'
    rslt = parser.parse()    
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.codeList), 3)
    self.assertEqual(len(data.index), 3)
    self.assertEqual(len(data.parseList), 3)
    self.assertEqual(data.firstLine, 10)


# test parse let statement


  def testParserLet (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 Let A = 1')
    commands.executeCommand('20 Let B = A + 1')
    rslt = parser.parse()    
    self.assertEqual(rslt, 'OK')
    self.assertEqual(len(data.parseList), 2)
    self.assertEqual(data.firstLine, 10)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 LET A = 1', 'statement': 'LET', 'nextLine': 20, 'part1': 'A', 'part2': '1', 'error': 'OK'}) 
    item2 = data.parseList[20]
    self.assertEqual(item2, {'code': '20 LET B = A + 1', 'statement': 'LET', 'nextLine': -1, 'part1': 'B', 'part2': 'A + 1', 'error': 'OK'}) 
    
#  test bad let statements

  def testParserLetErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 Let') 
    commands.executeCommand('20 Let B') 
    commands.executeCommand('30 Let C A + B') 
    rslt = parser.parse()    
    self.assertEqual(len(data.parseList), 3)
    item1 = data.parseList[10]
    self.assertEqual(item1['error'], 'Missing arguments') 
    item2 = data.parseList[20]
    self.assertEqual(item2['error'], 'Missing arguments') 
    item3 = data.parseList[30]
    self.assertEqual(item3['error'], 'Missing =') 

# test parse print

  def testParserPrint (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 PRINT A')
    commands.executeCommand('20 Print A * B / 2 * A + 2 * B') 
    rslt = parser.parse()    
    self.assertEqual(len(data.parseList), 2)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 PRINT A', 'statement': 'PRINT', 'nextLine': 20, 'part1': 'A', 'error': 'OK'}) 
    item2 = data.parseList[20]
    self.assertEqual(item2, {'code': '20 PRINT A * B / 2 * A + 2 * B', 'statement': 'PRINT', 'nextLine': -1, 'part1': 'A * B / 2 * A + 2 * B', 'error': 'OK'}) 

#  test bad print statements

  def testParserPrintErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 PRINT ')
    rslt = parser.parse()    
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]

# test parse if statement


  def testParserIf (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 IF True THEN 40')
    commands.executeCommand('20 IF A > B THEN 40')
    commands.executeCommand('30 IF B > A + 1 THEN 40 ELSE 10')
    commands.executeCommand('40 PRINT A')
    rslt = parser.parse()    
    self.assertEqual(len(data.parseList), 4)
    item1 = data.parseList[10]
    self.assertEqual(item1['part1'], 'TRUE')
    self.assertEqual(item1['part2'], '40')
    self.assertEqual(item1['part3'], '20')
    item2 = data.parseList[20]
    self.assertEqual(item2['part1'], 'A > B')
    self.assertEqual(item2['part2'], '40')
    self.assertEqual(item2['part3'], '30')
    item3 = data.parseList[30]
    self.assertEqual(item3['part1'], 'B > A + 1')
    self.assertEqual(item3['part2'], '40')
    self.assertEqual(item3['part3'], '10')
    
# test if with errors

  def testParserIfWithErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 IF') 
    commands.executeCommand('20 IF THEN 40')
    commands.executeCommand('30 IF B > A + 1 THEN 25')
    commands.executeCommand('40 PRINT A')
    rslt = parser.parse()    
    self.assertEqual(len(data.parseList), 4)
    item1 = data.parseList[10]
    self.assertEqual(item1['error'], 'Missing arguments')
    item2 = data.parseList[20]
    self.assertEqual(item2['error'], 'Missing expression')
    item3 = data.parseList[30]
    self.assertEqual(item3['error'], 'Unknown line number')
    
    
 
  
if __name__ == '__main__':  
    unittest.main()
    