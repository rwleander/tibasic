#  test for parser functions

import unittest

import parser
import commands
import data

class TestParser(unittest.TestCase):

# test parser - no code

  def testParserNoCode (self):
    commands.executeCommand('NEW')
    result = parser.parse()    
    self.assertEqual(result, 'No code')

#  test create index

  def testCreateIndex (self):
    commands.executeCommand('NEW')
    data.codeList[10] = '10 LET A = 1'
    data.codeList[20] = '20 LET B = 2'
    data.codeList[30] = '30 LET C = A + B'
    result = parser.createIndex()
    self.assertEqual(result, 'OK')
    self.assertEqual(data.index, [10, 20, 30]) 
    self.assertEqual(data.firstLine, 10)
    
 # test build parse list
 
  def testBuildParseList (self):
    commands.executeCommand('NEW')
    data.codeList[10] = '10 LET A = 1'
    data.codeList[20] = '20 LET B = 2'
    data.codeList[30] = '30 LET C = A + B'
    result = parser.createIndex()
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.index), 3)
    result = parser.buildParseList()
    self.assertEqual(result, 'OK')
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
    result = parser.parse()    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    self.assertEqual(len(data.index), 3)
    self.assertEqual(len(data.parseList), 3)
    self.assertEqual(data.firstLine, 10)


# test parse let statement


  def testParserLet (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 Let A = 1')
    commands.executeCommand('20 Let B = A + 1')
    result = parser.parse()    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.parseList), 2)
    self.assertEqual(data.firstLine, 10)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 LET A = 1', 'statement': 'LET', 'nextLine': 20, 'var': 'A', 'expr': '1', 'error': 'OK'}) 
    item2 = data.parseList[20]
    self.assertEqual(item2, {'code': '20 LET B = A + 1', 'statement': 'LET', 'nextLine': -1, 'var':'B', 'expr': 'A + 1', 'error': 'OK'}) 
    
#  test bad let statements

  def testParserLetErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 Let') 
    commands.executeCommand('20 Let B') 
    commands.executeCommand('30 Let C A + B') 
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 3)
    item1 = data.parseList[10]
    self.assertEqual(item1['error'], 'Missing expression') 
    item2 = data.parseList[20]
    self.assertEqual(item2['error'], 'Missing =') 
    item3 = data.parseList[30]
    self.assertEqual(item3['error'], 'Missing =') 

#  test implied let

  def testParserImpliedLet (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 A = 1')
    commands.executeCommand('20 B = A + 1')
    result = parser.parse()    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.parseList), 2)
    self.assertEqual(data.firstLine, 10)
    item1 = data.parseList[10]
    self.assertEqual({'code': '10 A = 1', 'statement': 'LET', 'nextLine': 20, 'var': 'A', 'expr': '1', 'error': 'OK'}, item1) 
    item2 = data.parseList[20]
    self.assertEqual(len(item2), 6)
    self.assertEqual({'code': '20 B = A + 1', 'statement': 'LET', 'nextLine': -1, 'var':'B', 'expr': 'A + 1', 'error': 'OK'}, item2) 
    

# test parse print

  def testParserPrint (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 PRINT A')
    commands.executeCommand('20 Print A * B / 2 * A + 2 * B') 
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 2)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 PRINT A', 'statement': 'PRINT', 'nextLine': 20, 'expr': 'A', 'error': 'OK'}) 
    item2 = data.parseList[20]
    self.assertEqual(item2, {'code': '20 PRINT A * B / 2 * A + 2 * B', 'statement': 'PRINT', 'nextLine': -1, 'expr': 'A * B / 2 * A + 2 * B', 'error': 'OK'}) 

#  test bad print statements

  def testParserPrintErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 PRINT ')
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]

# test parse if statement


  def testParserIf (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 IF True THEN 40')
    commands.executeCommand('20 IF A > B THEN 40')
    commands.executeCommand('30 IF B > A + 1 THEN 40 ELSE 10')
    commands.executeCommand('40 PRINT A')
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 4)
    item1 = data.parseList[10]
    self.assertEqual(item1['expr'], 'TRUE')
    self.assertEqual(item1['line1'], '40')
    item2 = data.parseList[20]
    self.assertEqual(item2['expr'], 'A > B')
    self.assertEqual(item2['line1'], '40')    
    item3 = data.parseList[30]
    self.assertEqual(item3['expr'], 'B > A + 1')
    self.assertEqual(item3['line1'], '40')
    self.assertEqual(item3['line2'], '10')
    
# test if with errors

  def testParserIfWithErrors (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 IF') 
    commands.executeCommand('20 IF THEN 40')
    commands.executeCommand('30 IF B > A + 1 THEN 25')
    commands.executeCommand('40 PRINT A')
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 4)
    item1 = data.parseList[10]
    self.assertEqual(item1['error'], 'Missing expression')
    item2 = data.parseList[20]    
    #self.assertEqual(item2['error'], 'Missing expression')
    self.assertEqual(item2['error'], 'OK')
    item3 = data.parseList[30]
    self.assertEqual(item3['error'], 'OK')

# test stop

  def testParserStop (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 STOP')
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1, {'code': '10 STOP', 'statement': 'STOP', 'nextLine': -1, 'error': 'OK'})
    
    #  test data statement

  def testParserData (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 DATA 1, 2, 3, 4, 5')
    result = parser.parse()    
    self.assertEqual(len(data.parseList), 1)
    item1 = data.parseList[10]
    self.assertEqual(item1['code'], '10 DATA 1, 2, 3, 4, 5')
    self.assertEqual(item1['statement'], 'DATA')
    self.assertEqual(item1['list'], '1, 2, 3, 4, 5')
    self.assertEqual(item1['data'], ['1', '2', '3', '4', '5'])
    
    
    
    
    #------------------
    #  lower level tests
    
    
# test add expression function using print statement

  def testAddExpressions (self):
    item = {'code': 'PRINT X'}
    ruleParts = ['PRINT', 'expr']    
    codeParts = ['PRINT', 'X']
    newItem = parser.addExpressions(item, ruleParts, codeParts)    
    self.assertEqual(len(newItem), 2)
    self.assertEqual(newItem, {'code': 'PRINT X', 'expr': 'X'})

# test add expressions using let statement

  def testAddExpressions2 (self):
    item = {'code': 'LET A = B + 2'}
    ruleParts = ['LET', 'var', '=', 'expr']
    codeParts = ['LET', 'A', '=','B + 2']
    newItem = parser.addExpressions(item, ruleParts, codeParts)    
    self.assertEqual(len(newItem), 3)
    self.assertEqual(newItem, {'code': 'LET A = B + 2', 'var': 'A', 'expr': 'B + 2'})

# test with bad let statement

  def testAddExpressions2WithError (self):
    item = {'code': 'LET A B + 2'}
    ruleParts = ['LET', 'var', '=', 'expr']
    codeParts = ['LET', 'A B + 2', '','']
    newItem = parser.addExpressions(item, ruleParts, codeParts)    
    self.assertEqual(len(newItem), 3)
    self.assertEqual(newItem, {'code': 'LET A B + 2', 'var': 'A B + 2', 'error': 'Missing =',})
    
# test split code functions with  prrint statement 

  def testSplitCode (self):
    code = '10 PRINT X'
    ruleParts = ['PRINT', 'expr']    
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 2)
    self.assertEqual(codeParts, ['PRINT', 'X'])

# test with let statement

  def testSplitCode2 (self):
    code = '10 LET A = B + 2'
    ruleParts = ['LET', 'var', '=', 'expr']    
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 4)
    self.assertEqual(codeParts, ['LET', 'A', '=', 'B + 2'])

# test with bad let statement

  def testSplitCode2WithErrors (self):
    code = '10 LET A B + 2'
    ruleParts = ['LET', 'var', '=', 'expr']    
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 3)
    self.assertEqual(codeParts, ['LET', 'A B + 2', ''])

# test if / then

  def testSplitCode3 (self):
    code = '10 IF A > B THEN 40 ELSE 10'
    ruleParts = ['IF', 'expr', 'THEN', 'line1', '[', 'ELSE', 'line2', ']'] 
    codeParts=  parser.splitCode(code, ruleParts)
    self.assertEqual(len(codeParts), 6)
    self.assertEqual(codeParts, ['IF', 'A > B', 'THEN', '40', 'ELSE', '10'])

#  test parse inputs

  def testParseInput (self):
    data.codeList = {10: '10 INPUT A, B, C'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.parseList), 1)
    item = data.parseList[10]
    self.assertEqual(item['statement'], 'INPUT')
    self.assertEqual(item['list'], 'A, B, C')
    self.assertEqual(item['prompt'], '?')
    self.assertEqual(item['inputs'], ['A', 'B', 'C'])
    self.assertEqual(item['error'], 'OK')

  def testParseInput2 (self):
    data.codeList = {10: '10 INPUT "Numbers:": A, B, C'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.parseList), 1)
    item = data.parseList[10]
    self.assertEqual(item['statement'], 'INPUT')
    self.assertEqual(item['list'], '"Numbers:": A, B, C')
    self.assertEqual(item['prompt'], 'Numbers:')
    self.assertEqual(item['inputs'], ['A', 'B', 'C'])
    self.assertEqual(item['error'], 'OK')
    
  
if __name__ == '__main__':  
    unittest.main()
    