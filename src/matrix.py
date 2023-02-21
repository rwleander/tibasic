#  TI 99/4A BASIC 
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
#  matrix.py - functions for matrix operations
#
#  Note:
#  data.matrixBase determines start of arrays
#  if 0, index goes from 0 to n - 1
#  if 1, index goes from 1 to n

import data
import helpers
import expressions

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
  
#  set a value inside the matrix variable
  
def setVariable(name, value):
  [var, exprX, exprY, exprZ, msg] = parseVariable(name)
  if msg != 'OK':
    return msg
    
  [x, msg] = expressions.evaluate(exprX)
  if msg != 'OK':
    return msg
    
  [y, msg] = expressions.evaluate(exprY)
  if msg != 'OK':
    return msg
    
  [z, msg] = expressions.evaluate(exprZ)
  if msg != 'OK':
    return msg

  x = int(x)
  y = int(y)
  z = int(z)    
  [i, msg] = calculateIndex(var, x, y, z)
  if msg != 'OK':
    return msg
    
  if helpers.isStringVariable(var):
    data.variables[var][i] = value
  else:
    data.variables[var][i] = float(value)
  
  return 'OK'

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

# evaluate matrix expression

def evaluate(parts):  
  var = parts[0]  
  if var not in data.matrixList:
    return [-1, 'Bad expression']
    
  x = 0
  y = 0
  z = 0
  
  if len(parts) > 1:
    x = int(parts[1])
  if len(parts) > 2:
    y = int(parts[2])
  
  if len(parts) > 3:
    z = int(parts[3])
  
  [i, msg] = calculateIndex(var, x, y, z)
  if msg != 'OK':
    return [-1, msg]
    
  value = data.variables[var][i]
  return [value, 'OK']
 
#  calculate index

def calculateIndex(name, x, y, z):  
  if name not in data.matrixList:
    return [-1, 'Unknown variable']
    
  matItem = data.matrixList[name]  
  i = x - data.matrixBase
  xMin =  data.matrixBase
  xMax = matItem['x'] - ( 1 - data.matrixBase)  
  yMin = 0
  yMax = 0
  zMin = 0
  zMax = 0
  
  if matItem['y'] > 0:
    i = i + matItem['y'] * (y - data.matrixBase)
    yMin = xMin
    yMax = matItem['y'] - (1 - data.matrixBase)
    
  if matItem['z'] > 0:
    i = i + matItem['z'] * (z - data.matrixBase)
    zMin = xMin
    zMax = matItem['z'] - (1 - data.matrixBase)

  if x < xMin or x > xMax:
    return [-1, 'Index out of bounds']
  
  if y < yMin or y > yMax:
    return [-1, 'Index out of bounds']
    
  if z < zMin or z > zMax:
    return [-1, 'Index out of bounds']
    
  return [i, 'OK']
    

