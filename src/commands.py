#  commands - parse and run repl commands

import os

import data
import expressions
import parser
import runtime
import helpers

# process a command

def executeCommand(cmd):

  functionList = {
    'BYE': cmdQuit,
    'DELETE': cmdDelete,
    'FILES': cmdFiles,        
    'LIST': cmdList,
    'NEW': cmdNew,
    'OLD': cmdOld,    
    'QUIT': cmdQuit,
    'RESEQUENCE': cmdResequence,
    'RUN': cmdRun,
    'SAVE': cmdSave
  }

  commandList = ['DISPLAY', 'INPUT', 'LET', 'PRINT']

  cmdWork = helpers.upshift(cmd)
  parts = cmdWork.split()
  if len(parts) == 0:
    return ''

  command = parts[0]          
  if command in functionList:
    return functionList[command](cmdWork)
    
  if command in commandList:
    return cmdRunCommand(cmdWork)
        
  if command[0] >= '0' and cmdWork[0] <= '9':
    return cmdAddLine(cmdWork)
  
  return 'unknown command'
    

#------------------------------
#  code editing functions
    
#  NEW - clear lists
    
def cmdNew(cmdWork):
  data.codeList = {}
  data.variables = {}  
  data.parseList = {}
  data.index = []
  data.gosubStack = []
  data.forNextStack = []
  data.dataList = []
  data.dataPointer = 0
  data.printPosition = 0
  data.matrixList = {}
  data.matrixBase = 0
  
  return 'OK'

#  list code

def cmdList(cmdWork):
  str = ''  
  index = []  
  for i in data.codeList:
    index.append(i)
  index.sort()  
  
  [first, last, msg] = splitLinesForList(cmdWork, index[0], index[len(index) - 1])
  if msg != 'OK':
    return msg
    
  for lineNumber in index:
    if lineNumber >= first and lineNumber <= last:
      str = str + data.codeList[lineNumber] 
      if lineNumber < last:
        str = str + '\n'
      
  return str  
    
    
#  add or update a line of code

def cmdAddLine(cmd):
  parts = cmd.split()
  if helpers.isnumeric(parts[0]):
    lineNumber = int(parts[0])
  else:
    return 'Bad line number'
    
  if len(parts) > 1:
    data.codeList[lineNumber] = cmd
  else:
    if lineNumber in data.codeList:
      data.codeList.pop(lineNumber)    
    else:
      return 'Not in list'
  return 'OK'

# resequence the list

def cmdResequence(cmdWork):
  newCodeList = {}
  lineList = {}
  seq = 10
  
  for lineNumber in data.codeList:
    line = data.codeList[lineNumber]
    i = line.index(' ')    
    oldLine = line[0: i]
    newLine = str(seq) + line[i:len(line)]    
    newCodeList[seq] = newLine
    lineList[oldLine] = str(seq)
    seq = seq + 10
    
    # replace line numbers within statements
    
  for lineNumber in newCodeList:
    line = newCodeList[lineNumber]
    parts = line.split()
      
    if parts[1] == 'GOTO' or parts[1] == 'GOSUB':
      i = len(line) - len(parts[2])
      line = line[0: i] + lineList[parts[2]]
      newCodeList[lineNumber] = line
        
    elif parts[1] == 'IF':
      i1 = line.find('THEN')
      i2 = line.find('ELSE')
      firstPart = line[0: i1 + 5]
      if i2 > 0:
        oldnum1 = parts[len(parts) - 3]
        oldNum2 = parts[len(parts) - 1]
        newNum1 = lineList[oldNum1]
        newNum2 = lineList[oldNum2]
        line = firstPart + newNum1 + ' ELSE ' + newNum2
      else:
        oldNum1 = parts[len(parts) - 1]
        newNum1 = lineList[oldNum1]
        i  = len(line) - len(oldNum1)
        line = firstPart + newNum1
      newCodeList[lineNumber] = line
        
  data.codeList = newCodeList
  return 'OK'
  
  
  #-----------------------
  #  file operations
  
  # load a file
  
def cmdOld(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
    
  cmdNew(cmdWork)
  if helpers.fileExists(fileName) == False:
    return 'File not found'
    
  with open (fileName, 'r') as fl:
    while  (line := fl.readline().strip()):
      line = helpers.upshift(line)
      cmdAddLine(line)  
    fl.close()
 
  return 'OK'
  
  #  save a file
  
def cmdSave(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
        
  index = []
  for lineNumber in data.codeList:
    index.append(lineNumber)
  index.sort()  
  
  with open (fileName, 'w') as fl:
    for lineNumber in index:
      fl.write (data.codeList[lineNumber] + '\n')
    fl.close()
  return 'OK'
  
  # list files
  
def cmdFiles(cmdWork):
  str = ''
  n = 0
  files  = os.listdir()
  for file in files:
    i = file.find('.ti')
    j = file.find('\\')
    if (i > 0) and (j < 0): 
      str = str + file[0:i] + '\t'
      n = n + 1
  
  if n > 0:
    return str[0:len(str)-1]
  else:
    return 'No files'
    
    # delete file
    
def cmdDelete(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
    
  if helpers.fileExists(fileName) == False:
    return 'File not found'
    
  os.remove(fileName)
  return 'OK'
  
  
  #-----------------------
  #  other commands
 
 #  run the program
 
def cmdRun(cmdWork):
  return runtime.run()
 
#  run immediate commands like let, input, print, etc

def cmdRunCommand(cmdWork):
  item = parser.parseCommand(cmdWork)
  if item['error'] != 'OK':
    return item['error']

  addr = runtime.executeStatement(item)
  return item['error']
 
#  quit

def cmdQuit(cmdWork):
  data.quitFlag = True
  return 'Bye'
  
#-------------------
#  helper functions
  
# get first and last line number for list statement
  
def splitLinesForList(txt, min, max):
  numbers = "1234567890"
  line1 = ''
  line2 = ''
  num1 = min
  num2 = max
  msg = 'OK'
  beforeDash = True
 
  if txt == 'LIST':
    return [min, max, 'OK']
   
  for ch in txt:
    if ch in numbers:
      if beforeDash:
        line1 = line1 + ch
      else:
        line2 = line2 + ch
        
    if ch == '-':
      if beforeDash == False:
        return [-1, -1, 'Bad line numbers']
      else:
        beforeDash = False      

  if line1 != '':
    min = int(line1)
  
  if line2 != '':
    max = int(line2)
  
  if beforeDash:
    max = min
  
  return [min, max, 'OK']
    
  
 