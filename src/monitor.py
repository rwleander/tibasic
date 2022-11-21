#  monitor - parse commands

import data

# process a command

def executeCommand(cmd):
  cmdWork = cmd.upper()
  if (cmdWork == 'QUIT'):
    data.quitFlag = True
    return ''
    
  return 'unknown command'
    
    
