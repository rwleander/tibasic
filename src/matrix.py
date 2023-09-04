#  matrix.py - functions for matrix operations

import data
import expressions
import scanner


#  set option base

def setOption(value):
  if value not in [0, 1]:
    return 'Incorrect statement'

  if len(data.matrixList) > 0:
    return 'Option must be before dim'

  data.matrixBase = value
  return 'OK'

#  create a new variable

def newVariable (name, dimensions):
  if len(dimensions) not in range(1, 8):
    return 'Bad statement'

  n = 1
  for  dim in dimensions:
    n = n * dim

  try:
    if scanner.isStringVariable(name):
      data.variables [name] = [''] * n
    else:
      data.variables[name] = [0] * n
  except MemoryError:
    data.variables[name] = 0
    return 'Out of memory'

  data.matrixList[name] = {'dim': dimensions, 'len': n}
  return 'OK'

#  set a value into an array

def saveVariable(var, value):
  if len(var) < 4:
    return 'Bad variable'

  varName = var[0]
  tokens = var[2: len(var) -1]
  [subscripts, msg] = calcSubscripts(tokens)
  if msg != 'OK':
    return msg

  if varName not in data.matrixList:
    return 'Bad variable'
  matrixItem = data.matrixList[varName]
  i = calcIndex(matrixItem['dim'], subscripts)
  if i < 0:
    return 'Bad subscripts'
  data.variables[varName][i] = value
  return 'OK'

#  evaluate expression

def evaluate(parts):
  if len(parts) < 2:
    return [-1, 'Bad expression']

  var = parts[0]
  subscripts = parts[1: len(parts)]
  if var not in data.matrixList:
    return [-1, 'Bad expression']

  matrixItem = data.matrixList[var]
  i = calcIndex(matrixItem['dim'], subscripts)
  n = data.variables[var][i]
  return [n, 'OK']

#  calculate index

def calcIndex(dimensions, subscripts):
  if len(dimensions) != len(subscripts):
    return -1

  n = 0
  for i in range(0, len(dimensions)):
    v = int(subscripts[i] - data.matrixBase)
    if v >= dimensions[i]:
      return -1
    n = n * dimensions[i] + v

  return int (n)

#  evaluate subscripts and return in values

def calcSubscripts(tokens):
  values = []
  expr = []
  error = 'OK'
  for token in tokens:
    if token == ',':
      [v, msg] = expressions.evaluate(expr)
      if msg != 'OK':
        error = msg
      values.append(v)
      expr = []
    else:
      expr.append(token)

  if len(expr) > 0:
    [v, msg] = expressions.evaluate(expr)
    if msg != 'OK':
      error = msg
    values.append(v)

  return [values, error]
