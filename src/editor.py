#  editor - functions to edit code

import parser
import data

# resequence the code list

def resequence(base, step):
  functionList = {
    'GOTO': resequenceGoto,
    'GOSUB': resequenceGoto,
    'IF': resequenceIf,
    'ON_GOSUB': resequenceOn,
    'ON_GOTO': resequenceOn 
  }
  
  newList = {}
  xref = {}
  newNumber = base  
  
  msg = parser.parse()
  if msg != 'OK':
    return msg
  for lineNumber in data.index:
    xref[lineNumber] = newNumber
    newNumber = newNumber + step
    
  for lineNumber in data.index:
    item = data.parseList[lineNumber]
    statement = item['statement']
    newNumber = xref[lineNumber]
    if statement in functionList:
      newLine = functionList[statement](lineNumber, newNumber, item, xref)
    else:
      newLine = resequenceLine(lineNumber, newNumber, item, xref)
    newList[newNumber] = newLine
      
  data.codeList = newList
  return 'OK'
    
    
    # default function to build resequenced line
    
def resequenceLine(oldNumber, newNumber, item, xref):
  code = item['code']
  i = code.find(' ')
  if i > 1:
    newLine = str(newNumber) + code[i: len(code)]
  else:
    newLine = code

  return newLine
  
#  resequence goto, gosub

def resequenceGoto(oldNumber, newNumber, item, xref):      
  statement = item['statement']
  oldGoto = int(item['line'])
  newGoto = xref[oldGoto]
  return  str(newNumber) + ' ' + statement + ' ' + str(newGoto)
  
  #  resequence if statements
  
def resequenceIf(oldNumber, newNumber, item, xref):      
  statement = item['statement']
  expr = item['expr']
  oldLine1 = int(item['line1'])
  if oldLine1 in xref:
    newLine1 = xref[oldLine1]  
  else:
    newLine1 = data.maxLine
  newText = str(newNumber) + ' ' + statement + ' ' + expr + ' THEN ' + str(newLine1)
  
  if 'line2' in item:
    oldLine2 = int(item['line2'])
    if oldLine2 in xref:
      newLine2 = xref[oldLine2]
    else:
      newLine2 = data.maxNumber
    newText = newText + ' ELSE ' + str(newLine2)
    
  return newText
  
    
  return  str(newNumber) + ' ' + statement + ' ' + str(newGoto)
  
#  resequence on goto, on gosub    

def resequenceOn(oldNumber, newNumber, item, xref):      
  statement = item['statement']
  expr = item['expr']
  lines = item['lines']
  newText = str(newNumber) + ' ON ' + expr

  if statement == 'ON_GOSUB':
    newText = newText + ' GOSUB '
  else:
    newText = newText + ' GOTO '  
  
  if len(lines) == 0:
    return newText
    
  for old  in lines:
    n1 = int(old)
    if n1 in xref:
      n2 = xref[n1]
      newText = newText  + str(n2) + ', '
    else:
      newText = str(data.maxNumber) + ', '
    
  return newText[0: len(newText) - 2]  
  return newText[0: len(newText) - 2]  

  