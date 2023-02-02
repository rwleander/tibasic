#  commands - parse and run repl commands

import os

import data
import expressions
import parser
import editor
import runtime
import helpers

# process a command

def executeCommand(cmd):

  functionList = {
    'BYE': cmdQuit,    
    'CONTINUE': cmdContinue,
    'EDIT': cmdEdit,
    'DELETE': cmdDelete,
    'FILES': cmdFiles,        
    'LIST': cmdList,
    'NEW': cmdNew,
    'NUMBER': cmdNumber,
    'OLD': cmdOld,    
    'QUIT': cmdQuit,
    'RESEQUENCE': cmdResequence,
    'RUN': cmdRun,
    'SAVE': cmdSave
  }

  commandList = ['BREAK', 'DISPLAY', 'INPUT', 'LET', 'PRINT', 'STOP', 'UNBREAK']

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
  data.breakpointList = []
  data.matrixList = {}
  data.matrixBase = 0
  
  return 'OK'

#  list code

def cmdList(cmdWork):
  if len(data.codeList) == 0:
    return 'Can\'t do that'
    
  str = ''  
  parser. createIndex()
  
  [first, last, msg] = getNumbersForList(cmdWork, data.index[0], data.index[len(data.index) - 1])
  if msg != 'OK':
    return msg
    
  if first > data.index[len(data.index) - 1] or last < data.index[0]:
    return 'Bad line number'
      
  for lineNumber in data.index:
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
    
  return editor.addLine(lineNumber, cmd)
  
# resequence the list

def cmdResequence(cmdWork):
  seq = 100
  incr = 10
  
  if len(data.codeList) == 0:
    return 'Can\'t do that'
  
  [seq, incr, msg] = getNumbers(cmdWork, seq, incr)
  if msg != 'OK':
    return msg
  
  if seq + incr * len(data.codeList) > data.maxLine:
    return 'Bad line number\nNo line numbers in this program are change'
    
  msg = editor.resequence(seq, incr)
  return msg
    
  #-----------------------
  #  file operations
  
#  prompt for program
  
def cmdNumber(cmdWork):
  seq = 100
  incr = 10  
  [seq, incr, msg] = getNumbers(cmdWork, seq, incr)
  if msg != 'OK':
    return msg
  
  code = input (str(seq))
  while code != '':
    data.codeList[seq] = str(seq) + ' ' + helpers.upshift(code)
    seq = seq + incr 
    code = input(str(seq))
    
  return 'OK'
  
  # load a file
  
def cmdOld(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
    
  cmdNew(cmdWork)
  if helpers.fileExists(fileName) == False:
    return 'No data found'
    
  with open (fileName, 'r') as fl:
    while  (line := fl.readline().strip()):
      line = helpers.upshift(line)
      cmdAddLine(line)  
    fl.close()
 
  return 'OK'
  
  #  save a file
  
def cmdSave(cmdWork):
  if len(data.codeList) == 0:
    return 'Can\'t do that'
    
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
  
  parser.createIndex()  
  
  with open (fileName, 'w') as fl:
    for lineNumber in data.index:
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
    
    
    #  continue after breakpoint
    
def cmdContinue(cmdWork):
  return runtime.runContinue(cmdWork)
    
#  edit a line of code
    
def cmdEdit(cmdWork):
  [n, code, msg] = editor.preEdit(cmdWork)
  if msg != 'OK':
    return msg
    
  print (str(n) + ' ' + code)
  mask = input (str(n) + ' ')
  while mask != '':
    code = editor.edit(code, mask)
    code = helpers.upshift(code)
    print (str(n) + ' ' + code)
    mask = input (str(n) + ' ')
  
  if code == '':
    data.codeList.pop(n)
  else:
    data.codeList[n] = str(n) + ' ' + code
  return 'OK'
  
    # delete file
    
def cmdDelete(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if msg != 'OK':
    return msg
    
  if helpers.fileExists(fileName) == False:
    return 'No data found'
    
  os.remove(fileName)
  return 'OK'
  
  
  #-----------------------
  #  other commands
 
 #  run the program
 
def cmdRun(cmdWork):    
  return runtime.run(cmdWork)
 
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
  
  #  get numbers separated by commas
      
def getNumbers(txt, n1, n2):
  part1 = ''
  part2 = ''
  num1 = n1
  num2 = n2
  msg = 'OK'
  
  i = txt.find(' ')
  if i < 3:
    return [n1, n2, 'OK']
    
  parts = txt[i: len(txt)].split(',')
  if len(parts) > 0:
    part1 = parts[0].strip()
    
  if len(parts) > 1:
    part2 = parts[1].strip()

  if part1 != '':
    if helpers.isnumeric(part1):
      num1 = int (part1)
    else:
      msg = 'Incorrect statement'
    
  if part2 != '':
    if helpers.isnumeric(part2):
      num2 = int (part2)
    else:
      msg = 'Incorrect statement'
    
  return [num1, num2, msg]
      
# get numbers for list command
#
#  list -      list all
#  list n      list line n
#  list n-     list lines n through last
#  list -n  -  list first through line n
#  list n1-n2  list lines n1 through n2
  
def getNumbersForList(txt, n1, n2):
  part1 = ''
  part2 = ''
  num1 = 0
  num2 = 0
  msg = 'OK'
  
  i = txt.find(' ')
  if i < 3:
    return [n1, n2, 'OK']
    
  parts = txt[i: len(txt)].split('-')
  if len(parts) > 0:
    part1 = parts[0].strip()
    
  if len(parts) > 1:
    part2 = parts[1].strip()

  if part1 != '':
    if helpers.isnumeric(part1):
      num1 = int (part1)
    else:
      msg = 'Incorrect statement'
    
  if part2 != '':
    if helpers.isnumeric(part2):
      num2 = int (part2)
    else:
      msg = 'Incorrect statement'
    
  if len(parts) == 1:
    return [num1, num1, msg]
  
  if part1 == '':
    if part2 == '':
      return [num1, num2, 'Incorrect statement']
    else:
      return [n1, num2, msg]
  else:
    if part2 == '':
      return [num1, n2, msg]
    else:
      return [num1, num2, msg]