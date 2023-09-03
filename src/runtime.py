#  TI 99/4A BASIC
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  runtime.py -  interpret and run the program
#
#  Entry points:
#
#  msg = runtime.run(cmd)
#     note: cmd may contain a line number such as 'RUN 100'
#     otherwise, cmd will be 'RUN'
#
#  msg = runContinue(cmd)
#

import random
import math

import parser
import data
import helpers
import expressions
import matrix
import readWrite

#  run the program

def run(cmd):
  if len(data.codeList) == 0:
    return 'Can\'t do that'

  clearData()

  result = parser.parse()
  if result != 'OK':
    return result

  result = restoreData(data.firstLine)
  if result != 'OK':
    return result

  data.address = data.firstLine
  parts = cmd.split()
  if len(parts) == 2:
    parts[1] = parts[1].strip()
    if helpers.isnumeric(parts[1]):
      data.address = int(parts[1])
    else:
      return 'Bad line number'

  msg =  runContinue(cmd)
  if len(data.fileList) > 0:
    readWrite.closeAllFiles()
  return msg

#  continue running code from address
#  note: consider refactoring

def runContinue(cmd):
  if data.address < 0:
    return 'Can\'t do that'

  while data.address > 0:
    if data.address in data.parseList:
      item = data.parseList[data.address]
    else:
      return 'Bad line number - ' + str(data.address)

    if item['error'] != 'OK':
      return createError(item)

  #  if in breakpoint list, stop

    if data.address in data.breakpointList:
      data.breakpointList.remove(data.address)
      return 'Breakpoint at ' + str(data.address) + '\n' + item['code']

#  if command is break without line numbers, also break

    if  item['statement'] == 'BREAK' and len(item['lines']) == 0:
      n = data.address
      data.address = item['nextLine']
      return 'Breakpoint at ' + str(n) + '\n' + item['code']

  #  if trace on, print the line number

    if data.traceFlag:
      print('<' + str(data.address) + '> ', end='')

    newAddress = executeStatement(item)
    if item['error']  != 'OK':
      return createError(item)

    if data.address == newAddress and data.address > 0 and item['statement'] != 'NEXT':
      return createMsg(item, 'Infinite loop')
    data.address = newAddress

  if len(data.forNextStack) > 0:
    return 'For-next error'

  return 'Done'

#  clear the global variables

def clearData():
  data.variables = {}
  data.index = []
  data.parserList = {}
  data.userFunctionList = {}
  data.gosubStack = []
  data.forNextStack = []
  data.dataList = []
  data.fileList = {}
  data.dataPointer = 0
  data.printPosition = 0
  data.matrixList = {}
  data.matrixBase = 0
  random.seed(0)

# call the appropriate function for the current statement

def executeStatement(item):

  functionList = {
    'BREAK': runBreak,
    'CLOSE': runClose,
    'DATA': runData,
    'DEF': runDef,
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
    'ON_GOSUB': runOnGosub,
    'ON_GOTO': runOnGoto,
    'OPEN': runOpen,
    'OPTION': runOption,
    'PRINT': runPrint,
    'RANDOMIZE': runRandomize,
    'READ': runRead,
    'REM': runRem,
    'RESTORE': runRestore,
    'RETURN': runReturn,
    'STOP': runStop,
    'TRACE': runTrace,
'UNBREAK': runUnbreak,
'UNTRACE': runTrace
}

  if item['error'] != 'OK':
    return -1

  statement = item['statement']
  if statement in functionList:
    return functionList[statement](item)

  item['error'] = 'Unknown statement'
  return -1

#  set  a breakpoint

def runBreak(item):
  for lineNumber in item['lines']:
    n = int(lineNumber)
    if n  in data.codeList:
      data.breakpointList.append(n)
      return item['nextLine']

    item['error'] = 'Bad line number - ' + lineNumber
    return -1

#  close a file

def runClose(item):
  readWrite.closeFile(item)
  if item['error'] != 'OK':
    return -1
  return item['nextLine']

# data statements are processed at the beginning of the program
#  go to to next statement when encountered during runtime

def runData(item):
  nextLine = item['nextLine']
  return nextLine

#  add a user defined function

def runDef(item):
  func = item['function']
  arg = item['arg']
  expr = item['expr']
  functionItem = {'arg': arg, 'expr': expr}
  data.userFunctionList[func] = functionItem
  nextLine = item['nextLine']
  return nextLine

# run dim statement - add to matrix list and initialize variable

def runDim(item):
  dimList = item['vars']
  for dimItem  in dimList:
    var = getString(dimItem, 'id')
    size = getString(dimItem, 'size')

    parts = size.split(',')
    x = 0
    y = 0
    z = 0

    if len(parts) < 1:
      item['error'] = 'Bad statement'
      return -1

    if len(parts) > 0:
      x = int(parts[0])

    if len(parts) > 1:
      y = int (parts[1])

    if len(parts) == 3:
      z = int(parts[2])

    msg= matrix.newVariable(var, x, y, z)
    if msg != 'OK':
      item['error'] = msg
      return -1

  return item['nextLine']

#  run for statement
#  note: consider refactor

def runFor(item):
  expr2 = getString (item, 'expr2')
  expr1 = getString(item, 'expr1')
  var = getString(item, 'var')
  if item['error'] != 'OK':
    return -1

  step = 1
  nextLine = item['nextLine']

  [minValue, msg] = expressions.evaluate(expr1)
  if msg != 'OK':
    item['error'] = msg
    return -1

  [maxValue, msg] = expressions.evaluate(expr2)
  if msg != 'OK':
    item['error'] = msg
    return -1

  if 'expr3' in item:
    [step, msg] = expressions.evaluate(item['expr3'])
    if msg != 'OK':
      item['error'] = msg
      return -1
    if step == 0:
      item['error'] = 'Bad value'
      return -1

  # if  initial value outside of range, skip to next

  if step > 0 and (minValue > maxValue):
    end  = item['forNext']
    nextItem = data.parseList[end]
    return nextItem['nextLine']

#otherwise, set up the for/next stack and proceed

  msg = helpers.setVariable(var, minValue)
  if msg != 'OK':
    item['error'] = msg
    return -1

  stackItem = {}
  stackItem['var'] = var
  stackItem['min'] = minValue
  stackItem['max'] = maxValue
  stackItem['step'] = step
  stackItem['nextLine'] = nextLine
  data.forNextStack.append(stackItem)
  return nextLine

# next - get data from for/next stack and either increment variable or go to next line

def runNext(item):
  if len(data.forNextStack) < 1:
    item['error'] = 'Can\'t do that'
    return -1

  stackItem = data.forNextStack[len(data.forNextStack) - 1]
  var = stackItem['var']
  maxValue = stackItem['max']
  step   = stackItem['step']
  value = data.variables[var]

  if item['var'] != var and item['var'] != '':
    item['error'] = 'Can\'t do that'
    return -1

  value = value + step

  # at end of for - remove item from stack, go to next line
# otherwise go to line after for

  if (step > 0 and value > maxValue) or (step < 0 and value < maxValue):
    data.forNextStack.pop()
    nextLine = item['nextLine']
  else:
    data.variables[var] = value
    nextLine = stackItem['nextLine']

  return nextLine

#  if goto or gosub were coded as two words, route to correct function

def runGo(item):
  cmdType = getString(item, 'type')
  line = getLine(item, 'line')

  if item['error'] != 'OK':
    return -1

  if cmdType == 'TO':
    return line

  if cmdType == 'SUB':
    item['line'] = line
    return runGosub(item)

  item['error'] = 'Bad command'
  return -1

# run go to

def runGoto(item):
  line = getLine(item, 'line')
  if item['error'] == 'OK':
    return line

  return -1

# run go sub

def runGosub(item):
  line = getLine(item,'line')
  if item['error'] != 'OK':
    return -1

  data.gosubStack.append(item['nextLine'])
  return line

#  return from gosub

def runReturn(item):
  if len(data.gosubStack) == 0:
    item['error'] = 'Missing GOSUB'
    return -1

  addr = data.gosubStack.pop()
  return addr

# run an if statement

def runIf(item):
  line2 = getLineOptional(item, 'line2', item['nextLine'])
  line1 = getLine(item, 'line1')
  expr = getString(item, 'expr')
  if item['error'] != 'OK':
    return -1

  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':
    item['error'] = msg
    return -1

  if value:
    newLine = line1
  else:
    newLine = line2

  return newLine

#  get input data

def runInput(item):
  prompt =getString(item, 'prompt')
  variables = item['inputs']
  fileNum = item['fileNum']
  if fileNum > 0:
    readWrite.inputFile(item)
    if item['error'] == 'OK':
      return item['nextLine']
    return -1

  txt = input (prompt)

  msg = readWrite.processInputsFromString(variables, txt)
  if msg == 'OK':
    nextLine = item['nextLine']
    return nextLine

  item['error'] = msg
  return -1


#  run the LET statement

def runLet(item):
  expr = getString(item, 'expr')
  variable = getString(item, 'var')
  if item['error'] != 'OK':
    return -1

  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':
    item['error'] = msg
    return -1

  if variable.find('(') > 0:
    msg = matrix.setVariable(variable, value)
  else:
    msg = helpers.setVariable(variable, value)

  if msg == 'OK':
    return item['nextLine']

  item['error'] = msg
  return -1

#  run on gosub

def runOnGosub(item):
  expr = getString(item, 'expr')
  lines = item['lines']

  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':
    item['error'] = msg
    return -1

  value = int(value)
  if value < 1 or value > len(lines):
    item['error'] = 'Bad index'
    return -1

  line = int(lines[value - 1])
  if line in data.parseList:
    item['line'] = line
    return runGosub(item)

  item['error'] = 'Bad line number - ' + str(line)
  return -1

#  run on goto statement

def runOnGoto(item):
  expr = getString(item, 'expr')
  lines = item['lines']

  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':
    item['error'] = msg
    return -1

  value = int(value)
  if value < 1 or value > len(lines):
    item['error'] = 'Bad value'
    return -1

  line = int(lines[value - 1])
  if line  in data.parseList:
    return line

  item['error'] = 'Bad line number - ' + str(line)
  return -1

#  run the open command

def runOpen(item):
  readWrite.openFile(item)
  if item['error'] != 'OK':
    return -1
  return item['nextLine']

#  change option

def runOption(item):
  n = getString(item, 'n')
  if n not in ['0', '1']:
    item['error'] = 'Incorrect statement'
    return -1

  msg = matrix.setOption(int(n))
  if msg == 'OK':
    nextLine = item['nextLine']
    return nextLine

  item['error'] = msg
  return -1


#  run print statement
#  note: consider refactor

def runPrint(item):
  parts = item['parts']
  fileNum = item['fileNum']
  if fileNum > 0:
    readWrite.printFile(item)
    if item['error'] == 'OK':
      return item['nextLine']
    return -1

  if len(parts) == 0:
    print()
    data.printPosition = 0
    return item['nextLine']

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
        item['error'] = msg
        return -1

      if type(txt) == bool:
        txt = str(txt)
      if type(txt) == float or type(txt) == int:
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

  return item['nextLine']

# randomize - set random sequence

def runRandomize(item):
  random.seed()
  return item['nextLine']

#  read from data list

def runRead(item):
  variables = item['inputs']
  values = []

  for var in variables:
    if data.dataPointer < len(data.dataList):
      values.append(data.dataList[data.dataPointer])
      data.dataPointer = data.dataPointer + 1
    else:
      item['error'] = 'Out of data'
      return -1

  msg = readWrite.processInputs(variables, values)
  if msg != 'OK':
    item['error'] = msg
    return -1

  nextLine = item['nextLine']
  return nextLine

#  REM statement

def runRem(item):
  return item['nextLine']

#  restore reload  data list

def runRestore(item):
  n = data.firstLine

  if 'line' in item:
    s = item['line']
    if s != '':
      n = int(s)

  msg = restoreData(n)
  if msg != 'OK':
    item['error'] = msg
    return -1

  return item['nextLine']

# stop and end

def runStop(item):
  data.address = -1
  return -1

#  set or reset trace flag

def runTrace(item):
  data.traceFlag = item['statement'] == 'TRACE'
  return item['nextLine']

#  clear breakpoint

def runUnbreak(item):
  if len(item['lines']) == 0:
    data.breakpointList = []
    return item['nextLine']

  for lineNumber in item['lines']:
    n = int(lineNumber)
    if n  in data.codeList:
      data.breakpointList.remove(n)
      return item['nextLine']

    item['error'] = 'Bad line number - ' + lineNumber
    return -1


#-------------------
#  handle input and output values

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

#  get a string by name from the parse tree

def getString(item, name):
  if name  in item:
    return item[name]

  item['error'] = 'Missing ' + name
  return 'error'

#  get a line number from the item

def getLine(item, name):
  if name  not in item:
    item['error'] = 'Missing ' + name
    return -1

  s = item[name]
  if helpers.isnumeric(s) is False:
    item['error'] = 'Bad line number - ' + s
    return -1

  line =  int(s)
  if line  in data.parseList:
    return line

  item['error'] = 'Bad line number'
  return line


#  get optional line number
#  if not found, return -1

def getLineOptional(item, name, defaultLine):
  if name in item:
    return getLine (item, name)

  return defaultLine

#  create an error message from an  item or string

def createError(item):
  if item['source'] == 'command':
    return item['error']

  return item['code'] + '\n' + item['error']

def createMsg(item, msg):
  if item['source'] == 'command':
    return msg

  return item['code'] + '\n' + msg
