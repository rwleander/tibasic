#  commands - parse and run repl commands

import data

# process a command

def executeCommand(cmd):
  cmdWork = cmd.upper()
  
  if (cmdWork == 'NEW'):
    return cmdNew()
    
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
      
    
