#  run time interprets  the code

import random
import math

import data
import parser
import helpers
import expressions
import matrix

#  run the program

def run():
  if len(data.codeList) == 0:
    return 'No code'
  
  clearData()
  
  result = parser.parse()
  if result != 'OK':
    return result

  result = restoreData(data.firstLine)
  if result != 'OK':
    return result
   
  address = data.firstLine
  while address > 0:
    item = data.parseList[address]
    [newAddress, msg] = executeStatement(item)
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
data.dataList = []
data.dataPointer = 0
data.printPosition = 0
data.matrixList = {}
data.matrixBase = 0
random.seed(0)
  
  
  # run a line of code
  
def executeStatement(item): 

  functionList = {    
    'DATA': runData,
    'DIM': runDim,
    'DISPLAY': runPrint,
    'END': runStop,
    'FOR': runFor,
    'GO': runGo,
    'GOSUB': runGosub,
    'GOTO': runGoto,
    'IF': runIf,
    'INPUT': runInput,
    'LET': runLet,
    'NEXT': runNext,
    'OPTION': runOption,
    'PRINT': runPrint,
    'RANDOMIZE': runRandomize,
    'READ': runRead,
    'REM': runRem,
    'RESTORE': runRestore,
    'RETURN': runReturn,
    'STOP': runStop    
}    
  
  if item['error'] != 'OK':    
    return [-1, createError(item)]  
  
  statement = item['statement']
  if statement in functionList:
    return functionList[statement](item)   
  else:
    return [-1, createMsg(item, 'unknown statement')]
  
  # run data statement - ignore - handled by restoreData function
  
def runData(item):  
  nextLine = item['nextLine']
  return [nextLine, 'OK']

# run dim statement - add to matrix list and initialize variable

def runDim(item):
  var = getString(item, 'var')
  size = getString(item, 'size')
  if helpers.isnumeric (size) == False:
    return [-1, 'Bad statement']
    
  parts = size.split('.')
  x = 0
  y = 0
  z = 0
  
  if len(parts) < 1:
    return [-1, 'Bad statement']
    
  if len(parts) > 0:
    x = int(parts[0])
    
  if len(parts) > 1:
    y = int (parts[1])
  
  if len(parts) == 3:
    z = int(parts[2])

  msg= matrix.newVariable(var, x, y, z)  
  if msg != 'OK':
    return [-1, 'OK']

  nextLine = item['nextLine']
  return [nextLine, 'OK']
    
  #  run for statement
  
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
  
#  get input data
  
def runInput(item):
  prompt =getString(item, 'prompt')
  vars = item['inputs']
  
  txt = input (prompt)
  
  msg = processInputsFromString(vars, txt)
  if msg == 'OK':
    nextLine = item['nextLine']
    return [nextLine, 'OK']
  else:
    return [-1, createMsg(item, msg)]
  
  
  #  run the LET command
  
def runLet(item):
  expr = getString(item, 'expr')
  variable = getString(item, 'var')
  if item['error'] != 'OK':    
    return [-1, createError(item)]
  
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':    
    return [-1, createMsg(item, msg)]
    
  if variable.find('(') > 0:
    msg = matrix.setVariable(variable, value)
  else:  
    msg = helpers.setVariable(variable, value)  
    
  if msg == 'OK':
    return [item['nextLine'], 'OK']
  else:
    return [-1, createMsg(item, msg)]
    
    #  change option
    
def runOption(item):  
  n = getString(item, 'n')  
  if n != '0' and n != '1':
    return [-1, 'Incorrect statement']
  
  msg = matrix.setOption(int(n))
  if msg == 'OK':  
    nextLine = item['nextLine']
    return [nextLine, 'OK']
  else:
    return [-1, msg]
    
    
#  run print statement
  
def runPrint(item):
  parts = item['parts']  
  if len(parts) == 0:
    print()
    data.printPosition = 0
    return [item['nextLine'], 'OK']
    
  for part in parts:
    if part == ';':
      data.printPosition = data.printPosition
    elif part == ':':
      print()
      data.printPosition = 0
 
    elif part == ',':
      zone = math.floor(data.printPosition / 14)
      nextZone  = (zone + 1) * 14
      if nextZone >= data.printWidth:
        print()
        data.printPosition =0
      else:
        tabWidth = nextZone - data.printPosition        
        print (helpers.tab(tabWidth), end = '')
        data.printPosition = nextZone

    else:
      [txt, msg] = expressions.evaluate(part)      
      if msg != 'OK':
        return [-1, msg]

      if type(txt) == float:
        txt = helpers.formatNumber(txt)
      if txt[0] == '"':
        txt = helpers.stripQuotes(txt)
      nextPosition = data.printPosition + len(txt)
      if nextPosition >= data.printWidth:
        print()
        data.printPosition = 0
      print (txt, end = '')
      data.printPosition = data.printPosition + len(txt)

  if parts[len(parts) - 1] not in [':', ';', ',']:
    print()
    data.printPosition = 0  

  return [item['nextLine'], 'OK']
  
  # remark
  
#  randomize - set random sequence
  
def runRandomize(item):
  random.seed()
  return [item['nextLine'], 'OK']

#  read from data list

def runRead(item):
  vars = item['inputs']
  values = []
  
  for var in vars:
    if data.dataPointer < len(data.dataList):
      values.append(data.dataList[data.dataPointer])
      data.dataPointer = data.dataPointer + 1
    else:
      return [-1, createMsg(item, 'Out of data')]
  
  msg = processInputs(vars, values)
  if msg != 'OK':
    return [-1, createMsg(item, msg)]
  
  nextLine = item['nextLine']
  return [nextLine, 'OK']
  
def runRem(item):
  return [item['nextLine'], 'OK']
  
  #  restore reload  data list
  
def runRestore(item):
  n = data.firstLine

  if 'line' in item:
    s = item['line']
    if s != '':
      n = int(s)
    
  msg = restoreData(n)
  if msg != 'OK':
    return [-1, createMsg(item, msg)]
  
  return [item['nextLine'], 'OK']
  
  # stop and end
  
def runStop(item):
  return [-1, 'OK'] 


#-------------------
#  handle input and output values

#  save input values

def processInputs(vars, values):
  if len(vars) != len(values):
    return 'Bad values'
    
  i = 0
  while i < len(vars):
    var = vars[i]
    value = values[i]
    
    if helpers.isStringVariable(var):
      if value[0] != '"':
        value = helpers.addQuotes(value)
    else:      
      if type(value) == str:
        if helpers.isnumeric(value):
          value = float(value)
        else:
          return 'Bad value'
        
      if type(value) == int:                    
        value = float(value)
        
    msg = helpers.setVariable(var, value)
    if msg != 'OK':
      return msg
    i = i + 1

  return 'OK'
  
#  process input  from comma delimited string
  
def processInputsFromString(vars, txt):
  values = splitValues(txt)      
  return processInputs(vars, values)
    
    # extract data from comma delimited string
    
def splitValues(txt):
  values = []
  value = ''
  inQuotes = False
  
  for ch in txt:
    if ch == '"':
      inQuotes = not inQuotes
      
    if inQuotes == True:
      value = value + ch
    else:
      if ch == ',':
        if value != '':
          values.append(value)
        value = ''
      elif ch != ' ':
        value = value + ch
    
  if value != '':
    values.append(value)
    
  return values
  
  # restore data starting at line number
  
def restoreData(n):
  if n not in data.index:
    return 'Bad line number - ' + str(n)

  data.dataList = []
  data.dataPointer = 0    
  lineNumber = n
  while lineNumber > 0:
    item = data.parseList[lineNumber]    
    if item['statement'] == 'DATA':
      if item['error'] != 'OK':
        return item['error']
      data.dataList.extend(item['data'])
    lineNumber = item['nextLine']
    
  return 'OK'    
  

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
    
  s = item[name]
  if helpers.isnumeric(s) == False:
    item['error'] = 'Bad line number - ' + s    
    return -1
  
  line =  int(s)
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
  if item['source'] == 'command':
    return item['error']
  else:
    return item['code'] + '\n' + item['error']

def createMsg(item, msg):
  if item['source'] == 'command':
    return msg
  else:  
    return item['code'] + '\n' + msg

