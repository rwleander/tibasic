#  TI 99/4A BASIC
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  readWrite.py - functions to read and write program code and data
#

import os

import commands
import scanner
import expressions
import statements
import data


#  load a program file

def loadCodeFile(fileName):
  if fileExists(fileName) is False:
    return 'No data found'

  with open (fileName, 'r', encoding='UTF-8') as fl:
    while  (line := fl.readline().strip()):
      commands.executeCommand(line)
    fl.close()

  return 'OK'

#  save the current code file to disk

def saveCodeFile(fileName):
  index = scanner.createIndex()

  with open (fileName, 'w', encoding='UTF-8') as fl:
    for lineNumber in index:
      codeItem = data.codeList[lineNumber]
      fl.write (codeItem['code'] + '\n')
    fl.close()
  return 'OK'

#  delete a code file

def deleteCodeFile(fileName):
  if fileExists(fileName) is False:
    return 'No data found'

  os.remove(fileName)
  return 'OK'

#  use the print area to list program and data files

def listFiles():
  printArea = initPrint(data.printWidth, data.printTab)
  formatText(printArea, 'Program files:')
  formatNewLine(printArea)
  codeFiles = os.listdir()
  for file in codeFiles:
    if file.find('.ti') > 0:
      file = file.replace('.ti', '')
      formatText(printArea, file)
      formatComma(printArea)
  formatNewLine(printArea)
  return printArea


#-----------------------
#  helper functions

#  does file exist

def fileExists(fileName):
  files = os.listdir()
  return fileName in files

#----------------------
#  input functions

#  load data from input command

def loadInput(variables, txt):
  [varList, msg] = scanner.stripCommas(variables)
  if msg != 'OK':
    return msg

  tokens = scanner.findTokens(txt)
  [values, msg] = scanner.stripCommas(tokens)
  if msg != 'OK':
    return msg

  if len(varList) != len(values):
    return 'Bad input'

  i = 0
  for varName in varList:
    msg = statements.saveVariable(varName, values[i])
    if msg != 'OK':
      return 'Bad input'
    i = i + 1
  return 'OK'

#----------------------
#  format routines for print and display commands

#  initialize print structure

def initPrint(width, tab):
  return {
    'buff': '',
    'lines': [],
    'width': width,
    'tab': tab,
    'error': 'OK'
  }

#  format print statements
#
#  warning - this gets a bit difficult
#  work is done in the print area
#  then results can be found in printArea['lines']

def formatPrint(printArea, printList):
  delimiters = {
    ',': formatComma,
    ';': formatSemi,
    ':': formatNewLine
  }

  printArea['lines'] = []
  if len(printList) == 0:
    formatNewLine(printArea)
    return printArea['lines']

  expr = []
  for token in printList:
    if token in delimiters:
      formatExpression(printArea, expr)
      delimiters[token](printArea)
      expr = []
    else:
      expr.append(token)

  if len(expr) > 0:
    formatExpression(printArea, expr)

  if printList[len(printList) - 1] not in delimiters:
    formatNewLine(printArea)

  return printArea['lines']

#  add spaces to complete a column

def formatComma(printArea):
  l = len(printArea['buff'])
  if l > printArea['width'] - printArea['tab']:
    formatNewLine(printArea)
    return
  t = printArea['tab'] - (l % printArea['tab'])
  printArea['buff'] = printArea['buff'] + t * ' '

#  ad a space

def formatSemi(printArea):
  l = len(printArea['buff'])
  if l < printArea['width']:
    printArea['buff'] = printArea['buff'] + ' '
  else:
    formatNewLine(printArea)

#  add expresion to line

def formatExpression(printArea, expr):
  lBuff = len(printArea['buff'])
  [value, msg] = expressions.evaluate(expr)
  if msg != 'OK':
    printArea['error'] = msg
    return

  if type(value) in [float, int, bool]:
    value = str(value)
  if len(value) > 0:
    if value[0] == '"':
      value = scanner.stripQuotes(value)
  if value[len(value) -2: len(value)] == '.0':
    value = value[0: len(value) - 2]
  lValue = len(value)
  if lBuff + lValue > printArea['width']:
    formatNewLine(printArea)
  printArea['buff'] = printArea['buff'] + value

#  add text to print area

def formatText(printArea, txt):
  lBuff = len(printArea['buff'])
  l = len(txt)
  if lBuff + l > printArea['width']:
    formatNewLine(printArea)
  printArea['buff'] = printArea['buff'] + txt

#  add  buff to line

def formatNewLine(printArea):
  printArea['lines'].append(printArea['buff'])
  printArea['buff'] = ''
