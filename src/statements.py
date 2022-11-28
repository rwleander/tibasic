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
  expr = cmdWork[i+2: len(cmdWork)] 
  try:
    value = eval(expr, data.variables)
  except:
    return 'Syntax error'
  data.variables[vName] = value  
  return 'OK'
  
#print statement
  
def stmtPrint(cmdWork):
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
  