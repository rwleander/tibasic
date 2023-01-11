#  functions for matrix operations

import data
import helpers

#  set option base

def setOption(value):  
  if value != 0 and value != 1:
    return 'Incorrect statement'
  
  if len(data.matrixList) > 0:
    return 'Option must be before dim'  
  
  data.matrixBase = value
  return 'OK'
  
  #  create a new variable 
  
def newVariable (name, x, y, z):
  if data.matrixBase == 0:
    x1 = x + 1
    y1 = y + 1
    z1 = z + 1
  else:
    x1 = x
    y1 = y
    z1 = z
    
    if y1 == 0:
      y1 = 1
    if z1 == 0:
      z1 = 1
        
  n = x1 * y1 * z1
  try:
    if helpers.isStringVariable(name):
      data.variables [name] = [''] * n
    else:
      data.variables[name] = [0] * n
  except MemoryError as err:
    data.variables[var] = 0
    return [-1, 'Out of memory']

  data.matrixList[name] = {'x': x, 'y': y, 'z': z}    
  return 'OK'
  
  #  set value inside matrixvariable
  
def setVariable(name, value):
  return 'Not ready'
    
  
#   parse matrix variable name into its parts
  
def parseVariable(name):
  i = name.find('(')
  if i < 1:
    return ['', 0, 0, 0, 'Bad name']
    
  j = name.find(')')
  if j < i:
    return ['', 0, 0, 0, 'Bad name']
    
  var = name[0: i].strip()
  list = name[i+1: j]
  x = ''
  y = ''
  z = ''

  parts = list.split(',')
  if len(parts) == 0:
    return ['', 0, 0, 0, 'Bad name']

  if len(parts) > 0:
    x = parts[0].strip()

  if len(parts) > 1:
    y = parts[1].strip()

  if len(parts) > 2:
    z = parts[2].strip()

  return [var, x, y, z, 'OK']


