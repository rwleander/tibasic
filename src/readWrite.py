#  TI 99/4A BASIC
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  readWrite.py - functions to read and write program code and data
#

import os

import parser
import commands
import expressions
import data
import helpers


#  load a program file

def loadCodeFile(fileName):
  if helpers.fileExists(fileName) is False:
    return 'No data found'

  with open (fileName, 'r', encoding='UTF-8') as fl:
    while  (line := fl.readline().strip()):
      line = helpers.upshift(line)
      commands.cmdAddLine(line)
    fl.close()

  return 'OK'

#  save the current code file to disk

def saveCodeFile(fileName):
  parser.createIndex()

  with open (fileName, 'w', encoding='UTF-8') as fl:
    for lineNumber in data.index:
      fl.write (data.codeList[lineNumber] + '\n')
    fl.close()
  return 'OK'

#  delete a code file

def deleteCodeFile(fileName):
  if helpers.fileExists(fileName) is False:
    return 'No data found'

  os.remove(fileName)
  return 'OK'

#  list code files in storage

def listCodeFiles():
  strWork = ''
  n = 0
  files  = os.listdir()
  for file in files:
    i = file.find('.ti')
    j = file.find('\\')
    if (i > 0) and (j < 0):
      strWork = strWork + file[0:i] + '\t'
      n = n + 1

  if n > 0:
    return strWork[0:len(strWork)-1]

  return 'No files'

#--------------------------
#  functions to open a file

def openFile(item):
  openFunctions = {
    'I': openFileInput,
    'O': openFileOutput,
    'A': openFileAppend,
    'U': openFileUpdate
  }

  fileNum = item['fileNum']
  if fileNum in data.fileList:
    item['error'] = 'Bad file number'
    return

  fileMode = item['fileMode']
  fileItem = {}
  fileItem['fileNum'] = item['fileNum']
  fileItem['fileName'] = item['fileName']
  fileItem['fileOrg'] = item['fileOrg']
  fileItem['maxRecs'] = item['maxRecs']
  fileItem['fileType'] = item['fileType']
  fileItem['fileMode'] = fileMode
  fileItem['recType'] = item['recType']
  fileItem['recWidth'] = item['recWidth']
  fileItem['life'] = item['life']
  fileItem['eof'] = 0
  fileItem['error'] = 'OK'

  if fileMode in openFunctions:
    openFunctions[fileMode] (fileItem)
  else:
    fileItem['error'] = 'Bad file mode - ' + fileMode

  if fileItem['error'] == 'OK':
    data.fileList[fileNum] = fileItem
  else:
    item['error'] = fileItem['error']

#  open a file for input

def openFileInput(fileItem):
  fileName = fileItem['fileName']
  fl = open(fileName, 'r', encoding='UTF-8')
  fileItem['fileHandle'] = fl
  prereadFile(fileItem)

#  open file for output

def openFileOutput(fileItem):
  fileName = fileItem['fileName']
  fl = open(fileName, 'w', encoding='UTF-8')
  fileItem['fileHandle'] = fl

def openFileAppend(fileItem):
  fileName = fileItem['fileName']
  fl = open(fileName, 'a', encoding='UTF-8')
  fileItem['fileHandle'] = fl

#  open a file for update

def openFileUpdate(fileItem):
  fileItem['error'] = 'Not ready'

#  read data from file

def inputFile(item):
  fileNum = item['fileNum']
  if fileNum not in data.fileList:
    item['error'] = 'File ' + str(fileNum) + ' not open'
    return

  fileItem = data.fileList[fileNum]
  if fileItem['eof'] != 0:
    item['error'] = 'Out of data'
    return

  buff = fileItem['buff']
  varList = item['inputs']
  item['error'] = processInputsFromString(varList, buff)
  prereadFile(fileItem)

  #  pre-read a record from the file

def prereadFile(fileItem):
  fl = fileItem['fileHandle']
  buff = fl.readline()
  eof = 0
  if buff == '':
    eof = 1
  fileItem['buff'] = buff.strip()
  fileItem['eof'] = eof


#  print to a file

def printFile(item):
  fileNum = item['fileNum']
  if fileNum not in data.fileList:
    item['error'] = 'File ' + str(fileNum) + ' not open'
    return

  fileItem = data.fileList[fileNum]
  fl = fileItem['fileHandle']
  parts = item['parts']
  buff = ''
  for expr in parts:
    if expr in [',', ':', ';']:
      buff = buff + ', '
    else:
      [value, msg] = expressions.evaluate(expr)
      if msg != 'OK':
        item['error'] = msg
        return
      if type(value) in [int, float, bool]:
        value = str(value)
      if type == str:
        value = helpers.addQuotes(value)
      buff = buff + value
  fl.write(buff + '\n')

#  close a file

def closeFile(item):
  fileNum = item['fileNum']
  if fileNum not in data.fileList:
    item['error'] = 'Bad file number'
    return
  fileItem = data.fileList[fileNum]
  fl = fileItem['fileHandle']
  fl.close()

  if item['delete'] == 'DELETE':
    os.remove(fileItem['fileName'])

  data.fileList.pop(fileNum)

#  at end of run, close remaining files

def closeAllFiles():
  for fileNum in data.fileList:
    fileItem = data.fileList[fileNum]
    fl = fileItem['fileHandle']
    fl.close()
  data.fileList = {}

#----------------------
#  helper functions for read and write

#  process input  from comma delimited string
#  note - if empty string, set variable to empty value

def processInputsFromString(variables, txt):
  if (len(variables) == 1) and (txt == ''):    
    values = ['""']
  else:  
    values = splitValues(txt)
  return processInputs(variables, values)

# extract data from comma delimited string

def splitValues(txt):
  values = []
  value = ''
  inQuotes = False

  for ch in txt:
    if ch == '"':
      inQuotes = not inQuotes

    if inQuotes:
      value = value + ch
    else:
      if ch == ',':
        if value != '':
          values.append(value)
        value = ''
      elif ch != ' ':
        value = value + ch

  if value != '':
    values.append(value)

  return values

#  save input values

def processInputs(variables, values):
  if len(variables) > len(values):
    return 'Bad values'

  i = 0
  while i < len(variables):
    var = variables[i]
    value = values[i]

    if helpers.isStringVariable(var):
      if value[0] != '"':
        value = helpers.addQuotes(value)
    else:
      if type(value) == str:
        if helpers.isnumeric(value):
          value = float(value)
        else:
          return 'Bad value - ' + value

      if type(value) == int:
        value = float(value)

    msg = helpers.setVariable(var, value)
    if msg != 'OK':
      return msg
    i = i + 1

  return 'OK'
