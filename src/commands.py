#  process console commands

import statements
import scanner
import runtime
import readWrite
import resequencer
import language
import data

#  execute a command

def executeCommand (cmd):
  commandList = {
    'BREAK': cmdBreak,
    'BYE': cmdQuit,
    'CLEAR': cmdStatement,
    'CONTINUE': cmdContinue,
    'DATA': cmdData,
    'DEF': cmdStatement,
    'DELETE': cmdDelete,
    'FILES': cmdFiles,
    'INPUT': cmdStatement,
    'LET': cmdStatement,
    'LINPUT': cmdStatement,
    'LIST': cmdList,
    'MERGE': cmdMerge,
    'NEW': cmdNew,
    'NUMBER': cmdNumber,
    'OLD': cmdOld,
    'PRINT': cmdStatement,
    'QUIT': cmdQuit,
    'RANDOMIZE': cmdStatement,
    'READ': cmdStatement,
    'RESEQUENCE': cmdResequence,
    'RESTORE': cmdStatement,
    'RUN': cmdRun,
    'SAVE': cmdSave,
    'TRACE': cmdStatement,
   'UNBREAK': cmdStatement,
    'UNTRACE': cmdStatement,
    'VERSION': cmdStatement,
  }

  item = scanner.parseCommand(cmd)
  tokens = item['tokens']
  if len(tokens) == 0:
    return ''

  statement = tokens[0]
  if statement in commandList:
    return commandList[statement](item)

  lineNumber = scanner.getLineNumber(tokens[0])
  if lineNumber > 0:
    return cmdAddLine(lineNumber, cmd, item)

  return 'Bad command'

#  load data

def cmdData(item):
  return statements.doDataLoad(item)

#  delete

def cmdDelete(item):
  scanner.parseFileName(item)
  if item['error'] == 'OK':
    return readWrite.deleteCodeFile(item['fileName'])
  return item['error']

#  list disk files

def cmdFiles(item):
  printArea = readWrite.listFiles()
  if printArea['error'] != 'OK':
    return printArea['error']
  for line in printArea['lines']:
    print (line)
  return 'OK'

#  new

def cmdNew(item):
  data.codeList = {}
  return statements.doClear({})

#  run the program

def cmdRun(item):
  option = scanner.getItemValue(item, 'option')
  newAddress = -1
  if scanner.isnumeric(option):
    newAddress = int(option)
  else:
    if option != '':
      msg = executeCommand('OLD ' + option)
      if msg != 'OK':
        return msg

  if len(data.codeList) == 0:
    return 'Can\'t do that'

  scanner.createIndex()

  msg =  runtime.loadData()
  if msg != 'OK':
    return msg

  if newAddress > 0:
    data.address = newAddress
  return runtime.run()

#  add a breakpoint

def cmdBreak(item):
  lineList = item['line']
  if len(lineList) == 0:
    item['error'] = 'Missing line number'
    return item['error']
  return cmdStatement(item)

#  continue after break

def cmdContinue(item):
  if data.breakFlag is False:
    return 'Can\t do that'

  data.breakFlag = False
  return runtime.run()

#  run a statement

def cmdStatement(item):
  return statements.executeStatement(item)

#  list the code

def cmdList(item):
  index = scanner.createIndex()
  if len(index) == 0:
    return 'Can\'t do that'

  [startLine, endLine] = scanner.getItemSequence(item, 'range',
                         '-', data.firstLine, language.maxLine - 1)
  if item['error'] != 'OK':
    return item['error']

  txtWork = ''
  for lineNumber in index:
    if lineNumber in range(startLine, endLine + 1):
      codeItem = data.codeList[lineNumber]
      txtWork = txtWork + codeItem['code'] + '\n'
  txtWork = txtWork + 'OK'
  return txtWork

#  add a line of code

def cmdAddLine(lineNumber, cmd, item):
  if len(item['tokens']) > 1:
    codeItem = {}
    codeItem['code'] = cmd
    codeItem['next'] = -1
    data.codeList[lineNumber] = codeItem
  else:
    if lineNumber in data.codeList:
      data.codeList.pop(lineNumber)
    else:
      return 'Bad line number'

  return 'OK'

#  resequence - upldate line numbers

def cmdResequence(item):
  [num, step] = scanner.getItemSequence(item, 'sequence',
                ',', language.defaultStart, language.defaultStep)
  if item['error'] != 'OK':
    return item['error']

  return resequencer.resequence(num, step)

# number - prompt for input

def cmdNumber(item):
  [num, step] = scanner.getItemSequence(item, 'sequence',
                ',', language.defaultStart, language.defaultStep)
  if item['error'] != 'OK':
    return item['error']

  txt = 'xxx'
  prompt = str(num) + ' '
  while (txt != '') and (num < language.maxLine):
    txt = input(prompt)
    if txt != '':
      codeItem = {'code': str(num) + ' ' + txt, 'next': -1}
      data.codeList[num] = codeItem
      num = num + step
      prompt = str(num) + ' '

  return 'OK'

#  old - load file

def cmdOld(item):
  scanner.parseFileName(item)
  if item['error'] == 'OK':
    cmdNew(item)
    return readWrite.loadCodeFile(item['fileName'])
  return item['error']

#  merge another file

def cmdMerge(item):
  scanner.parseFileName(item)
  if item['error'] == 'OK':
    return readWrite.loadCodeFile(item['fileName'])
  return item['error']

#  save file

def cmdSave(item):
  scanner.parseFileName(item)
  if item['error'] == 'OK':
    return readWrite.saveCodeFile(item['fileName'])
  return item['error']

  #  quit

def cmdQuit(item):
  data.quitFlag = True
  return 'Bye'
