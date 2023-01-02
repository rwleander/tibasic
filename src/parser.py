#  parser - scan code for errors and build parseList data structure

import data
import helpers

parseRules = {
  'DATA': 'DATA list',
  'END': 'END',
  'FOR': 'FOR var = expr1 TO expr2 [ STEP expr3 ]',
  'GO': 'GO type line',
  'GOSUB': 'GOSUB line',
  'GOTO': 'GOTO line',
  'IF': 'IF expr THEN line1 [ ELSE line2 ]',
  'INPUT': 'INPUT list',
  'LET': 'LET var = expr',
  'NEXT': 'NEXT',  
  'PRINT': 'PRINT expr',  
  'RANDOMIZE': 'RANDOMIZE',
  'READ': 'READ list',
  'REM': 'REM expr',
  'RESTORE': 'RESTORE [ line ]',
  'RETURN': 'RETURN',  
  'STOP': 'STOP'  
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
  return msg
  
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
  for lineNumber in data.index: 
    item = data.parseList[lineNumber]
    statement = item['statement']
    
    if statement == 'DATA':
      msg =  parseDataList(item)
      if msg != 'OK':
        return msg
      
    if statement == 'INPUT':
      msg =  parseInputList(item)
      if msg != 'OK':
        return msg
  
    if statement == 'READ':
      msg = parseReadList(item)
      if msg != 'OK':
        return msg
      
  return 'OK'

#  parse the list of data items

def parseDataList(item):
  listText = item['list']
  values = splitCommaList(listText)
  item['data'] = values
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
 
  for ch in txt:
    if ch == '"':
      inQuotes = not inQuotes
    
    if ch == ',':
      if value != '':
        values.append (value)
      value = ''

    elif ch == ' ':
      if inQuotes:
        value = value + ch
    
    else:
      value = value + ch
      
  if value != '':
    values.append (value)
  return values
