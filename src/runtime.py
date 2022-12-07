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
    [newAddress, msg] = executeStatement(address)
    if (msg  != 'OK'):
        return msg    
    if (address == newAddress):
      return 'Infinite loop at line ' + str(newAddress)    
    address = newAddress
    
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
    
  if (item['statement'] == 'GOTO'):
    return runGoto(item)
    
  if (item['statement'] == 'GOSUB'):
    return runGosub(item)
    
  if (item['statement'] == 'RETURN'):
    return runReturn(item)
    
  if (item['statement'] == 'PRINT'):
    return runPrint(item)
  
  if (item['statement'] == 'REM'):
    return runRem(item)
  
  if (item['statement'] == 'STOP' or item['statement'] == 'END'):
    return runStop(item)
    
    
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
  
  # run goto 
  
def runGoto(item):
  lineNum = item['line']
  err = item['code'] + '\nBad line number'
  if (helpers.isnumeric(lineNum) == False):
    return [-1, err]
  
  line = int(lineNum)  
  if line in data.parseList:
    return [line, 'OK']
  else:
    return [-1, err]
  
  # run gosub 
  
def runGosub(item):
  lineNum = item['line']
  err = item['code'] + '\nBad line number'
  if (helpers.isnumeric(lineNum) == False):
    return [-1, err]
  
  line = int(lineNum)  
  if line not in data.parseList:
    return [-1, err]
  
  data.gosubStack.append(item['nextLine'])
  return [line, 'OK']

#  return from gosub

def runReturn(item):
  addr = data.gosubStack.pop()
  return [addr, 'OK']
  
  #  run print statement
  
def runPrint(item):
  expr = item['expr']
  [value, msg] = helpers.evaluateExpression(expr)
  if (msg != 'OK'):
    msg = item['code'] + '\n' + 'Expression error' 
    return [-1, msg]    
  print (value)
  return [item['nextLine'], 'OK']
  
  # remark
  
def runRem(item):
  return [item['nextLine'], 'OK']
  
  # stop and end
  
def runStop(item):
  return [-1, 'OK'] 
  
