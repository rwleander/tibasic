#  run time interprets  the code

import data
import parser
import helpers
import expressions

#  run the program

def run():
  if len(data.codeList) == 0:
    return 'No code'
  
  clearData()
  
  rslt = parser.parse()
  if rslt != 'OK':
    return rslt
   
  address = data.firstLine
  while address > 0:
    [newAddress, msg] = executeStatement(address)
    if msg  != 'OK':    
        return msg    
        
    if address == newAddress:
      return 'Infinite loop at line ' + str(newAddress)    
    address = newAddress
    
  if len(data.forNextStack) > 0:
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
  if item['error'] != 'OK':
    msg =   item['code'] + '\n' + item['error']
    return [-1, msg]  
  
  if item['statement'] == 'LET':
    return runLet(item)
  
  if item['statement'] == 'IF':
    return runIf(item)
    
  if item['statement'] == 'GOTO':
    return runGoto(item)
    
  if item['statement'] == 'GOSUB':
    return runGosub(item)
    
  if item['statement'] == 'RETURN':
    return runReturn(item)
    
  if item['statement'] == 'FOR':
    return runFor(item)
    
  if item['statement'] == 'NEXT':
    return runNext(item)

  if item['statement'] == 'PRINT':
    return runPrint(item)
  
  if item['statement'] == 'REM':
    return runRem(item)
  
  if item['statement'] == 'STOP' or item['statement'] == 'END':
    return runStop(item)
    
  msg = item['code'] + '\n' + 'Unknown statement type'
  return [-1, msg]
  
  
  #  run the LET command
  
def runLet(item):
  expr = getString(item, 'expr')
  variable = getString(item, 'var')
  if item['error'] != 'OK':    
    return [-1, createError(item)]
  
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':    
    return [-1, createMsg(item, msg)]
    
  data.variables[variable] = value
  return [item['nextLine'], 'OK']
  
  # run an if statement
  
def runIf(item):
  line2 = getLineOptional(item, 'line2', item['nextLine'])
  line1 = getLine(item, 'line1')
  expr = getString(item, 'expr')
  if item['error'] != 'OK':    
    return [-1, createError(item)]
    
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':    
    return [-1, createMsg(item, msg)]
    
  if value == True:
    newLine = line1
  else:
    newLine = line2
  
  if (newLine in data.parseList) or (newLine == -1):
    return [newLine, 'OK']
  else:
    return [-1, createMsg(item, 'Bad line number')]
  
  # run goto 
  
def runGoto(item):
  line = getLine(item, 'line')
  if item['error'] == 'OK':  
    return [line, 'OK']
  else:
    return [-1, createError(item)]
  
  # run gosub 
  
def runGosub(item):
  line = getLine(item,'line')
  if item['error'] != 'OK':
    return [-1, createError(item)]
    
  data.gosubStack.append(item['nextLine'])
  return [line, 'OK']

#  return from gosub

def runReturn(item):
  addr = data.gosubStack.pop()
  return [addr, 'OK']

# for statement - push data to for stack then return next line

def runFor(item):
  expr2 = getString (item, 'expr2')
  expr1 = getString(item, 'expr1')
  var = getString(item, 'var')
  if item['error'] != 'OK':
    return [-1, createError(item)]
  
  step = 1
  nextLine = item['nextLine']
  
  [min, msg] = expressions.evaluate(expr1)
  if msg != 'OK':
    return [-1, createMsg(item, msg)]
    
  [max, msg] = expressions.evaluate(expr2)
  if msg != 'OK':
    return [-1, createMsg(item, msg)]
  
  if 'expr3' in item:
    [step, msg] = expressions.evaluate(item['expr3'])
    if msg != 'OK':
      return [-1, createMsg(item, msg)]
  
  data.variables[var] = min
  stackItem = {}
  stackItem['var'] = var 
  stackItem['min'] = min 
  stackItem['max'] = max
  stackItem['step'] = step
  stackItem['nextLine'] = nextLine
  data.forNextStack.append(stackItem)   
  return [nextLine, 'OK']
  
# next - get data from for/next stack and either increment variable or got o next line
  
def runNext(item):
  if len(data.forNextStack) < 1:
    return [-1, createMsg(item, 'Missing FOR')]
    
  stackItem = data.forNextStack[len(data.forNextStack) - 1]
  var = stackItem['var']
  max = stackItem['max']
  step   = stackItem['step']
  value = data.variables[var]
  
  value = value + step

  # at end of for - remove item from stack, go to next line
# otherwise go to line after for

  if (step > 0 and value > max) or (step < 0 and value < max):
    data.forNextStack.pop()
    nextLine = item['nextLine']  
  else:
    data.variables[var] = value
    nextLine = stackItem['nextLine']
  
  return [nextLine, 'OK']
  
#  run print statement
  
def runPrint(item):
  expr = getString(item, 'expr')
  if item['error'] != 'OK':
    return [-1, createError(item)]
    
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':    
    return [-1, createError(item, msg)]
    
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
  if helpers.isnumeric(str) == False:
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

def getLineOptional(item, name, defaultLine):
  if name in item:
    return getLine (item, name)
  else:
    return defaultLine

#  create an error message from an  ite or stringm    

def createError(item):
  return item['code'] + '\n' + item['error']

def createMsg(item, msg):
  return item['code'] + '\n' + msg

