#  test for resequencer functions

import unittest

import resequencer
import commands
import scanner
import language
import data

class TestResequencer(unittest.TestCase):

#  test get new line from cross reference

  def testGetNewLine (self):
    xref = {10: 110, 20: 120, 30: 130}
    result = resequencer.getNewLine(xref, 20)
    self.assertEqual(result, 120)
    result = resequencer.getNewLine(xref, 50)
    self.assertEqual(result, language.maxLine)

#  test get new text from cross reference

  def testGetNewText (self):
    xref = {10: 110, 20: 120, 30: 130}
    result = resequencer.getNewText(xref, '30')
    self.assertEqual(result, '130')
    result = resequencer.getNewText(xref, '')
    self.assertEqual(result, str(language.maxLine))


    #  test create cross reference
    
  def testCreateXref (self):
    index = [10, 20, 30]
    xref = resequencer.createXref(index, 100, 10)
    self.assertEqual(len(xref), 3)    
    self.assertEqual(xref[10], 100)
    self.assertEqual(xref[20], 110)
    self.assertEqual(xref[30], 120)

    #  test replace line number
        
  def testReplaceLineNumber (self):
    xref = {10: 110, 20: 120, 30: 130}
    newCode = resequencer.replaceLineNumber(xref, '20 A = 5', 120)
    self.assertEqual(newCode, '120 A = 5')
    newCode = resequencer.replaceLineNumber(xref, '30', 130)
    self.assertEqual(newCode, '130')
    
    #  test replace if
    
  def testReplaceIf (self):
    xref = {10: 110, 20: 120, 30: 130, 40: 140, 50: 150}    
    code = '10 IF I = 10 THEN 30'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceIf(xref, code, item)
    self.assertEqual(newCode, '10 IF I = 10 THEN 130')        
    code = '10 IF I = 10 THEN 30 ELSE 50'
    item = scanner.parseCommand(code)    
    newCode = resequencer.replaceIf(xref, code, item)
    self.assertEqual(newCode, '10 IF I = 10 THEN 130 ELSE 150')

#  test replace line number in gosub
    
  def testReplaceGosub (self):
    xref = {10: 110, 20: 120, 30: 130, 40: 140, 50: 150}        
    code = '10 GOSUB 20'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceGosub(xref, code, item)
    self.assertEqual(newCode, '10 GOSUB 120')        
    code = '10 GO SUB 30'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceGosub(xref, code, item)
    self.assertEqual(newCode, '10 GO SUB 130')    
    code = '10 GOTO 40'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceGosub(xref, code, item)
    self.assertEqual(newCode, '10 GOTO 140')    
    code = '10 GO TO 20'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceGosub(xref, code, item)
    self.assertEqual(newCode, '10 GO TO 120')

#  test replace line numbers after on gosub
    
  def testReplaceOnGosub (self):
    xref = {10: 110, 20: 120, 30: 130, 40: 140, 50: 150, 50: 150, 60: 160, 70: 170}        
    code = '10 ON I GOSUB 20, 30, 40, 50'
    item = scanner.parseCommand(code)
    newCode = resequencer.replaceOnGosub(xref, code, item)
    self.assertEqual(newCode, '10 ON I GOSUB 120, 130, 140, 150')

# test  resequence

  def testResequence (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 1')
    commands.executeCommand('20 LET B = 2')
    commands.executeCommand('30 LET C = A + B')
    result = resequencer.resequence(110, 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    self.assertEqual(data.codeList[110], {'code': '110 LET A = 1', 'next': -1})
    self.assertEqual(data.codeList[120], {'code': '120 LET B = 2', 'next': -1})
    self.assertEqual(data.codeList[130], {'code': '130 LET C = A + B', 'next': -1})

#  test resequence with gosob, etc

  def testResequence1 (self):
    commands.executeCommand('NEW')
    commands.executeCommand('10 LET A = 1')
    commands.executeCommand('20 IF A > 4 THEN 80')
    commands.executeCommand('30 ON A GOTO 40, 50, 60, 70')    
    commands.executeCommand('40 A = A + 1')
    commands.executeCommand('50 A = A + 1')
    commands.executeCommand('60 A = A + 1')
    commands.executeCommand('70 GOTO 30')
    commands.executeCommand('80 STOP')    
    result = resequencer.resequence(110, 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 8)
    self.assertEqual(data.codeList[110], {'code': '110 LET A = 1', 'next': -1})
    self.assertEqual(data.codeList[120], {'code': '120 IF A > 4 THEN 180', 'next': -1})
    self.assertEqual(data.codeList[130], {'code': '130 ON A GOTO 140, 150, 160, 170', 'next': -1})
    

if __name__ == '__main__':  
    unittest.main()
    