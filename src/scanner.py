# tokenize and scan code

import expressions
import data
import language

#  parse commands using the language model

def parseCommand(cmd):
  item = {}
  item['code'] = cmd
  item['error'] = 'OK'

  tokens = findTokens(cmd)
  tokens = upshiftTokens(tokens)
  item['tokens'] = tokens
  statement = getStatementName(item)
  item['statement'] = statement
  if statement == 'Bad command':
    item['error'] = statement
  else:
    item['statement'] = statement

    rules = language.statements[statement].split()
    checkRules(item, rules)

  return item

#  create a list of tokens from a line of text

def findTokens(cmd):
  tokens = []
  value = ''
  inQuotes = False

  for char in cmd:
    if char == '"':
      inQuotes = not inQuotes

    if inQuotes or char == '"':
      value = value + char
    elif char in language.delimiters:
      setDelimiter(char, value, tokens)
      value = ''
    elif char in language.operators:
      setOperator(char, value, tokens)
      value = ''
    else:
      value = value + char

  if value != '':
    tokens.append(value)
  return tokens

#  upshift tokens before parsing commands

def upshiftTokens(tokens):
  for i in range(0, len(tokens)):
    if type(tokens[i]) == str:
      if tokens[i][0] != '"':
        tokens[i] = tokens[i].upper()
  return tokens

#  handle two character tokens

def setOperator(char, value, tokens):
  if len(tokens) > 1:
    tmpOperator = tokens[len(tokens) - 1] + char
    if tmpOperator in language.operators:
      tokens[len(tokens) - 1] = tmpOperator
      return

  setDelimiter(char, value, tokens)

#  add delimiter to token list

def setDelimiter(char, value, tokens):
  if value != '':
    tokens.append(value)

  if char != ' ':
    tokens.append (char)

#  get the command name from a list of tokens
#  may need to refactor

def getStatementName(item):
  tokens = item['tokens']
  msg = 'Bad command'
  if len(tokens) == 0:
    return msg

  if tokens[0] in language.statements:
    return tokens[0]

  if checkSynonyms(item) is True:
    return item['statement']

  if len(tokens) < 2:
    return msg

  if tokens[1] in language.statements:
    return tokens[1]

  if checkImpliedLet(item) is True:
    return 'LET'

  if checkOnGosub(item) is True:
    return item['statement']

  if checkGoTo(item) is True:
    return item['statement']

  return msg

#  check for implied let

def checkImpliedLet(item):
  tokens = item['tokens']
  i = getTokenIndex(tokens, '=')
  if i < 0:
    return False

  if i == 0 :
    return False

  if isnumeric(tokens[0]):
    line = tokens[0]
    item['tokens'] = [line, 'LET'] + tokens[1: len(tokens)]
  else:
    item['tokens'] = ['LET'] + tokens
  item['statement'] = 'LET'
  return True

 #  find on gosub or on goto

def checkOnGosub(item):
  if 'ON' not in item['tokens']:
    return False

  item['tokens'] = joinGosub(item['tokens'])
  if 'GOSUB' in item['tokens']:
    item['statement'] = 'ON_GOSUB'
    return True

  if 'GOTO' in item['tokens']:
    item['statement'] = 'ON_GOTO'
    return True

  return False

 #  find goto or gosub

def checkGoTo(item):
  item['tokens'] = joinGosub(item['tokens'])
  if 'GOSUB' in item['tokens']:
    item['statement'] = 'GOSUB'
    return True

  if 'GOTO' in item['tokens']:
    item['statement'] = 'GOTO'
    return True

  return False

#  join go to and go sub

def joinGosub(tokens):
  i = getTokenIndex(tokens, 'GO')
  if i < 0:
    return tokens

  if i + 1 < len(tokens):
    if tokens[i + 1] in ['SUB', 'TO']:
      tokens[i] = tokens[i] + tokens[i + 1]
      tokens.pop(i + 1)

  return tokens

#  switch synonyms such as num to number

def checkSynonyms(item):
  tokens = item['tokens']
  found = False
  for syn in language.synonyms:
    i = getTokenIndex(tokens, syn)
    if i >= 0:
      item['tokens'][i] = language.synonyms[syn]
      item['statement'] = language.synonyms[syn]
      found = True

  return found

#  match command to statement rules

def checkRules(item, rules):
  tokens = item['tokens']
  key = ''
  lastIndex = 0
  i = 0
  optional = False

  for  rule in rules:
    if rule == '[':
      optional = True
    elif rule == ']':
      optional = False

    elif rule[0] >= 'a' and rule[0] <= 'z':
      key = rule
      lastIndex = i + 1
    else:
      i = getTokenIndex(tokens, rule)
      if i < 0:
        if optional is True:
          i = len(tokens)
        else:
          item['error'] = 'Bad command'
          return

      if lastIndex > 0:
        item[key] = tokens[lastIndex: i]
        lastIndex = 0

  if lastIndex > 0:
    item[key] = tokens[lastIndex: len(tokens)]

#  create the file name

def parseFileName(item):
  file = getItemValue(item, 'file')
  item['fileName'] = ''
  fileName = file.upper()
  if isValidVariable(fileName) is False:
    item['error'] = 'Bad file name'
  else:
    item['fileName'] = file.upper() + '.ti'

#  get parsed tokens from list

def getItemTokens(item, name):
  if name in item:
    return item[name]

  item['error'] = name + ' not in list'
  return []

#  get a value from a parsed statement

def getItemValue(item, name):
  tokens = getItemTokens(item, name)
  if item['error'] != 'OK':
    return ''
  if len(tokens) > 0:
    return tokens[0]
  return ''

#  get evaluated expression value

def getItemExpression(item, name):
  tokens = getItemTokens(item, name)
  if item['error'] != 'OK':
    return ''

  if len(tokens) == 0:
    item['error'] = 'Bad expression'
    return ''

  [value, msg] = expressions.evaluate(tokens)
  if msg != 'OK':
    item['error'] = msg
    return ''
  return value

#   get list of data items
#  strip commas, convert to float

def getItemData(item, name):
  tokens = getItemTokens(item, name)
  if item['error'] != 'OK':
    return []
  [values, msg] = stripCommas(tokens)
  if msg != 'OK':
    item['error'] = msg
  return values

#  get start, step for number and resequence commands

def getItemSequence(item, name, delimiter, start, end):
  numberList = {
    0: getItemSequence0,
    1: getItemSequence1,
    2: getItemSequence2,
    3: getItemSequence3
  }

  tokens = getItemTokens(item, name)
  if item['error'] != 'OK':
    return [0, 0]

  n = len(tokens)
  if n not in range(0, 4):
    return getItemSequenceError(item)

  return numberList[n](item, tokens, delimiter, start, end)

# parse values based on number of tokens

def getItemSequence0(item, tokens, delimiter, start, end):
  return [start, end]

def getItemSequence1(item, tokens, delimiter, start, end):
  if isnumeric(tokens[0]) is False:
    return getItemSequenceError(item)

  n = int(tokens[0])
  if delimiter == '-':
    return [n, n]

  return [n, end]

def getItemSequence2(item, tokens, delimiter, start, end):
  if delimiter == '-':
    return getItemSequence2Dash (item, tokens, delimiter, start, end)

  if tokens[0] != delimiter:
    return getItemSequenceError(item)

  if isnumeric(tokens[1]) is False:
    return getItemSequenceError(item)

  n = int(tokens[1])
  return [start, n]

def getItemSequence2Dash(item, tokens, delimiter, start, end):
  if tokens[1] == '-':
    if isnumeric(tokens[0]) is False:
      return getItemSequenceError(item)
    n = int(tokens[0])
    return [n, end]

  if tokens[0] != delimiter:
    return getItemSequenceError(item)

  if isnumeric(tokens[1]) is False:
    return getItemSequenceError(item)

  n = int(tokens[1])
  return [start, n]

def getItemSequence3(item, tokens, delimiter, start, end):
  if isnumeric(tokens[0]) is False:
    return getItemSequenceError(item)

  if tokens[1] != delimiter:
    return getItemSequenceError(item)

  if isnumeric(tokens[2]) is False:
    return getItemSequenceError(item)

  n1 = int(tokens[0])
  n2 = int(tokens[2])
  return [n1, n2]

def getItemSequenceError(item):
  item['error'] = 'Bad argument'
  return [-1, -1]


#  remove commas from list

def stripCommas(tokens):
  values = []
  for i in range(0, len(tokens)):
    if i % 2 == 0:
      if tokens[i] == ',':
        return [[], 'Bad list']
      if isnumeric(tokens[i]):
        values.append(int(tokens[i]))
      else:
        values.append(tokens[i])
    else:
      if tokens[i] != ',':
        return [[], 'Bad list']
  return [values, 'OK']

#--------------
#  helper functions

#  index the code list

def createIndex():

  #  create the index structure

  index = []
  data.firstLine = -1
  if len(data.codeList) == 0:
    return index

  for lineNumber in data.codeList:
    index.append(lineNumber)
  index.sort()

  #  add forward links to each codeList item

  data.firstLine = index[0]
  data.address = index[0]
  lastItem = {}
  for lineNumber in index:
    if lineNumber == data.firstLine:
      lastItem = data.codeList[lineNumber]
    else:
      codeItem = data.codeList[lineNumber]
      codeItem['next'] = -1
      lastItem['next'] = lineNumber
      lastItem = codeItem

  return index

#  does  this variable contain a string

def isStringVariable(txt):
  if txt == '':
    return False

  return txt[len(txt) - 1] == '$'

#  is this string numeric

def isnumeric(strWork):
  if type(strWork) in [int, float]:
    return True

  if strWork == '':
    return False
  for  ch in strWork:
    if ch not in "0123456789-.":
      return False

  return True

#  is this a valid variable name
#  may need to refactor

def isValidVariable(txt):
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  numbers = "0123456789"
  characters = ['@', '_']

  # if blank, quit

  if txt == '':
    return False

# if already in variables list, we're ok

  if txt in data.variables:
    return True

  # not a reserved word

  if txt  in language.reservedWords:
    return False

# cannot be more than 15 characters

  if len(txt) > 15:
    return False

  # first character must be a letter

  if txt[0] not in letters:
    return False

  # scan remaining characters  up to last

  for ch in txt[1: len(txt) - 1]:
    if ch not in letters and ch not in numbers and ch not in characters:
      return False

  # last character

  ch = txt[len(txt) - 1]
  if ch not in letters and ch not in numbers and ch not in characters and  ch != '$':
    return False

  return True

#  add surrounding quotes to strings

def addQuotes(txt):
  if txt == '':
    return '""'

  txtWork = txt
  if txtWork[0] != '"':
    txtWork = '"' + txtWork

  if txtWork[len(txtWork) - 1] != '"':
    txtWork = txtWork + '"'

  return txtWork

#  remove surrounding quotes

def stripQuotes(txt):
  if len(txt) < 3:
    return txt

  newTxt = txt
  if newTxt[0] == '"':
    newTxt = newTxt[1: len(txt)]

  if newTxt[len(newTxt) - 1] == '"':
    newTxt = newTxt[0: len(newTxt) - 1]

  return newTxt


  #  parse a line number, return -1 if not valid

def getLineNumber(txt):
  n = -1
  try:
    n = int(txt)
  except:
    return -1

  if n in range (1, language.maxLine + 1):
    return n

  return -1

#  get index of element in array

def getTokenIndex (tokens, string):
  if string in tokens:
    return tokens.index(string)

  return -1
