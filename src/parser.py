#  parser - scan code for errors and build parseList data structure

import data
import helpers

parseRules = {
  'BREAK': 'BREAK list',
  'DATA': 'DATA list',
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
  'OPTION': 'OPTION BASE n',
  'PRINT': 'PRINT [ list ]',  
  'RANDOMIZE': 'RANDOMIZE',
  'READ': 'READ list',
  'REM': 'REM expr',
  'RESTORE': 'RESTORE [ line ]',
  'RETURN': 'RETURN',  
  'STOP': 'STOP',
  'UNBREAK': 'UNBREAK list'  
}


#  parse the code list and place in parseList

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
    
  
  #  parse a command line

def parseCommand(cmd):

  functionList = {
    'BREAK': parseBreakList,
    'DATA': parseDataList,
    'DISPLAY': parsePrintList,
    'INPUT': parseInputList,
    'PRINT': parsePrintList,
    'READ': parseReadList,
'UNBREAK': parseBreakList    
  }

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
    
  if statement in functionList:
    msg = functionList[statement](item)
      
  return item 
      
# create an ordered list of line numbers

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

#  build the basic parse list from the index

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
  
#  parse individual statements based on statement keyword
  
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
  
#  split a line of code by the upper case keywords in the rule
  
def splitCode(code, ruleParts):
  codeParts = []
  lastKeyword = ''
  lastIndex = -1
  for word in ruleParts:
    
  # if word is upper case, truncate last expression then add to list
  
    if (word[0] < 'a' or word[0] > 'z'):
      if len(codeParts) > 0:
        l = len(codeParts)
        expr = codeParts[l - 1]
        i = expr.find(word)
        if i > 0:
          codeParts[l - 1] = expr[0: i - 1]
          
      j = code.find(word)
      if word != '[' and word != ']':
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
        i = lastIndex + len(lastWord) + 1
        codeParts.append(code[i: len(code)])
  return codeParts
  
#  add the expressions to the item list

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
      if expr == '' and optional == False:
        item['error'] = 'Missing expression'
        return item
    else:      
      if expr == '' and optional == False:
        item['error'] = 'Missing ' + word
        return item
    i = i + 1    
    if word != '[' and  word != ']':
      j = j + 1  
  return item
  
  
  #--------------------------
# parse input, print and other list based statements

def parseDetails():

  functionList = {
    'BREAK': parseBreakList,
    'DATA': parseDataList,
    'DIM': parseDimList,
    'DISPLAY': parsePrintList,    
    'INPUT': parseInputList,
    'ON': parseOnList,
    'PRINT': parsePrintList,
    'READ': parseReadList,
'UNBREAK': parseBreakList    
  }

  for lineNumber in data.index: 
    item = data.parseList[lineNumber]    
    statement = item['statement']    
    
    if statement in functionList:
      msg = functionList[statement](item)
      if msg != 'OK':
        return msg
        
  return 'OK'

#  parse the list of breakpoints for break and unbreak commands

def parseBreakList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['lines'] = values
  return 'OK'
  
#  parse the list of data items

def parseDataList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['data'] = values
  return 'OK'
  
  #  split dim statement
  
def parseDimList(item):
  listText = item['list']
  parts = splitCommaList(listText)
  vars = [] 
  
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
    vars.append(varList)
    
  item['vars'] = vars
  return 'OK'
  
  # parse the list of inputs
  
def parseInputList(item):
  listText = item['list']
  
  #  find prompt
  
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
  if keyword == 'GOTO' or keyword == 'GO TO':
    item['statement'] = 'ON_GOTO'
  
  if keyword == 'GOSUB' or keyword == 'GO SUB':
    item['statement'] = 'ON_GOSUB'
    
  item['lines'] = splitCommaList(listText[j: len(listText)])
  return 'OK'  
    
    
  
  
 

#  split the print list into its parts

def parsePrintList(item):
  listText = item['list']    
  parts = []
  part = ''
  inQuotes = False
  inParens = False
    
  for ch in listText:
    if ch == '"':
      inQuotes = not inQuotes
  
    if ch == '(':
      inParens = True
 
    
    if inQuotes == True or inParens == True:
      part = part + ch    
      if ch == ')':
        inParrens = False
      
    elif ch in [',', ':', ';']:
      if part != '':
        parts.append(part)  
      parts.append(ch)
      part = ''

    elif ch != ' ':
      part = part + ch    
        
  if part != '':
    parts.append(part)

  item['parts'] = parts
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
    
    if inQuotes == True or inParens == True:
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
      else:
        tmpItem = forStack.pop()
        tmpItem['forNext'] = lineNumber
        if item['var'] != tmpItem['var'] and item['var'] != '':
          return 'For-Next error'

    
  if len(forStack) > 0:
    return 'For-next error'
    
  return 'OK'
   