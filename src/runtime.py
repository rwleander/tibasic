#  runtime thread runs on second processor

import statements
import scanner
import data

#  main loop to run a program

def run():
  msg = 'Done'
  while data.address > 0:
    if data.traceFlag is True:
      print (data.address, end=' ')

    if data.breakFlag is True:
      return 'Break ' + str(data.address)

    codeItem = data.codeList[data.address]
    code = codeItem['code']
    data.address = codeItem['next']

    item = scanner.parseCommand(code)
    statements.executeStatement(item)
    if item['error'] != 'OK':
      msg = code + '\n' + item['error']
      return msg

    if data.address in data.breakList:
      data.breakFlag = True

  return msg


#  scan for data statements

def loadData():
  data.callList= {}
  data.dataList = []
  data.dataPointer = 0
  callCount = 0

  lineNumber = data.firstLine
  while lineNumber > 0:
    line = data.codeList[lineNumber]
    code = line['code']
    parts = code.split()
    if len(parts) > 1:
      if parts[1] == 'DATA':
        item = scanner.parseCommand(code)
        statements.doDataLoad(item)
        if item['error'] != 'OK':
          return code + '\n' + item['error']

      if parts[1] == 'SUB':
        item = scanner.parseCommand(code)
        statements.doSubLoad(item, line['next'])
        if callCount > 0:
          return 'Missing end sub'
        callCount = callCount + 1
        if item['error'] != 'OK':
          return item['error']

      if len(parts) > 2:
        if parts[1] in ['EXIT', 'END'] and parts[2] == 'SUB':
          if callCount < 1:
            return 'Missing sub'
          callCount = callCount - 1

    lineNumber = line['next']

  return 'OK'
