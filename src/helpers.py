#  helper functions created to reproduce functions missing from Circuit Python

import os
import data

#  is this string numeric

def isnumeric(str):
  i = 0
  while (i < len(str)):
    if str[i] < '0' or str[i] > '9':
      if str[i] != '-':
        return False
    i = i + 1
  return True

# is this a valid variable name

def isValidVariable(txt):
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  numbers = "0123456789"
  
  # if blank, quit
  
  if txt == '':
    return False
    
  # first character must be a number
  
  if txt[0] not in letters:
    return False

  # scan remaining characters  up to last

  for ch in txt[1: len(txt) - 1]:
    if ch not in letters and ch not in numbers:
      return false  
    
  # last character
  ch = txt[len(txt) - 1]
  if ch in letters or ch in numbers:
    return True
      
  if ch == '$':
    return True
  else:
    return False
      
# get file name from command line

def parseFileName(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 2):
    return ['', 'Missing file name']
    
  if (len(parts) > 2):
    return ['', 'Too many arguments']

  fileName = parts[1] + '.ti'
  return [fileName, 'OK']


# does file exist

def fileExists(fileName):
  files = os.listdir()
  return fileName in files

