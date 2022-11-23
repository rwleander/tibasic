#  commands - parse and run repl commands

import data

# process a command

def executeCommand(cmd):
  cmdWork = cmd.upper()
  parts = cmdWork.split()
  if (len(parts) == 0):
    return ''

  command = parts[0]      
  if (command == 'NEW'):
    return cmdNew()
    
  if (command == 'LIST'):
    return cmdList()  

  if (command[0] >= '0' and cmdWork[0] <= '9'):
    return cmdAddLine(cmdWork)
  
  if (command == 'SAVE'):
    return cmdSave(cmdWork)
    
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
  if (parts[0].isnumeric()):
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

  #-----------------------
  #  file operations
  
  #  save a file
  
def cmdSave(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 2):
    return 'Missing file name'
    
  if (len(parts) > 2):
    return 'Too many arguments'
      
  index = []
  for lineNumber in data.codeList:
    index.append(lineNumber)
  index.sort()  
  
  fileName =  parts[1] + '.ti'  
  with open (fileName, 'w') as fl:
    for lineNumber in index:      
      fl.write (data.codeList[lineNumber] + '\n')
    fl.close()
  return 'OK'