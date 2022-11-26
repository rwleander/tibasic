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
  value = eval(expr, data.variables)

  data.variables[vName] = value  
  return 'OK'
  
#print statement
  
def stmtPrint(cmdWork):
  parts = cmdWork.split()
  if (len(parts) != 2):
    return 'Syntax error'
  
  if (parts[1] in data.variables):
    return str(data.variables[parts[1]])
    
  else:
    return 'Unknown variable'
  
  