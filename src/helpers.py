#  helper functions created to reproduce functions missing from Circuit Python

import os
import data

#  is this string numeric

def isnumeric(str):
  i = 0
  while (i < len(str)):
    if (str[i] < '0' or str[i] > '9'):
      if (str[i] != '-'):
        return False
    i = i + 1
  return True

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

# evaluate an expression

def evaluateExpression(expr):
  try:
    value = eval(expr, data.variables)
    return [value, 'OK']
  except:
    return [-1, 'Expression error']
    
    
  
