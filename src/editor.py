#  TI 99/4A BASIC 
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  editor.py - functions to edit the basic code

import parser
import helpers
import data

#  add or replace code lines

def addLine(n, code):
  if str(n) == code.strip():
    if n in data.codeList:
      data.codeList.pop(n)
    else:
      return 'Bad line number'
  else:
    data.codeList[n] = code  
  return 'OK'
  
#  parse the edit command
#  returns the line number and any error message
  
def preEdit(cmd):
  parts = cmd.split()
  if len(parts) < 2:
    return [-1, '', 'Bad command']
    
  if helpers.isnumeric(parts[1]) == False:
    return [-1, '', 'Bad command']
  
  n = int(parts[1])
  if n not in data.codeList:
    return [-1, '', 'Bad command']
  
  codeLine = data.codeList[n]
  i = codeLine.find(' ')
  if i > 0:
    code = codeLine[i + 1: len(codeLine)]  
  else:
    code = ''
  return [n, code, 'OK']
  
#  edit a line of code
#  uses the old HP line edit commands
#  spaces move the cursor to the position within the line
#  i inserts additional text
#  d deletes a character
#  r replaces existing text
  
def edit(txt, mask):
  functionList = {
    'D': editDelete,
    'I': editInsert,
    'R': editReplace    
  }
  
  shortMask = mask.lstrip()
  if len (shortMask) == 0:
    return txt
    
  i = len(mask) - len(shortMask)
  op = shortMask[0].upper()
  if op not in ['I', 'D', 'R']:
    op = 'R'
    
  return functionList[op](txt, i, shortMask)

#  delete characters
  
def editDelete(txt, i, mask):
  n = 0  
  for ch in mask:
    if ch.upper() == 'D':
      n = n + 1  
  return  txt[0: i] + txt[i + n: len(txt)]

#  insert text
  
def editInsert(txt, i, mask):
  return txt[0: i] + mask[1: len(mask)] + txt[i: len(txt)]

#  replace text

def editReplace(txt, i, mask):
  if mask[0] == 'R':    
    newMask = mask[1: len(mask)]
    return txt[0: i] + newMask + txt[i + len(newMask): len(txt)]
  else:
    return txt[0: i] + mask + txt[i + len(mask): len(txt)]

# resequence the code list
#  uses the parser to build the code tree
#  so we can replace line numbers within gosub and other similar commands

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

  