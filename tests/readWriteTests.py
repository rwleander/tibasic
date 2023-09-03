#  test for read and write functions 

import unittest

import readWrite
import parser
import commands
import data

class TestReadWrite(unittest.TestCase):

# test save then load code file

  def testSaveCodeFile (self):
    commands.cmdNew('NEW')
    commands.cmdAddLine('10 REM TEST File')
    commands.cmdAddLine('20 LET A = 1')
    commands.cmdAddLine('30 LET B = 2')
    result = readWrite.saveCodeFile('TESTFILE.ti')    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    
    commands.cmdNew('NEW')
    result = readWrite.loadCodeFile('TESTFILE.ti')
    self.assertEqual(len(data.codeList), 3)
    self.assertEqual(len(data.codeList), 3)
    self.assertEqual(data.codeList[20], '20 LET A = 1')
    
#  test delete code file function
#  first, create a file, then delete it

  def testDeleteCodeFile (self):
    commands.cmdNew('NEW')
    commands.cmdAddLine('10 REM TEST File')
    commands.cmdAddLine('20 LET A = 1')
    commands.cmdAddLine('30 LET B = 2')
    result = readWrite.saveCodeFile('TESTFILE.ti')    
    self.assertEqual(result, 'OK')
    self.assertEqual(len(data.codeList), 3)
    
    result = readWrite.deleteCodeFile('TESTFILE.ti')
    self.assertEqual(result, 'OK')
    result = readWrite.deleteCodeFile('TESTFILE.ti')
    self.assertEqual(result, 'No data found')
    
    #  test list of code files
        
  def testFiles (self):  
    result = readWrite.listCodeFiles()
    self.assertNotEqual(result, '') 
    
#  test open then close

  def testOpenCloseFile (self):
    commands.executeCommand('NEW')      
    data.codeList = {10: '10 OPEN #12, "TESTFILE", SEQUENTIAL, INTERNAL, OUTPUT, VARIABLE 120, TEMPORARY'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')
    item1 = data.parseList[10]    
    readWrite.openFile(item1)
    self.assertEqual(item1['error'], 'OK')
    self.assertEqual(len(data.fileList), 1)    
    self.assertEqual(len(data.fileList), 1)    
    file1 = data.fileList[12]        
    self.assertEqual(file1['fileNum'], 12)
    self.assertEqual(file1['fileName'], 'TESTFILE.dat')
    self.assertEqual(file1['fileOrg'], 'S')
    self.assertEqual(file1['maxRecs'], 0)
    self.assertEqual(file1['fileType'], 'I')
    self.assertEqual(file1['fileMode'], 'O')
    self.assertEqual(file1['recType'], 'V')
    self.assertEqual(file1['recWidth'], 120)
    self.assertEqual(file1['life'], 'T')    
    
    data.codeList = {20: '20 CLOSE #12'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')        
    item2 = data.parseList[20]    
    readWrite.closeFile(item2)
    self.assertEqual(item1['error'], 'OK')
    self.assertEqual(len(data.fileList), 0)

#  test file open for read

  def testOpenCloseFileRead (self):
    commands.executeCommand('NEW')      
    data.codeList = {10: '10 OPEN #12, "TESTFILE", SEQUENTIAL, INTERNAL, INPUT, VARIABLE 120, TEMPORARY'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')
    item1 = data.parseList[10]    
    readWrite.openFile(item1)
    self.assertEqual(item1['error'], 'OK')
    self.assertEqual(len(data.fileList), 1)    
    self.assertEqual(len(data.fileList), 1)    
    file1 = data.fileList[12]        
    self.assertEqual(file1['fileNum'], 12)
    self.assertEqual(file1['fileName'], 'TESTFILE.dat')
    self.assertEqual(file1['fileOrg'], 'S')
    self.assertEqual(file1['maxRecs'], 0)
    self.assertEqual(file1['fileType'], 'I')
    self.assertEqual(file1['fileMode'], 'I')
    self.assertEqual(file1['recType'], 'V')
    self.assertEqual(file1['recWidth'], 120)
    self.assertEqual(file1['life'], 'T')    
    
    data.codeList = {20: '20 CLOSE #12'}
    result = parser.parse()  
    self.assertEqual(result, 'OK')        
    item2 = data.parseList[20]    
    readWrite.closeFile(item2)
    self.assertEqual(item1['error'], 'OK')
    self.assertEqual(len(data.fileList), 0)

#  test process input function

  def testProcessInput (self):
    vars = ['A', 'B', 'C']
    values = [1, 2, 3]
    result = readWrite.processInputs(vars, values)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)

  def testProcessInput2 (self):
    vars = ['A$', 'B$', 'C']
    values = ['Red', '"Blue"', '3']
    result = readWrite.processInputs(vars, values)
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A$'], '"Red"')
    self.assertEqual(data.variables['B$'], '"Blue"')
    self.assertEqual(data.variables['C'], 3)
    
# test input from string

  def testProcessInput3 (self):
    vars = ['A$', 'B$', 'C']    
    result = readWrite.processInputsFromString(vars, 'Red, "Blue", 3')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A$'], '"Red"')
    self.assertEqual(data.variables['B$'], '"Blue"')
    self.assertEqual(data.variables['C'], 3)

#  test split values

  def testSplitValues (self):
    result = readWrite.splitValues('1, 2, 3')
    self.assertEqual(result, ['1', '2', '3'])
    result = readWrite.splitValues('Red, "Blue", 3')
    self.assertEqual(result, ['Red', '"Blue"', '3'])

#  test process input from string function

  def testProcessInputsFromString (self):
    commands.cmdNew('NEW')    
    variables = ['A', 'B', 'C']
    result =  readWrite.processInputsFromString(variables, '1, 2, 3')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A'], 1)
    self.assertEqual(data.variables['B'], 2)
    self.assertEqual(data.variables['C'], 3)

#  test with empty string

  def testProcessInputsFromStringEmpty (self):
    commands.cmdNew('NEW')    
    variables = ['A$']
    result =  readWrite.processInputsFromString(variables, '')
    self.assertEqual(result, 'OK')
    self.assertEqual(data.variables['A$'], '""')
    
    
    
  
if __name__ == '__main__':  
    unittest.main()
    