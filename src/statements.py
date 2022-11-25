#  statements - used as both command and runtime

#  note: line numvers will be removed before passing to these functions

import data
import helpers

# let statement

def stmtLet(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 4):
    return 'Syntax error'
	
  if (parts[2] != '='):
    return 'Syntax error'
      
  vName = parts[1]
  i = cmdWork.find('=')
  [value, msg] = helpers.evaluate(cmdWork[i+1: len(cmdWork)])
  if (msg != 'OK'):
    return msg

  data.variables[vName] = value  
  return 'OK'
  
  
  