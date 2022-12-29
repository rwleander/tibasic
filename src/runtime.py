#  run time interprets  the code

import random

import data
import parser
import helpers
import expressions

#  run the program

def run():
  if len(data.codeList) == 0:
    return 'No code'
  
  clearData()
  
  result = parser.parse()
  if result != 'OK':
    return result
   
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
random.seed(0)
  
  
  # run a line of code
  
def executeStatement(address): 

  functionList = {    
    'END': runStop,
    'FOR': runFor,
    'GO': runGo,
    'GOSUB': runGosub,
    'GOTO': runGoto,
    'IF': runIf,
    'LET': runLet,
    'NEXT': runNext,
    'PRINT': runPrint,
    'RANDOMIZE': runRandomize,
    'REM': runRem,
    'RETURN': runReturn,
    'STOP': runStop    
}    
  
  item = data.parseList[address]
  if item['error'] != 'OK':    
    return [-1, createError(item)]  
  
  statement = item['statement']
  if statement in functionList:
    return functionList[statement](item)   
  else:
    return [-1, createMsg(item, 'unknown statement')]
  
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
  
  msg = helpers.setVariable(var, min) 
  if msg != 'OK':
    return [-1, createMsg(item, msg)]
  
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

  #  if goto or gosub were coded as two words, route to correct function
  
def runGo(item):
  cmdType = getString(item, 'type')
  line = getLine(item, 'line')
  
  if item['error'] != 'OK':
    return [-1, createError(item)]

  if cmdType == 'TO':
    return [line, 'OK']
    
  if cmdType == 'SUB':
    data.gosubStack.append(item['nextLine'])
    return [line, 'OK']
  
  return [-1, createMsg(item, 'Bad command')]
  
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
  
  #  run the LET command
  
def runLet(item):
  expr = getString(item, 'expr')
  variable = getString(item, 'var')
  if item['error'] != 'OK':    
    return [-1, createError(item)]
  
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':    
    return [-1, createMsg(item, msg)]
    
  msg = helpers.setVariable(variable, value)  
  if msg == 'OK':
    return [item['nextLine'], 'OK']
  else:
    return [-1, createMsg(item, msg)]
    
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
  
#  randomize - set random sequence
  
def runRandomize(item):
  random.seed()
  return [item['nextLine'], 'OK']

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

