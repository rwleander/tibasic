#  commands - parse and run repl commands

import os

import data
import runtime
import helpers

# process a command

def executeCommand(cmd):
  cmdWork = cmd.upper()
  parts = cmdWork.split()
  if (len(parts) == 0):
    return ''

  command = parts[0]      
  if (command == 'NEW'):
    return cmdNew()
    
  if (command[0] >= '0' and cmdWork[0] <= '9'):
    return cmdAddLine(cmdWork)

  if (command == 'RESEQUENCE'):
    return cmdResequence()
  
  if (command == 'OPEN'):
    return cmdOpen(cmdWork)
    
  if (command == 'SAVE'):
    return cmdSave(cmdWork)
    
  if (command == 'FILES'):
    return cmdFiles()
    
  if (command == 'DELETE'):
    return cmdDelete(cmdWork)
      
  if (command == 'LET'):
    return cmdLet(cmdWork)
    
  if (command == 'PRINT'):
    return cmdPrint(cmdWork)


  if (command == 'LIST'):
    return cmdList()  

  if(command == 'RUN'):
    return runtime.run()
  
  if (command == 'QUIT'):
    data.quitFlag = True
    return ''
    
  return 'unknown command'
    

#------------------------------
#  code editing functions
    
#  NEW - clear lists
    
def cmdNew():
  data.codeList = {}
  data.variables = {}
  data.strings = {}
  data.parseList = {}
  return 'OK'

#  list code

def cmdList():
  str = ''
  index = []
  n = 0
  for i in data.codeList:
    index.append(i)
  index.sort()  
  for j in index:
    str = str + data.codeList[j] 
    n = n + 1
    if (n < len(data.codeList)):
      str = str + '\n'
  return str  
    
    
#  add or update a line of code

def cmdAddLine(cmd):
  parts = cmd.split()
  if (helpers.isnumeric(parts[0])):
    lineNumber = int(parts[0])
  else:
    return 'Bad line number'
    
  if (len(parts) > 1):
    data.codeList[lineNumber] = cmd
  else:
    if lineNumber in data.codeList:
      data.codeList.pop(lineNumber)    
    else:
      return 'Not in list'
  return 'OK'

# resequence the list

def cmdResequence():
  newCodeList = {}
  seq = 10
  
  for lineNumber in data.codeList:
    line = data.codeList[lineNumber]
    i = line.index(' ')    
    newLine = str(seq) + line[i:len(line)]    
    newCodeList[seq] = newLine
    seq = seq + 10
  data.codeList = newCodeList
  return 'OK'
  
  
  #-----------------------
  #  file operations
  
  # load a file
  
def cmdOpen(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if (msg != 'OK'):
    return msg
    
  cmdNew()
  if (helpers.fileExists(fileName) == False):
    return 'File not found'
    
  with open (fileName, 'r') as fl:
    while  (line := fl.readline().strip()):
      cmdAddLine(line)  
    fl.close()
 
  return 'OK'
  
  #  save a file
  
def cmdSave(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if (msg != 'OK'):
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
  
def cmdFiles():
  str = ''
  n = 0
  files  = os.listdir()
  for file in files:
    i = file.find('.ti')
    j = file.find('\\')
    if (i > 0 and j < 0): 
      str = str + file[0:i] + '\t'
      n = n + 1
  
  if (n > 0):
    return str[0:len(str)-1]
  else:
    return 'No files'
    
    # delete file
    
def cmdDelete(cmdWork):
  [fileName, msg] = helpers.parseFileName(cmdWork)
  if (msg != 'OK'):
    return msg
    
  if (helpers.fileExists(fileName) == False):
    return 'File not found'
    
  os.remove(fileName)
  return 'OK'
  
  
  #-----------------------
  #  other commands
  
  # let statement

def cmdLet(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 4):
    return 'Syntax error'
	
  if (parts[2] != '='):
    return 'Syntax error'
      
  vName = parts[1]
  i = cmdWork.find('=')
  expr = cmdWork[i+2: len(cmdWork)] 
  try:
    value = eval(expr, data.variables)
  except:
    return 'Syntax error'
  data.variables[vName] = value  
  return 'OK'
  
#print statement
  
def cmdPrint(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 2):
    return 'Syntax error'
  
  i = cmdWork.find(' ')
  expr = cmdWork[i+1: len(cmdWork)]
  try:
    value = eval(expr, data.variables)
  except:
    return  'Syntax error'
  return str(value)
  
  