#  run time interprets  the code

import data
import parser
import helpers

#  run the program

def run():
  if (len(data.codeList) == 0):
    return 'No code'
  
  rslt = parser.parse()
  if (rslt != 'OK'):
    return rslt
    
   
  address = data.firstLine
  while (address > 0):
    [address, msg] = executeStatement(address)
    if (msg  != 'OK'):
        return msg    
        
  return 'Done'
  
  
  # run a line of code
  
def executeStatement(address):
  item = data.parseList[address]
  if (item['error'] != 'OK'):
    msg =   item['code'] + '\n' + item['error']
    return [-1, msg]  
  
  if (item['statement'] == 'LET'):
    return runLet(item)
  
  if (item['statement'] == 'IF'):
    return runIf(item)
    
  if (item['statement'] == 'PRINT'):
    return runPrint(item)
  
  msg = item['code'] + '\n' + 'Unknown statement type'
  return [-1, msg]
  
  
  #  run the LET command
  
def runLet(item):
  variable = item['var']
  expr = item['expr']
  [value, msg] = helpers.evaluateExpression(expr)
  if (msg != 'OK'):
    msg = item['code'] + '\n' + 'Expression error' 
    return [-1, msg]    
  data.variables[variable] = value
  return [item['nextLine'], 'OK']
  
  # run an if statement
  
def runIf(item):
  expr = item['expr']
  [value, msg] = helpers.evaluateExpression(expr)
  if (msg != 'OK'):
    msg = item['code'] + '\n' + 'Expression error' 
    return [-1, msg]    
    
  trueLine = int(item['line1'])
  falseLine = item['nextLine']
  if 'line2' in item:
    if (helpers.isnumeric(item['line2']) and item['line2'] != ''):
      falseLine = int(item['line2'])
  
  if (value == True):
    nextLine = trueLine
  else:
    nextLine = falseLine
  return [nextLine, 'OK']
  
  #  run print statement
  
def runPrint(item):
  expr = item['expr']
  [value, msg] = helpers.evaluateExpression(expr)
  if (msg != 'OK'):
    msg = item['code'] + '\n' + 'Expression error' 
    return [-1, msg]    
  print (value)
  return [item['nextLine'], 'OK']
  
