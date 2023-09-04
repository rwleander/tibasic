#  test for scanner module

import unittest

import scanner
import commands
import language
import data

class TestScanner(unittest.TestCase):

# test  get token function

  def testFindTokens (self):
    result = scanner.findTokens('10 LET A = B + C')
    self.assertEqual(result, ['10', 'LET', 'A', '=', 'B', '+', 'C'])
    result = scanner.findTokens('20 LET A = (B * 2)  + C')
    self.assertEqual(result, ['20', 'LET', 'A', '=', '(', 'B', '*', '2', ')', '+', 'C'])
    result = scanner.findTokens('30 print a; b; c; d') 
    self.assertEqual(result, ['30', 'print', 'a', ';', 'b', ';', 'c', ';', 'd'])
    result = scanner.findTokens('40 print "Hello", "This is a test"')
    self.assertEqual(result, ['40', 'print', '"Hello"', ',', '"This is a test"'])
    result = scanner.findTokens('50 IF A <> B THEN 100 ELSE 200')
    self.assertEqual(result, ['50', 'IF', 'A', '<>', 'B', 'THEN', '100', 'ELSE', '200'])
    result = scanner.findTokens('60 LET A = 3 + 5')
    self.assertEqual(result, ['60', 'LET', 'A', '=', '3', '+', '5'])
    result = scanner.findTokens('2 * SQR(2 * 2) + 2')
    self.assertEqual(result, ['2', '*',  'SQR', '(', '2', '*', '2', ')',  '+', '2']) 


#  test get line number

  def testGetLineNumber (self):
    result = scanner.getLineNumber('1234')
    self.assertEqual(result, 1234)
    result = scanner.getLineNumber('1')
    self.assertEqual(result, 1)
    result = scanner.getLineNumber('32767')
    self.assertEqual(result, 32767)

#  test get line number with bad results

  def testGetLineNumberBad (self):
    result = scanner.getLineNumber('0')
    self.assertEqual(result, -1)
    result = scanner.getLineNumber('xxx')
    self.assertEqual(result, -1)
    result = scanner.getLineNumber('32768')
    self.assertEqual(result, -1)

#  test buildIndex

  def testBuildIndex (self):
    commands.executeCommand('NEW')
    commands.executeCommand('30 NEXT')
    commands.executeCommand('20 PRINT I')
    commands.executeCommand('10 FOR I = 1 TO 10')
    self.assertEqual(len(data.codeList), 3)
    index  = scanner.createIndex()    
    self.assertEqual(index, [10, 20, 30])
    self.assertEqual(data.firstLine, 10)
    self.assertEqual(data.codeList[10], {'code': '10 FOR I = 1 TO 10', 'next': 20})
    
#  test get statement name

  def testGetStatementName (self):  
    item = {}
    item['tokens'] = scanner.findTokens('RUN')
    result = scanner.getStatementName(item)
    self.assertEqual(result, 'RUN')    
    
    item['tokens'] = scanner.findTokens('10 IF A = 5 THEN 20')
    result = scanner.getStatementName(item)
    self.assertEqual(result, 'IF')
    
    item['tokens'] = scanner.findTokens('NUM 100, 10')
    result = scanner.getStatementName(item)
    self.assertEqual(result, 'NUMBER')
    
    item['tokens'] = scanner.findTokens('XYZZ')
    result = scanner.getStatementName(item)
    self.assertEqual(result, 'Bad command')
    
    
#  test parse command

  def testParseQuitCommand (self):
    result = scanner.parseCommand('QUIT')
    self.assertEqual(result, {'code': 'QUIT', 'statement': 'QUIT', 'tokens': ['QUIT'], 'error': 'OK'})
    
#  test bad command

  def testParseBadCommand (self):
    result = scanner.parseCommand('XYZ')
    self.assertEqual(result['error'], 'Bad command')

#  test parse of if statement

  def testParseIfCommand (self):
    item = scanner.parseCommand('10 IF A = 1 THEN 20')
    self.assertEqual(len(item), 7)
    self.assertEqual(item['code'], '10 IF A = 1 THEN 20')
    self.assertEqual(item['statement'], 'IF')
    self.assertEqual(item['expr'], ['A', '=', '1'])
    self.assertEqual(item['line1'], ['20'])
    self.assertEqual(item['line2'], [])
    self.assertEqual(item['error'], 'OK')

#  test if / else

  def testParseIfElseCommand (self):
    item = scanner.parseCommand('10 IF A = 1 THEN 20 ELSE 30')
    self.assertEqual(len(item), 7)    
    self.assertEqual(item['statement'], 'IF')
    self.assertEqual(item['expr'], ['A', '=', '1'])
    self.assertEqual(item['line1'], ['20'])
    self.assertEqual(item['line2'], ['30'])
    self.assertEqual(item['error'], 'OK')
    
    
#  test bad if statement

  def testParseBadIfCommand (self):
    item = scanner.parseCommand('10 IF A = 1 THN 20')
    self.assertEqual(item['code'], '10 IF A = 1 THN 20')
    self.assertEqual(item['statement'], 'IF')
    self.assertEqual(item['error'], 'Bad command')
    
#  test parse of let statement

  def testParseLetCommand (self):
    item = scanner.parseCommand('10 LET A = 3 + 5')
    self.assertEqual(len(item), 6)    
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(item['statement'], 'LET')
    self.assertEqual(item['var'], ['A'])
    self.assertEqual(item['expr'], ['3', '+', '5'])
    
#  test impled let

  def testParseImpliedLetCommand (self):
    item = scanner.parseCommand('10 A = 3 + 5')    
    self.assertEqual(len(item), 6)    
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(item['statement'], 'LET')
    self.assertEqual(item['var'], ['A'])
    self.assertEqual(item['expr'], ['3', '+', '5'])
    
#  test go to

  def testParseGoTo(self):
    item = scanner.parseCommand('10 GO TO 20')
    self.assertEqual(len(item), 5)    
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(item['statement'], 'GOTO')
    self.assertEqual(item['line'], ['20'])    

#  test on gosub

  def testParseOnGoSub(self):
    item = scanner.parseCommand('10 ON I GO SUB 20, 30, 40, 50')
    self.assertEqual(len(item), 6)    
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(item['statement'], 'ON_GOSUB')
    self.assertEqual(item['expr'], ['I'])        
    self.assertEqual(item['list'], ['20', ',', '30', ',', '40', ',', '50'])    

#  test find num

  def testParseNumber(self):
    item = scanner.parseCommand('NUM 20, 10')
    self.assertEqual(len(item), 5)    
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(item['statement'], 'NUMBER')
    self.assertEqual(item['sequence'], ['20', ',', '10'])
#  test get sequence with both values
    
  def testGetSequence(self):
    item = scanner.parseCommand('NUMBER 20, 5')
    self.assertEqual(item['sequence'], ['20', ',', '5'])
    [start, step] = scanner.getItemSequence(item, 'sequence', ',', language.defaultStart, language.defaultStep)
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(start, 20)
    self.assertEqual(step, 5)

     #  test get sequence - start only
         
  def testGetSequence1(self):
    item = scanner.parseCommand('NUMBER 20')
    [start, step] = scanner.getItemSequence(item, 'sequence', ',', language.defaultStart, language.defaultStep)
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(start, 20)
    self.assertEqual(step, language.defaultStep)
     
     #  test get sequence - step only
         
  def testGetSequence2(self):
    item = scanner.parseCommand('NUMBER ,5')
    [start, step] = scanner.getItemSequence(item, 'sequence', ',', language.defaultStart, language.defaultStep)
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(start, language.defaultStart)
    self.assertEqual(step, 5)
     
     #  test get sequence - no args
         
  def testGetSequence3(self):
    item = scanner.parseCommand('NUMBER')    
    [start, step] = scanner.getItemSequence(item, 'sequence', ',', language.defaultStart, language.defaultStep)
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(start, language.defaultStart)
    self.assertEqual(step, language.defaultStep)
    
#  test get sequence - bad arg
    
  def testGetSequence4(self):
    item = scanner.parseCommand('NUMBER 20x, 5')    
    [start, step] = scanner.getItemSequence(item, 'sequence', ',', language.defaultStart, language.defaultStep)
    
    self.assertEqual(item['error'], 'Bad argument')

#  test is numeric

  def testIsnumeric(self):
    self.assertEqual(scanner.isnumeric('12345'), True)
    self.assertEqual(scanner.isnumeric('12x45'), False)
    self.assertEqual(scanner.isnumeric('-12345.56'), True)
    self.assertEqual(scanner.isnumeric(''), False)

#  test valid variables

  def testIsValidVariable(self):
    self.assertEqual(scanner.isValidVariable('A'), True)
    self.assertEqual(scanner.isValidVariable('A1'), True)
    self.assertEqual(scanner.isValidVariable('1A'), False)
    self.assertEqual(scanner.isValidVariable('A12345678901234567890'), False)
    self.assertEqual(scanner.isValidVariable(''), False)
    
    #  test get parsed tokens
    
  def testGetItemTokens(self):
    item = scanner.parseCommand('10 ON I GO SUB 20, 30, 40, 50')
    self.assertEqual(len(item), 6)    
    tokens = scanner.getItemTokens(item, 'list')
    self.assertEqual(tokens, ['20', ',', '30', ',', '40', ',', '50'])
    
    #  test get parsed tokens with bad value
    
  def testGetItemTokensError(self):
    item = scanner.parseCommand('10 ON I GO SUB 20, 30, 40, 50')
    self.assertEqual(len(item), 6)    
    tokens = scanner.getItemTokens(item, 'l')
    self.assertEqual(item['error'],  'l not in list')
    self.assertEqual(tokens, [])
    
    #  test get parsed value
    
  def testGetItemValue(self):
    item = scanner.parseCommand('10 LET A = 2')
    self.assertEqual(len(item), 6)    
    value = scanner.getItemValue(item, 'var')
    self.assertEqual(value, 'A')

#  test get item expression value
    
  def testGetItemExpression(self):
    item = scanner.parseCommand('10 LET A = 2 * 3 + 1')
    value = scanner.getItemExpression(item, 'expr')
    self.assertEqual(value, 7)
#  test strip commas from list
    
  def testStripCommas(self):
    item = scanner.parseCommand('10 Data 1, 2, 3, 4, 5')    
    list = scanner.getItemData(item, 'list')
    self.assertEqual(item['error'], 'OK')
    self.assertEqual(list, [1, 2, 3, 4, 5])

#  test upshift tokens
    
  def testUpshiftTokens(self):
    tokens = scanner.upshiftTokens(['let', 'a' , '=', '"Hello"'])   
    self.assertEqual(tokens, ['LET', 'A', '=', '"Hello"'])
    
    
    

if __name__ == '__main__':  
    unittest.main()
    