#  test for text editor functions

import unittest

import editor
import data

class TestEditor(unittest.TestCase):

#  add / replace lines

#  add the first line

  def testAddLine (self):
    data.codeList = {}      
    result = editor.addLine(10, '10 A = 10')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, {10: '10 A = 10'})

#  replace a line

  def testAddLineReplace (self):
    data.codeList = {10: '10 X = 20'}      
    result = editor.addLine(10, '10 A = 10')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, {10: '10 A = 10'})

#  delete a line

  def testAddLineDelete (self):
    data.codeList = {10: '10 X = 20'}      
    result = editor.addLine(10, '10')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, {})

#  delete line not in list

  def testAddLineBadDelete (self):
    data.codeList = {10: '10 X = 20'}      
    result = editor.addLine(20, '20')
    self.assertEqual(result, 'Bad line number')
    
#------------------
#  test edit functions

#  test pre-edit - parse command and retrieve code

  def testPreEdit (self):
    data.codeList = {
      10: '10 A = 1',
      20: '20 B = 2'
    }
    [n, code, msg] = editor.preEdit('EDIT 10')
    self.assertEqual(n, 10)
    self.assertEqual(code, 'A = 1')
    self.assertEqual(msg, 'OK')    
    [n, code, msg] = editor.preEdit('EDIT')
    self.assertEqual(msg, 'Bad command')        
    [n, code, msg] = editor.preEdit('EDIT 15')
    self.assertEqual(msg, 'Bad command')    
    [n, code, msg] = editor.preEdit('EDIT xx')
    self.assertEqual(msg, 'Bad command')

    
#  test edit function

  def testEdit (self):
    result = editor.edit('ABCDEFG', '   DDD')
    self.assertEqual(result, 'ABCG')
    result = editor.edit('ABCDEFG', 'DDD')
    self.assertEqual(result, 'DEFG')
    result = editor.edit('ABCDEFG', '   i123')
    self.assertEqual(result, 'ABC123DEFG')
    result = editor.edit('ABCDEFG', '   R123')
    self.assertEqual(result, 'ABC123G')
    result = editor.edit('ABCDEFG', '   123')
    self.assertEqual(result, 'ABC123G')







#------------------
#  resequence tests

#  test basic resequence

  def testResequence (self):
    data.codeList = {
      10: '10 N = 0',
      20: '20 FOR I = 1 to 10',
      30: '30 N = N + 1',
      40: '40 NEXT',
      50: '50 PRINT N'
    }
    
    newList = {
      100: '100 N = 0',
      110: '110 FOR I = 1 to 10',
      120: '120 N = N + 1',
      130: '130 NEXT',
      140: '140 PRINT N'
    }
    
    result = editor.resequence(100, 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, newList)

  def testResequenceGosub (self):
    data.codeList = {
      10: '10 N = 0',
      20: '20 FOR I = 1 to 10',
      30: '30 GOSUB 70',
      40: '40 NEXT',
      50: '50 PRINT N',
      60: '60 STOP',
      70: '70 N = N + 1',
      80: '80 RETURN'
    }
    
    newList = {
100: '100 N = 0',
      120: '120 FOR I = 1 to 10',
      140: '140 GOSUB 220',
      160: '160 NEXT',
      180: '180 PRINT N',
      200: '200 STOP',
      220: '220 N = N + 1',
      240: '240 RETURN'
    }    
    result = editor.resequence(100, 20)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, newList)
    
  def testResequenceIf (self):
    data.codeList = {
      10: '10 N = 0',
      20: '20 FOR I = 1 to 10',
      30: '30 IF N > 5 THEN 60',
      40: '40 N = N + 1',
      50: '50 GOTO 70',
      60: '60 N = N + 2',
      70: '70 NEXT',
      80: '80 PRINT N'
    }
    
    newList = {
      100: '100 N = 0',
      110: '110 FOR I = 1 to 10',
      120: '120 IF N > 5 THEN 150',
      130: '130 N = N + 1',
      140: '140 GOTO 160',
      150: '150 N = N + 2',
      160: '160 NEXT',
      170: '170 PRINT N'
    }
    result = editor.resequence(100, 10)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.codeList, newList)
    
  def testResequenceOnGoto (self):
    data.codeList = {
      10: '10 N = 0',
      20: '20 FOR I = 1 to 5',
      30: '30 ON i GOTO 40, 50, 60, 70, 80', 
      40: '40 N = N + 1',
      50: '50 N = N + 1',
      60: '60 N = N + 1',
      70: '70 N = N + 1',
80: '80 N = N + 1',
      90: '90 NEXT',
      100: '100 PRINT n'
    }
    
    newList = {
100: '100 N = 0',
      110: '110 FOR I = 1 to 5',
      120: '120 ON i GOTO 130, 140, 150, 160, 170',
      130: '130 N = N + 1',
      140: '140 N = N + 1',
      150: '150 N = N + 1',
      160: '160 N = N + 1',
170: '170 N = N + 1',
      180: '180 NEXT',
      190: '190 PRINT n'
    }    
    result = editor.resequence(100, 10)
    self.assertEqual(result, 'OK')    
    self.assertEqual(data.codeList, newList)
    
    

if __name__ == '__main__':  
    unittest.main()
    