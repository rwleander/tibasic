#  helper functions created to reproduce functions missing from Circuit Python

import os
import data

#  upshift user inpuut
#  note leavel literals in lower case

def upshift(txt):
  newTxt = ''
  inQuotes = False
  for ch in txt:
    if ch == '"':
      inQuotes = not inQuotes
    if inQuotes:
      newTxt = newTxt + ch
    else:
      newTxt = newTxt + ch.upper()
  return newTxt  
    
    #  is this variable name a string
    
def isStringVariable(txt):
  if txt == '':
    return False
  else:
    return txt[len(txt) - 1] == '$'
      
#  is this string numeric

def isnumeric(str):
  for  ch in str:
    if ch not in "0123456789-.":      
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
    return ''
  
  newTxt = txt
  if newTxt[0] == '"':
    newTxt = newTxt[1: len(txt)]
    
  if newTxt[len(newTxt) - 1] == '"':
    newTxt = newTxt[0: len(newTxt) - 1]
      
  return newTxt
    
  

# is this a valid variable name

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

# cannot be more than 15 characters

  if len(txt) > 15:
    return False
  
  # first character must be a number
  
  if txt[0] not in letters:
    return False

  # scan remaining characters  up to last

  for ch in txt[1: len(txt) - 1]:
    if ch not in letters and ch not in numbers and ch not in characters:
      return false  
    
  # last character
  
  ch = txt[len(txt) - 1]
  if ch not in letters and ch not in numbers and ch not in characters and  ch != '$':
    return False
    
  # not a reserved word
    
  if txt  in data.reservedWords:
    return False
    
  return True
      
#  set variable value

def setVariable(name, value):

#  make sure variable name is valid

  if isValidVariable(name) == False:
    return 'Bad name'
    
# match type

  if isStringVariable(name):
    if type(value) != str:    
      return 'Bad type'  
  else:
    if type(value) == int:
      value = float(value)
    if type(value) != float:
      return 'Bad type'
    
  data.variables[name] = value
  return 'OK'
  

# get file name from command line

def parseFileName(cmdWork):
  parts = cmdWork.split()
  if len(parts) < 2:
    return ['', 'Missing file name']
    
  if len(parts) > 2:
    return ['', 'Too many arguments']

  fileName = parts[1] + '.ti'
  return [fileName, 'OK']


# does file exist

def fileExists(fileName):
  files = os.listdir()
  return fileName in files

