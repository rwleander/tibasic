#  commands - parse and run repl commands

import data

# process a command

def executeCommand(cmd):
  cmdWork = cmd.upper()
  
  if (cmdWork == 'NEW'):
    return cmdNew()
  if (cmdWork == 'LIST'):
    return cmdList()  
    
  if (cmdWork == 'QUIT'):
    data.quitFlag = True
    return ''
    
  return 'unknown command'
    
    
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
    