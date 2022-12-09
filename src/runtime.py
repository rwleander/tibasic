#  run time interprets  the code

import data
import parser
import helpers

#  run the program

def run():
  if (len(data.codeList) == 0):
    return 'No code'
  
  clearData()
  
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
    
  if (len(data.forNextStack) > 0):
    return 'Missing NEXT'
    
  return 'Done'
  
#  clear the variables
  
  
def clearData():
  data.variables = {}
data.index = []
data.parserList = {}
data.gosubStack = []
data.forNextStack = []
  
  
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
    
  if (item['statement'] == 'FOR'):
    return runFor(item)
    
  if (item['statement'] == 'NEXT'):
    return runNext(item)

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

# for statement - push data to for stack then return next line

def runFor(item):
  var = item['var']
  expr1 = item['expr1']
  expr2 = item['expr2']  
  step = 1
  nextLine = item['nextLine']
  
  [min, msg] = helpers.evaluateExpression(expr1)
  if (msg != 'OK'):
    return [-1, msg]
    
  [max, msg] = helpers.evaluateExpression(expr2)
  if (msg != 'OK'):
    return [-1, msg]
  
  if 'expr3' in item:
    [step, msg] = helpers.evaluateExpression(item['expr3'])
    if (msg != 'OK'):
      return [-1, msg]
  
  data.variables[var] = min
  stackItem = {'var': var, 'min': min, 'max': max, 'step': step,  'nextLine': nextLine}
  data.forNextStack.append(stackItem)   
  return [nextLine, 'OK']
  
# next - get data from for/next stack and either increment variable or got o next line
  
def runNext(item):
  if (len(data.forNextStack) < 1):
    return [-1, 'Missing FOR']
    
  stackItem = data.forNextStack[len(data.forNextStack) - 1]
  var = stackItem['var']
  max = stackItem['max']
  step = stackItem['step']
  value = data.variables[var]
  value = value + step

  # at end of for - remove item from stack, go to next line
# otherwise go to line after for

  if ((step > 0 and value > max) or (step < 0 and value < max)):
    data.forNextStack.pop()
    nextLine = item['nextLine']  
  else:
    data.variables[var] = value
    nextLine = stackItem['nextLine']
  
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
  
  # remark
  
def runRem(item):
  return [item['nextLine'], 'OK']
  
  # stop and end
  
def runStop(item):
  return [-1, 'OK'] 


#--------------------
#  validate and return items from parseList

#  get a string by name

def getString(item, name):
  if name  in item:
    return item[name]
  else:
    item['error'] = 'Missing ' + name
    return 'error'
  
#  get a line number from the item

def getLine(item, name):
  if name  not in item:
    item['error'] = 'Missing ' + name
    return -1
    
  str = item[name]
  if (helpers.isnumeric(str) == False):
    item['error'] = 'Bad line number'
    return -1
    
  line =  int(str)
  if line  in data.parseList:
    return line
  else:
    item['error'] = 'Bad line number'
    return line
    

#  get optional line number
#  if not found, return -1

def getLineOptional(item, name):
  if name in item:
    return getLine (item, name)
  else:
    return -1
    
