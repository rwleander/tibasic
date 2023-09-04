#  process statements

import random

import commands
import scanner
import expressions
import matrix
import readWrite
import data
import language

#  execute a statement

def executeStatement (item):
  if item['error'] != 'OK':
    return item['error']

  statementList = {
    'BREAK': doBreak,
    'CALL': doCall,
    'CLEAR': doClear,
    'DATA': doData,
    'DEF': doDef,
    'DIM': doDim,
    'END': doStop,
    'EXIT': doEndsub,
    'FOR': doFor,
    'GOSUB': doGosub,
    'GOTO': doGoto,
    'IF': doIf,
    'INPUT': doInput,
    'LET': doLet,
    'LINPUT': doLinput,
    'NEXT': doNext,
    'ON_GOSUB': doOnGosub,
    'ON_GOTO': doOnGoto,
    'OPTION': doOption,
    'PRINT': doPrint,
    'RANDOMIZE': doRandomize,
    'READ': doRead,
    'REM': doRem,
    'RESTORE': doRestore,
    'RETURN': doReturn,
    'RUN': doRun,
    'STOP': doStop,
    'SUB': doSub,
    'TRACE': doTrace,
    'UNBREAK': doUnbreak,
    'UNTRACE': doUntrace,
    'VERSION': doVersion
  }

  statement = item['statement']
  if statement in statementList:
    return statementList[statement](item)

  return 'Bad command'

#  clear

def doClear(item):
  data.variables = {}
  data.stack = []
  data.dataList = []
  data.dataPointer = 0
  data.userFunctionList = {}
  data.callList = {}
  data.matrixList = {}
  data.matrixBase = 0
  data.printArea = readWrite.initPrint(data.printWidth, data.printTab)
  data.traceFlag = False
  data.breakFlag = False
  data.breakList = []
  return 'OK'

#  version

def doVersion(item):
  return language.title + '\n' + language.version

#  set trace flag

def doTrace(item):
  data.traceFlag = True
  return item['error']
#  clear trace flag

def doUntrace(item):
  data.traceFlag = False
  return item['error']

#  set break point

def doBreak(item):
  lineList = item['line']
  if len(lineList) == 0:
    data.breakFlag = True
    return item['error']

  line = int(lineList[0])
  if line not in data.breakList:
    data.breakList.append(line)
  return item['error']

#  clear break points

def doUnbreak(item):
  lineList = item['line']
  if len(lineList) == 0:
    data.breakList = []
    return item['error']

  line = int(lineList[0])
  if line in data.breakList:
    data.breakList.remove(line)
  else:
    item['error'] = 'Bad line number'
  return item['error']

#  on data statement, do nothing

def doData(item):
  return item['error']

#  load data statement into dataList

def doDataLoad(item):
  values = scanner.getItemData(item, 'list')
  if len(values) == 0:
    item['error'] = 'Bad statement'
    return item['error']

  data.dataList = data.dataList + values
  return item['error']

#  def statement

def doDef(item):
  name = scanner.getItemValue(item, 'name')
  arg = scanner.getItemValue(item, 'arg')
  expr = scanner.getItemTokens(item, 'expr')
  if item['error'] != 'OK':
    return item['error']

  functionData = {
    'arg': arg,
    'expr': expr
  }
  data.userFunctionList[name] = functionData
  return 'OK'

#  load subroutine declaration

def doSubLoad(item, nextLine):
  subName = scanner.getItemValue(item, 'name')
  args = scanner.getItemTokens(item, 'args')
  if item['error'] != 'OK':
    return item['error']

  callData = {
    'name': subName,
    'args': args,
    'line': nextLine
  }
  data.callList[subName] = callData
  return 'OK'

# sub statement - ignore

def doSub(item):
  return 'OK'

#  call subroutine

def doCall(item):
  callName = scanner.getItemValue(item, 'name')
  args = scanner.getItemTokens(item, 'args')
  if item['error'] != 'OK':
    return item['error']

  if callName not in data.callList:
    item['error'] = 'Missing sub ' + callName
    return item['error']

  callData = data.callList[callName]
  stackItem = {
    'type': 'SUB',
    'line': data.address,
    'vars': data.variables,
    'mats': data.matrixList
  }
  data.stack.append(stackItem)

  [newVars, newMats, msg] = saveArguments(callData['args'], args)
  if msg != 'OK':
    item['error'] = msg
    return msg

  data.variables  = newVars
  data.matrixList = newMats
  data.address = callData['line']
  return 'OK'

#  end sub - pop the stack and continue run

def doEndsub(item):
  if len(data.stack) == 0:
    item['error'] = 'Missing sub'
    return item['error']

  stackItem = data.stack.pop(len(data.stack) -1)
  data.address = stackItem['line']
  data.variables = stackItem['vars']
  data.matrixList = stackItem['mats']
  return 'OK'

#  if statement

def doIf(item):
  value = scanner.getItemExpression(item, 'expr')
  line1Text = scanner.getItemValue(item, 'line1')
  if item['error'] != 'OK':
    return item['error']

  if scanner.isnumeric(line1Text) is True:
    line1 = int(line1Text)
  else:
    item['error'] = 'Bad line number in then:  ' + line1Text
    return item['error']

  line2 = getIfElseLine(item)
  if item['error'] != 'OK':
    return item['error']

  if value is True:
    data.address = line1
  else:
    data.address = line2
  return item['error']

#  get line number for else

def getIfElseLine(item):
  line2 = data.address

  if 'line2' not in item:
    return item['next']
  line2Text = scanner.getItemValue(item, 'line2')
  if line2Text == '':
    return line2

  if scanner.isnumeric(line2Text):
    line2 = int(line2Text)
    return line2
  item['error'] = 'Bad line number in else'
  return line2

#  on gosub - get line, then do gosub

def doOnGosub(item):
  value = scanner.getItemExpression(item, 'expr')
  lineNumbers = scanner.getItemData(item, 'list')
  if item['error'] != 'OK':
    return item['error']

  value = int(value)
  if value not in range(1, len(lineNumbers) +1):
    item['error'] = 'Bad value'
    return item['error']

  line = lineNumbers[value - 1]
  stackItem = {
    'type': 'GOSUB',
    'line': data.address
  }
  data.stack.append(stackItem)
  data.address = line
  return 'OK'

#  gosub

def doGosub(item):
  lineText = scanner.getItemValue(item, 'line')
  if scanner.isnumeric(lineText) is False:
    item['error'] = 'Bad line number'
    return item['error']

  line = int(lineText)
  stackItem = {
    'type': 'GOSUB',
    'line': data.address
  }
  data.stack.append(stackItem)
  data.address = line
  return item['error']

#  return from gosub

def doReturn(item):
  l = len(data.stack)
  if l == 0:
    item['error'] = 'Missing gosub'
    return item['error']

  stackItem = data.stack[l - 1]
  if stackItem['type'] != 'GOSUB':
    item['error'] = 'Missing gosub'
    return item['errpr']

  data.stack.pop(l - 1)
  data.address = stackItem['line']
  return item['error']

#  do on goto

def doOnGoto(item):
  value = scanner.getItemExpression(item, 'expr')
  lineNumbers = scanner.getItemData(item, 'list')
  if item['error'] != 'OK':
    return item['error']

  value = int(value)
  if value not in range(1, len(lineNumbers) +1):
    item['error'] = 'Bad value'
    return item['error']

  line = lineNumbers[value - 1]
  data.address = line
  return 'OK'

#  go to

def doGoto(item):
  line = scanner.getItemValue(item, 'line')
  if scanner.isnumeric(line):
    data.address = int(line)
  else:
    item['error'] = 'Bad line number'
  return item['error']

#  let statement

def doLet(item):
  tokens = scanner.getItemTokens(item, 'var')
  value = scanner.getItemExpression (item, 'expr')
  if item['error'] != 'OK':
    return item['error']

  if len(tokens) > 1:
    item['error'] = matrix.saveVariable(tokens, value)
  else:
    item['error'] = saveVariable(tokens[0], value)
  return item['error']

#  set matrixBase

def doOption(item):
  n = scanner.getItemExpression(item, 'n')
  if item['error'] == 'OK':
    return matrix.setOption(n)
  return item['error']

#  dim - allocate matrix

def doDim(item):
  var = scanner.getItemValue(item, 'var')
  dims = scanner.getItemData(item, 'dims')
  if item['error'] != 'OK':
    return item['error']

  item['error'] = matrix.newVariable(var, dims)
  return item['error']

#  print

def doPrint(item):
  lines = readWrite.formatPrint(data.printArea, item['list'])
  if data.printArea['error'] != 'OK':
    item['error'] = data.printArea['error']
    return item['error']

  for line in lines:
    print(line)
  return 'OK'

#  randomize

def doRandomize(item):
  random.seed()
  return 'OK'

#  read from data list

def doRead(item):
  tokens = scanner.getItemTokens(item, 'list')
  if item['error'] != 'OK':
    return item['error']

  for var in tokens:
    if var != ',':
      msg = doReadItem(var)
      if msg != 'OK':
        item['error'] = msg
        return msg

  return item['error']

  #  save a variable from the read list

def doReadItem(var):
  if data.dataPointer >= len(data.dataList):
    return 'Out of data'

  value = data.dataList[data.dataPointer]
  data.dataPointer = data.dataPointer + 1
  return saveVariable(var, value)

#  restore

def doRestore(item):
  data.dataPointer = 0
  return 'OK'

#  remark

def doRem(item):
  return 'OK'

#  stop / end
#  also route end sub to doEndsub

def doStop(item):
  option = scanner.getItemValue(item, 'option')
  if option == 'SUB':
    return doEndsub(item)

  data.address = -1
  return 'OK'

#  run statement

def doRun(item):
  option = scanner.getItemValue(item, 'option')
  if option == '':
    item['error'] = 'Bad argument'
    return item['error']

  commands.executeCommand('NEW')
  msg = commands.executeCommand('OLD ' + option)
  if msg != 'OK':
    item['error'] = msg
    return msg

  scanner.createIndex()
  return 'OK'

#  line input

def doLinput(item):
  prompt = '?'
  itemList = scanner.getItemTokens(item, 'list')
  if item['error'] != 'OK':
    return item['error']

  if len(itemList) > 2:
    if itemList[1] == ':':
      prompt = scanner.stripQuotes(itemList[0])
      itemList.pop(1)
      itemList.pop(0)

  if len(itemList) < 1:
    item['error'] = 'Bad argument'
    return item['error']

  varName = itemList[0]
  txt = input (prompt)
  item['error'] = saveVariable(varName, txt)
  return item['error']

#  read from keyboard

def doInput(item):
  prompt = '?'
  itemList = scanner.getItemTokens(item, 'list')
  if item['error'] != 'OK':
    return item['error']

  if len(itemList) > 1:
    if itemList[1] == ':':
      prompt = scanner.stripQuotes(itemList[0])
      itemList.pop(1)
      itemList.pop(0)

  txt = input (prompt)
  msg = readWrite.loadInput(itemList, txt)
  item['error'] = msg
  return msg

#  for statement

def doFor(item):
  var = scanner.getItemValue(item, 'var')
  minNum = scanner.getItemExpression(item, 'expr1')
  maxNum = scanner.getItemExpression(item, 'expr2')
  step = getForStep(item, minNum, maxNum)
  if item['error'] != 'OK':
    return item['error']

  stackItem = {'type': 'FOR'}
  stackItem['var'] = var
  stackItem['min'] = minNum
  stackItem['max'] = maxNum
  stackItem['step'] = step
  stackItem['line'] = data.address
  data.stack.append(stackItem)

  item['error'] = saveVariable(var, minNum)
  return item['error']

#  determine step value in for statement

def getForStep(item, minNum, maxNum):
  step = 1
  if minNum > maxNum:
    step = -1

  if 'expr3' not in item:
    return step

  tokens = scanner.getItemTokens(item, 'expr3')
  if len(tokens) == 0:
    return step

  return scanner.getItemExpression(item, 'expr3')

#  next statement

def doNext(item):
  itemVar = ''
  if 'var' in item:
    itemVar = scanner.getItemValue(item, 'var')

  if len(data.stack) == 0:
    item['error'] = 'Missing for'
    return item['error']

  stackItem = data.stack[len(data.stack) - 1]
  if stackItem['type'] != 'FOR':
    item['error'] = 'Missing for'
    return item['error']

  var = stackItem['var']
  maxNum = stackItem['max']
  step = stackItem['step']
  if itemVar not in [var, '']:
    item['error'] = 'Mismatched for'
    return item['error']

  value = data.variables[var] + step
  data.variables[var] = value
  if doForCheckMax(value, maxNum, step) is True:
    data.stack.pop(len(data.stack) - 1)
  else:
    data.address = stackItem['line']
  return 'OK'

#  determine if do loop has completed

def doForCheckMax(value, maxNum, step):
  if step > 0:
    return value > maxNum
  return value < maxNum


#  helper methods

#  save variable in storage

def saveVariable(var, value):
  if scanner.isValidVariable(var) is False:
    return 'Bad variable'

  data.variables[var] = value
  return 'OK'

#  save list of variables for call statement
#  note: value list may contain expressions

def saveArguments(args, values):
  newVars = {}
  newMats = {}
  i = 0
  for arg in args:
    if arg == ',':
      if values[i] != ',':
        return [newVars, newMats, 'Bad list']
    else:
      if values[i] in data.matrixList:
        newMats[arg] = data.matrixList[values[i]]
        newVars[arg] = data.variables[values[i]]
      else:
        [value, msg] = expressions.evaluate([values[i]])
        if msg != 'OK':
          return [newVars, newMats, msg]
        newVars[arg] = value

    i = i + 1
  return [newVars, newMats, 'OK']
