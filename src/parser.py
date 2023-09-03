#  TI 99/4A BASIC
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  parser - scan code for errors and build parseList data structure
#
#  Entry points:
#
#  Parse the code found in data.codeList:
#    msg = parser.parse()
#
#  Parse the single line command in string cmd:
#    item = parser.parseCommand(cmd)
#
# All functions return either 'OK' or an error message
#

import data
import helpers

#  the parseRules dictionary contains a list of
#  statements and their formats

parseRules = {
  'BREAK': 'BREAK [ list ]',
  'CLOSE': 'CLOSE list',
  'DATA': 'DATA list',
  'DEF': 'DEF func = expr',
  'DIM': 'DIM list',
  'DISPLAY': 'DISPLAY [ list ]',
  'END': 'END',
  'FOR': 'FOR var = expr1 TO expr2 [ STEP expr3 ]',
  'GO': 'GO type line',
  'GOSUB': 'GOSUB line',
  'GOTO': 'GOTO line',
  'IF': 'IF expr THEN line1 [ ELSE line2 ]',
  'INPUT': 'INPUT list',
  'LET': 'LET var = expr',
  'NEXT': 'NEXT [ var ]',
  'ON': 'ON list',
  'OPEN': 'OPEN list',
  'OPTION': 'OPTION BASE n',
  'PRINT': 'PRINT [ list ]',
  'RANDOMIZE': 'RANDOMIZE',
  'READ': 'READ list',
  'REM': 'REM [ expr ]',
  'RESTORE': 'RESTORE [ line ]',
  'RETURN': 'RETURN',
  'STOP': 'STOP',
  'TRACE': 'TRACE',
  'UNBREAK': 'UNBREAK [ list ]',
'UNTRACE': 'UNTRACE'
}


#  parse each line in data.codeList into a dictionary object,
#  then   add it to data.parseList by line number

def parse():
  msg = createIndex()
  if msg != 'OK':
    return msg

  msg = buildParseList()
  if msg != 'OK':
    return msg

  msg = parseStatements()
  if msg != 'OK':
    return msg

  msg = parseDetails()
  if msg != 'OK':
    return msg

  msg = scanForNext()
  return msg


# parse a single command line and return a dictionary containing the parsed data

def parseCommand(cmd):
  parts = cmd.split()
  statement = parts[0]

  item = {}
  item['code'] = cmd
  item['statement'] = statement
  item['nextLine'] = -1
  item['error'] = 'OK'
  item['source'] = 'command'

      # parse by statement type

  if statement not in parseRules:
    item['error'] = 'Bad command'
    return item

  rule = parseRules[statement]
  ruleParts = rule.split()
  codeParts= splitCode('00 ' + cmd, ruleParts)
  item = addExpressions(item, ruleParts, codeParts)

  selectParseFunction(item)
  return item


# ---------------------
#  local functions

# create an ordered list of line numbers in data.index
#  this array is used to list and save data.codeList in order by line number

def createIndex():
  data.index = []
  data.firstLine = -1
  if len(data.codeList) == 0:
    return 'No code'

  for lineNumber in data.codeList:
    data.index.append(lineNumber)
  data.index.sort()
  data.firstLine = data.index[0]
  return 'OK'

#  create a dictionary item for each line of code
#  containing the code,, code parts, next line and error message,
#  then add each to data.parseList

def buildParseList():
  data.parseList = {}
  lastLine = -1
  for lineNumber in data.index:
    item = {}
    code = data.codeList[lineNumber]
    parts = code.split()
    item['code'] = code
    item['statement'] = parts[1]
    item['nextLine'] = -1
    item['error'] = 'OK'
    item['source'] = 'runtime'

    # if implied let, set statement type to let

    if len(parts) > 2:
      if parts[2] == '=':
        item['statement'] = 'LET'

    data.parseList[lineNumber] = item

    if lastLine > 0:
      data.parseList[lastLine]['nextLine'] = lineNumber
    lastLine = lineNumber
  return 'OK'

#  parse individual statements using the parseRules dictionary
#  for each line, add keywords and values to match the statement rules
#  for example: LET A = B + C becomes {'statement': 'LET', 'var': 'A', 'expr': 'B + C'}

def parseStatements():
  i = 0
  while i < len(data.index):
    lineNumber = data.index[i]
    item = data.parseList[lineNumber]
    statement = item['statement']
    code = item['code']

    if statement not in parseRules:
      return code + '\n' + 'Unknown statement'

    # if implied let, add keyword

    if statement == 'LET' and code.find('LET') < 0:
      j = code.find(' ')
      code = code[0: j] + ' LET' + code[j:len(code)]

    rule = parseRules[statement]
    ruleParts = rule.split()
    codeParts= splitCode(code, ruleParts)
    newItem = addExpressions(item, ruleParts, codeParts)
    data.parseList[lineNumber] = newItem
    i = i + 1
  return 'OK'

#  split one line of code into its parts using the rule
#  function matches upper case keywords to determine parts
#  hope to refactor this code to make it more resilient and handle additional elements

def splitCode(code, ruleParts):
  codeParts = []
  lastWord = ''
  lastIndex = -1
  for word in ruleParts:

  # if word is upper case, truncate last expression then add to list

    if (word[0] < 'a' or word[0] > 'z'):
      if len(codeParts) > 0:
        l = len(codeParts)
        expr = codeParts[l - 1]
        i = expr.find(word)
        if i > 0:
          codeParts[l - 1] = expr[0: i].strip()

      j = code.find(word)
      if word not in [ '[', ']']:
        if j > 1:
          codeParts.append(word)
          lastWord = word
          lastIndex = j
        else:
          codeParts.append('')
          lastWord = ''
          lastIndex = -1

    # if lower case, add new expression

    else:
      if lastIndex > 0:
        i = lastIndex + len(lastWord)
        codeParts.append(code[i: len(code)].strip())
  return codeParts

#  match up the rule and the extracted code items and add them to data.parseList
#  this also needs to be refactored to make it more readable

def addExpressions(item, ruleParts, codeParts):
  optional = False

  # for GO TO / GO SUB, fix up type and line

  if 'statement' in item:
    if item['statement'] == 'GO':
      tmpParts = codeParts[1].split()
      codeParts[1] = tmpParts[0]
      codeParts[2] = tmpParts[1]

  i = 0
  j = 0
  while (i < len(ruleParts)) and (j < len(codeParts)):
    word = ruleParts[i]
    expr = codeParts[j].strip()
    if word == '[':
      optional = True

    if word[0] >= 'a' and word[0] <= 'z':
      item[word] = expr
      if expr == '' and optional is False:
        item['error'] = 'Missing expression'
        return item
    else:
      if expr == '' and optional is False:
        item['error'] = 'Missing ' + word
        return item
    i = i + 1
    if word not in ['[', ']']:
      j = j + 1
  return item


#--------------------------
#  second level parsing for more difficult statements

# check each item in parse list then, if necessary,
#  call additional functions to fill in details

def parseDetails():
  for lineNumber in data.index:
    item = data.parseList[lineNumber]
    msg = selectParseFunction(item)
    if msg != 'OK':
      return msg

  return 'OK'

#  if found in the function list, call the appropriate function

def selectParseFunction(item):

  functionList = {
    'BREAK': parseBreakList,
    'CLOSE': parseCloseList,
    'DATA': parseDataList,
    'DEF': parseDefList,
    'DIM': parseDimList,
    'DISPLAY': parsePrintList,
    'INPUT': parseInputList,
    'ON': parseOnList,
    'OPEN': parseOpenList,
    'PRINT': parsePrintList,
    'READ': parseReadList,
'UNBREAK': parseBreakList
  }

  statement = item['statement']
  if statement in functionList:
    return functionList[statement](item)

  return 'OK'

#  determine  the list of breakpoints for break and unbreak commands

def parseBreakList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['lines'] = values
  return 'OK'

#  parse the close statement

def parseCloseList(item):
  listText = item['list']
  values = listText.split(':')
  if len(values) > 2:
    item['error'] = 'Bad statement'
    return 'Bad statement'

  fNum = values[0].strip()
  if fNum[0] != '#':
    item['error'] = 'Bad file number'
    return 'Bad file number'
  fNum = fNum[1: len(fNum)]
  if helpers.isnumeric (fNum) is False:
    item['error'] = 'Bad file number'
    return 'Bad file number'
  item['fileNum'] = int(fNum)

  item['delete'] = 'No'
  if len(values) == 2:
    if values[1].strip() == 'DELETE':
      item['delete'] = 'DELETE'
    else:
      item['error'] = 'Bad statement'
      return 'Bad statement'

  return 'OK'

#  split  the list of data items

def parseDataList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['data'] = values
  return 'OK'

#  split function and argument

def parseDefList(item):
  func = item['func']
  funcParts = func.split('(')
  if len(funcParts) < 2:
    return 'Bad statement'

  funcName = funcParts[0].strip()
  if helpers.isValidVariable(funcName) is False:
    return 'Bad function name'

  arg = funcParts[1]
  item['function'] = funcName
  item['arg'] = arg[0:len(arg) - 1].strip()
  return 'OK'

#  split dim statements

def parseDimList(item):
  listText = item['list']
  parts = splitCommaList(listText)
  variables = []

  for part in parts:
    i = part.find('(')
    if i < 0:
      return 'Bad statement '

    j = part.find(')')
    if j < i:
      return 'Bad statement'

    varName = part[0: i].strip()
    varList = {}
    varList['id'] = varName
    varList['size'] = part[i + 1: j].strip()
    variables.append(varList)

  item['vars'] = variables
  return 'OK'

# determine  the list of variables for the input statement

def parseInputList(item):
  listText = item['list']

# find the prompt - if it was specified
#  otherwise default to question mark

  prompt = '?'
  if listText[0] == '"':
    p = listText.find('"', 1)
    if p > 1:
      if listText[p + 1] != ':':
        item['error'] = 'Bad prompt'
      prompt = listText[1: p]
      listText = listText[p + 2: len(listText)]
    else:
      item['error'] = 'Bad prompt'
  item['prompt'] = prompt

#  find file number

  fileNum = 0
  if listText[0] == '#':
    f = listText.find(':')
    if f > 0:
      txt = listText[1: f]
      if helpers.isnumeric(txt):
        fileNum = int(txt)
      else:
        item['error'] = 'Bad statement'
    listText = listText[f + 1: len(listText)]

  item['fileNum'] = fileNum

  inputs = splitCommaList(listText)
  item['inputs'] = inputs
  return 'OK'

#  parse on gosub or on goto statement

def parseOnList(item):
  listText = item['list']

  i = listText.find('GO')
  if i < 2:
    item['error'] = 'Bad statement'
    return 'Bad statement'

  item['expr'] = listText[0: i].strip()

  j = listText.find(' ', i + 3)
  if j < i:
    item['error'] = 'Bad statement'
    return 'Bad statement'

  keyword = listText[i: j]
  if keyword in ['GOTO', 'GO TO']:
    item['statement'] = 'ON_GOTO'

  if keyword in ['GOSUB', 'GO SUB']:
    item['statement'] = 'ON_GOSUB'

  item['lines'] = splitCommaList(listText[j: len(listText)])
  return 'OK'

#  parse the items found in an open statement

def parseOpenList(item):
  listText = item['list']
  parts = splitCommaList(listText)
  if len(parts) < 2:
    item['error'] = 'Bad statement'
    return 'Bad statement'

  fNum = parts[0].strip()
  fileNum = parseOpenFileNum(fNum)
  if fileNum < 0:
    item['error'] = 'Bad file number'
    return 'Bad file number'

  fileName = parts[1].strip()
  if fileName[0] != '"' or fileName[len(fileName) - 1] != '"':
    item['error'] = 'Bad file name'
    return 'Bad file name'
  fileName = helpers.upshift(fileName)
  fileName = helpers.stripQuotes(fileName)
  if helpers.isValidVariable(fileName) is False:
    item['error'] = 'Bad file name'
    return 'Bad file name'

  fileOrg = 'S'
  maxRecs = 0
  if len(parts) >= 3:
    [fileOrg, maxRecs] = parseOpenFileOrg(parts[2])
    if fileOrg == 'X':
      item['error'] = 'Bad file org'
      return 'Bad file org'

  fileType = 'D'
  if len(parts) >= 4:
    fType = parts[3].strip()
    if fType not in ['DISPLAY', 'INTERNAL', '']:
      item['error'] = 'Bad file type'
      return 'Bad file type'
    if fType != '':
      fileType = fType[0]

  fileMode = 'U'
  if len(parts) >= 5:
    fMode = parts[4].strip()
    if fMode not in ['INPUT', 'OUTPUT', 'UPDATE', 'APPEND', '']:
      item['error'] = 'Bad file mode'
      return 'Bad file mode'
    if fMode != '':
      fileMode = fMode[0]

  recType = 'F'
  recWidth = 80
  if len(parts) >= 6:
    [recType, recWidth] = parseOpenFileRecType(parts[5])
    if recWidth < 0:
      item['error'] = 'Bad record type'
      return 'Bad record type'

  fileLife = 'P'
  if len(parts) >= 7:
    fLife = parts[6].strip()
    if fLife not in ['PERMANENT', 'TEMPORARY', '']:
      item['error'] = 'Bad file life'
      return 'Bad file life'
    if fLife != '':
      fileLife = fLife[0]

  item['list'] = listText
  item['fileNum'] = fileNum
  item['fileName'] = fileName + '.dat'
  item['fileOrg'] = fileOrg
  item['maxRecs'] = maxRecs
  item['fileType'] = fileType
  item['fileMode'] = fileMode
  item['recType'] = recType
  item['recWidth'] = recWidth
  item['life'] = fileLife
  return 'OK'

#  get the file number

def parseOpenFileNum(fNum):
  if fNum[0] != '#':
    return -1

  fNum =fNum[1: len(fNum)]
  if helpers.isnumeric(fNum) is False:
    return -1

  fileNum = int(fNum)
  if fileNum not in range(1, 255):
    return -1

  return fileNum

  #  parse file organization and number of records from open statement

def parseOpenFileOrg(fOrg):
  fileOrg = 'S'
  maxRecs = 0
  parts = fOrg.split()
  if len(parts) > 2:
    return ['X', -1]

  org = parts[0].strip()
  if org not in ['RELATIVE', 'SEQUENTIAL', '']:
    return ['X', -1]

  if org != '':
    fileOrg = org[0]

  if len(parts) == 1:
    return [fileOrg, 0]

  maxStr = parts[1].strip()
  if helpers.isnumeric(maxStr) is False:
    return ['X', -1]

  maxRecs = int(maxStr)
  return [fileOrg, maxRecs]

    #  parse record type

def parseOpenFileRecType(recTypeItem):
  recType = 'F'
  recWidth = 80
  parts = recTypeItem.split()
  if len(parts) > 2:
    return ['X', -1]

  rType = parts[0].strip()
  if rType not in ['FIXED', 'VARIABLE', '']:
    return ['X', -1]

  if rType != '':
    recType = rType[0]

  if len(parts) < 2:
    return [recType, recWidth]

  rWidth = parts[1].strip()
  if helpers.isnumeric(rWidth) is False:
    return ['X', -1]

  recWidth = int(rWidth)
  return [recType, recWidth]


#  split the print list into its parts

def parsePrintList(item):
  listText = item['list']
  parts = []
  fileNum = 0
  part = ''
  inQuotes = False
  inParens = False

  for ch in listText:
    if ch == '"':
      inQuotes = not inQuotes

    if ch == '(':
      inParens = True

    if inQuotes or inParens:
      part = part + ch

    elif ch in [',', ':', ';']:
      if part != '':
        parts.append(part)
      parts.append(ch)
      part = ''

    elif ch != ' ':
      part = part + ch

  if part != '':
    parts.append(part)

  if len(parts) > 2:
    parts0 = parts[0]
    if parts0[0] == '#':
      parts0 = parts0[1: len(parts0)]
      if not helpers.isnumeric(parts0):
        return 'Bad statement'
      fileNum = int(parts0)
      parts.pop(1)
      parts.pop(0)

  item['parts'] = parts
  item['fileNum'] = fileNum
  return 'OK'

#  [parse read statement

def parseReadList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['inputs'] = values
  return 'OK'


#  split comma delimited lists

def splitCommaList(txt):
  values = []
  value = ''
  inQuotes = False
  inParens = False

  for ch in txt:
    if ch == '"':
      inQuotes = not inQuotes

    if ch == '(':
      inParens = True

    if inQuotes or inParens:
      value = value + ch
      if ch == ')':
        inParens = False

    elif ch == ',':
      if value != '':
        values.append (value.strip())
      value = ''

    else:
      value = value + ch

  if value != '':
    values.append (value.strip())
  return values



  # Finally, tie together the for and next statements

def scanForNext():
  forStack = []

  for  lineNumber in data.index:
    item = data.parseList[lineNumber]
    if item['statement'] == 'FOR':
      forStack.append(item)

    if item['statement'] == 'NEXT':
      if len(forStack) == 0:
        item['error'] = 'For-next error'
        return 'For-next error'

      tmpItem = forStack.pop()
      tmpItem['forNext'] = lineNumber
      if item['var'] != tmpItem['var'] and item['var'] != '':
        return 'For-Next error'

  if len(forStack) > 0:
    return 'For-next error'

  return 'OK'
