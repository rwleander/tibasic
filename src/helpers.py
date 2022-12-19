#  helper functions created to reproduce functions missing from Circuit Python

import os
import data

#  is this string numeric

def isnumeric(str):
  for  ch in str:
    if ch not in "0123456789-.":      
      return False
      
  return True

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

  lastChar = name[len(name) - 1]
  if type(value) == int or type(value) == float:
    if lastChar == '$':
      return 'Bad type'  
  else:
    if lastChar != '$':
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

