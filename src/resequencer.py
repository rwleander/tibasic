#  resequencer - resequence code found in data.codelist

import scanner
import language
import data

#  resequence the list

def resequence(start, step):
  functionList = {
    'BREAK': replaceGosub,
    'GOSUB': replaceGosub,
    'GOTO': replaceGosub,
    'IF': replaceIf,
    'ON_GOSUB': replaceOnGosub,
    'ON_GOTO': replaceOnGosub
  }

  newCodeList = {}
  index = scanner.createIndex()
  xref = createXref(index, start, step)

  for lineNumber in index:
    codeItem = data.codeList[lineNumber]
    code = codeItem['code']
    item = scanner.parseCommand(code)

    newLine = getNewLine(xref, lineNumber)
    newCode = replaceLineNumber(xref, code, newLine)

    statement = item['statement']
    if statement in functionList:
      newCode = functionList[statement](xref, newCode, item)

    newCodeList[newLine] = {
      'code': newCode,
      'next': -1
    }

  data.codeList = newCodeList
  return 'OK'

#  create cross reference from index

def createXref(index, start, step):
  xref = {}
  n = start
  for lineNumber in index:
    xref[lineNumber] = n
    n = n + step
  return xref

#  replace the starting line number for a line of code

def replaceLineNumber(xref, code, newLine):
  num = str(newLine)
  i = code.find(' ')
  if i < 0:
    return num
  return num + code[i: len(code)]

#  replace line numbers inside if - then

def replaceIf(xref, code, item):
  line1 = scanner.getItemValue(item, 'line1')
  newLine1 = getNewText(xref, line1)
  line2 = scanner.getItemValue(item, 'line2')
  newLine2 = getNewText(xref, line2)

  iThen = code.find(' THEN ')
  if iThen < 0:
    return code

  iElse = code.find(' ELSE')

  newCode = code[0: iThen]
  newCode = newCode + ' THEN ' + newLine1

  if iElse > 0:
    newCode = newCode + ' ELSE ' + newLine2
  return newCode

#  replace line number in gosub or goto

def replaceGosub(xref, code, item):
  line = scanner.getItemValue(item, 'line')
  newLine = getNewText(xref, line)

  n = -1
  for keyword in [' BREAK ', ' GOSUB ', 'GO SUB ', ' GOTO ', ' GO TO ']:
    i = code.find(keyword)
    if i > 0:
      n = i + len(keyword)
  if n < 0:
    return code

  newCode = code[0: n] + newLine
  return newCode
#  replace line numbers after on gosub

def replaceOnGosub(xref, code, item):
  lineList = scanner.getItemData(item, 'list')

  n = -1
  for keyword in [' GOSUB ', 'GO SUB ', ' GOTO ', ' GO TO ']:
    i = code.find(keyword)
    if i > 0:
      n = i + len(keyword)
  if n < 0:
    return code

  newCode = code[0: n]
  for lineNum in lineList:
    newLine = getNewLine(xref, lineNum)
    newCode = newCode + str(newLine) + ', '

  newCode = newCode[0: len(newCode) -2]
  return newCode

#--------------------------
#  helper functions

#  get new line from cross reference

def getNewLine(xref, n):
  if n in xref:
    return xref[n]
  return language.maxLine

#  get new line number from text string

def getNewText(xref, txt):
  if scanner.isnumeric(txt) is False:
    return str(language.maxLine)

  n = int(txt)
  return str(getNewLine(xref, n))
  