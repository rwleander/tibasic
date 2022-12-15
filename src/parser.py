#  parser - scan code for errors and build parseList data structure

import data
import helpers

parseRules = {
  'LET': 'LET var = expr',
  'PRINT': 'PRINT expr',
  'IF': 'IF expr THEN line1 [ ELSE line2 ]',
  'GOTO': 'GOTO line',
  'GOSUB': 'GOSUB line',
  'RETURN': 'RETURN',
  'FOR': 'FOR var = expr1 TO expr2 [ STEP expr3 ]',
'NEXT': 'NEXT',  
  'REM': 'REM expr',
  'STOP': 'STOP',
  'END': 'END'
}

#  parse the code list and place in parseList

def parse():
  rslt = createIndex()
  if (rslt != 'OK'):
    return rslt
    
  rslt = buildParseList()
  if rslt != 'OK':
    return rslt
  
  rslt = parseStatements()
  return rslt
  

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
    data.parseList[lineNumber] = item
    
    if lastLine > 0:
      data.parseList[lastLine]['nextLine'] = lineNumber  
    lastLine = lineNumber
  return 'OK'
  
#  parse individual statements based on statement keyword
  
def parseStatements():
  i = 0
  while (i < len(data.index)):
    lineNumber = data.index[i]
    item = data.parseList[lineNumber]
    statement = item['statement']
    code = item['code']
    if statement not in parseRules:
      return code + '\n' + 'Unknown statement'
      
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
  i = 0
  j = 0
  while (i < len(ruleParts) and j < len(codeParts)):
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
    
  