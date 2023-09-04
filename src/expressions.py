# expressions.py - parse and evaluate an expressions

import data
import language
import functions
import matrix
import scanner


#  parse  an expression and return the result

def evaluate (tokens):
  [tree, msg] = buildTree(tokens)
  if msg != 'OK':
    return [0, msg]

  [value, msg] = calculate(tree)
  if msg != 'OK':
    return [0, msg]

  return [value, 'OK']

#  build the tree structure from the parts
#  note: needs refactoring

def buildTree(parts):
  tree = {}
  tree['end'] = 0

  #  create furst branch

  branch = {}
  branch['type'] = 'expr'
  branch['parts'] = []
  branch['value'] = 0
  branch['id'] = 0
  branch['parent'] = -1

  #  add first branch to tree

  tree[0] = branch

 #  copy parts to branch

  for item in parts:
    if item in language.functionNames or item in data.userFunctionList:
      idNum = tree['end'] + 1
      tree['end'] = idNum
      branch['parts'].append('~' + str(idNum))

      newBranch = {}
      newBranch['type'] = 'func'
      if item in data.userFunctionList:
        newBranch['type'] = 'udf'
      newBranch['parts'] = [item]
      newBranch['value'] = 0
      newBranch['id'] = idNum
      newBranch['parent'] = branch['id']
      tree[idNum] = newBranch
      branch = newBranch

    elif item in data.matrixList:
      idNum = tree['end'] + 1
      tree['end'] = idNum
      branch['parts'].append('~' + str(idNum))

      newBranch = {}
      newBranch['type'] = 'mat'
      newBranch['parts'] = [item]
      newBranch['value'] = 0
      newBranch['id'] = idNum
      newBranch['parent'] = branch['id']
      tree[idNum] = newBranch
      branch = newBranch

    elif item == '(':
      idNum = tree['end'] + 1
      tree['end'] = idNum
      branch['parts'].append('~' + str(idNum))

      newBranch = {}
      newBranch['type'] = 'expr'
      newBranch['parts'] = []
      newBranch['value'] = 0
      newBranch['id'] = idNum
      newBranch['parent'] = branch['id']
      tree[idNum] = newBranch

      branch = newBranch

    elif item == ',':
      oldBranchId = branch['parent']
      branch = tree[oldBranchId]

      idNum = tree['end'] + 1
      tree['end'] = idNum
      branch['parts'].append('~' + str(idNum))

      newBranch = {}
      newBranch['type'] = 'expr'
      newBranch['parts'] = []
      newBranch['value'] = 0
      newBranch['id'] = idNum
      newBranch['parent'] = branch['id']
      tree[idNum] = newBranch

      branch = newBranch

    elif item == ')':
      oldBranch = branch
      oldId = oldBranch['id']
      tree[oldId] = oldBranch
      parentId = oldBranch['parent']
      if parentId == -1:
        return [tree, 'Bad expression']
      branch = tree[parentId]

      #  note: if this is a function call or matrix item, pop the stack twice

      if branch['type'] in ['func', 'udf', 'mat']:
        oldBranch = branch
        oldId = oldBranch['id']
        tree[oldId] = oldBranch
        branch = tree[oldBranch['parent']]

    else:
      branch['parts'].append (item)

  if branch['id'] > 0:
    return [tree, 'Missing )']

  return [tree, 'OK']


#  calculate the value of the expression
#  by calculating the result of each tree node

def calculate(tree):

  functionList = {
    'expr': calculateExpression,
    'func': calculateFunction,
    'udf': calculateUserFunction,
    'mat': calculateMatrix
  }

  i = tree['end']
  while i >= 0:
    branch = tree[i]
    parts = branch['parts']

    parts = setVariables(parts, tree)

    branch['parts'] = parts

    branchType = branch['type']
    [branch, msg] = functionList[branchType](branch)
    if msg != 'OK':
      return [0, msg]

    tree[i] = branch
    i = i - 1

  rootBranch = tree[0]
  value =rootBranch['value']
  return [value, 'OK']

#  substitute variables and convert numbers to floats

def setVariables(parts, tree):
  newParts = []
  for item in parts:
    if item[0] == '~':
      text = item[1: len(item)]
      index = int(text)
      branch = tree[index]
      newParts.append(branch['value'])

    elif item in data.matrixList or item in language.functionNames:
      newParts.append (item)

    elif item in data.variables:
      newParts.append(data.variables[item])

    elif item in data.userFunctionList:
      newParts.append(item)

    elif scanner.isnumeric(item) and item != '-':
      newParts.append (float(item))

    elif item[0] == '"':
      newParts.append(item)

    elif scanner.isValidVariable(item):
      if item[len(item) - 1] == '$':
        data.variables[item] = ""
        newParts.append("")
      else:
        data.variables[item] = 0
        newParts.append (0)

    else:

      newParts.append(item)

  return newParts

#  reduce partial expressions from each tree node

def calculateExpression(branch):
  parts = branch['parts']

  #  reduce parts

  [parts, msg] = minusParts(parts)
  if msg != 'OK':
    return [branch, msg]

  for operation in ['^', '/', '*', '+', '-']:
    [parts, msg] = calcParts(parts, operation)
    if msg != 'OK':
      return [branch, msg]

  [parts, msg] = joinStrings(parts)
  if msg != 'OK':
    return [branch, msg]

  [parts, msg] = compareParts(parts)
  if msg != 'OK':
    return [branch, msg]

# see what we got

  if len(parts) > 1:
    return [branch, 'Bad expression']

  if len(parts) == 0:
    branch['value'] = 0
  else:
    branch['value'] = parts[0]

  return [branch, 'OK']


#  reduce function parts

def calculateFunction(branch):
  parts = branch['parts']
  [value, msg] = functions.evaluate(parts)
  if msg != 'OK':
    return [branch, msg]

  if type(value) == int:
    value = float(value)

  branch['value'] = value
  return [branch, 'OK']

#  evaluate user defined function

def calculateUserFunction(branch):
  parts = branch['parts']
  if len(parts) < 2:
    return [branch, 'Bad statement']
  functionName = parts[0]
  argValue = parts[1]
  if functionName not in data.userFunctionList:
    return [branch, 'Bad user function: ' + functionName]
  functionData = data.userFunctionList[functionName]
  argName = functionData['arg']
  expr = functionData['expr']
  for i  in range (0, len(expr)):
    if expr[i] == argName:
      expr[i] = str(argValue)

  [value, msg] = evaluate(expr)
  if msg != 'OK':
    return [branch, msg]
  branch['value'] = value
  return [branch, 'OK']

#  reduce matrix parts

def calculateMatrix(branch):
  parts = branch['parts']
  [value, msg] = matrix.evaluate(parts)
  if msg != 'OK':
    return [branch, msg]

  if type(value) == int:
    value = float(value)

  branch['value'] = value
  return [branch, 'OK']

# switch numbers negative if preceded by -

def minusParts(parts):
  if len(parts) < 2:
    return [parts, 'OK']

  i = len (parts) - 2
  while i >= 0:
    if parts[i] == '-':
      nextItem = parts[i + 1]
      lastItem = 'xxx'
      if i > 0:
        lastItem = parts[i - 1]

      if  type(lastItem) != float  and type(nextItem) == float:
        parts[i] = 0 -nextItem
        del parts[i + 1]
    i = i - 1

  return [parts, 'OK']

# reduce expression pairs
#  note: may want to refactor for readability

def calcParts(parts, op):
  if len(parts) < 3:
    return [parts, 'OK']

  i = 1
  while i > 0:
    i = findOperator(parts, op)
    if i in [0, len(parts) - 1]:
      return [parts, 'Bad expression']

    if i > 0:
      lastItem = parts[i - 1]
      nextItem = parts[i + 1]

      if lastItem in language.operators or nextItem in language.operators:
        return [parts, 'Bad expression']

      newItem = 0
      if op == '^':
        newItem = lastItem ** nextItem

      if op == '/':
        if nextItem == 0.0:
          return [parts, 'Bad expression - divide by zero']
        newItem = lastItem / nextItem

      if op == '*':
        if type(lastItem) == bool and type(nextItem) == bool:
          newItem = lastItem and nextItem
        else:
          newItem = lastItem * nextItem

      if op == '+':
        if type(lastItem) == bool and type (nextItem) == bool:
          newItem = lastItem or nextItem
        else:
          newItem = lastItem + nextItem

      if op == '-':
        newItem = lastItem - nextItem

      parts[i - 1] = newItem
      del parts[i + 1]
      del parts[i]

  return [parts, 'OK']

# join strings

def joinStrings(parts):
  if len(parts) < 3:
    return [parts, 'OK']

  i = 1
  while i > 0:
    i = findOperator(parts, '&')
    if i in [0, len(parts) - 1]:
      return [parts, 'Bad expression']

    if i > 0:
      lastItem = parts[i - 1]
      nextItem = parts[i + 1]

      if type(lastItem) != str or type(nextItem) != str:
        return [parts, 'Bad expression']

      newItem = lastItem[0: len(lastItem) - 1] + nextItem[1: len(nextItem)]
      parts[i - 1] = newItem
      del parts[i + 1]
      del parts[i]

  return [parts, 'OK']

  # comparisons
  #  may want to refactor

def compareParts(parts):
  if len(parts) < 3:
    return [parts, 'OK']

  i = 1
  while i < len(parts) - 1:
    item = parts[i]
    if item in ['=', '<', '>', '<=', '>=', '<>']:
      prevItem = parts[i - 1]
      nextItem = parts[i + 1]

      if type(prevItem) == int:
        prevItem = float(prevItem)

      if type (prevItem) == str:
        prevItem = scanner.stripQuotes(prevItem)

      if type(nextItem) == int:
        nextItem = float(nextItem)

      if type (nextItem) == str:
        nextItem = scanner.stripQuotes(nextItem)

      if type(prevItem) != type(nextItem):
        return [parts, 'Bad expression']

      value = False
      if item == '=':
        value = prevItem == nextItem

      if item == '<':
        value = prevItem < nextItem

      if item == '<=':
        value = prevItem <= nextItem

      if item == '>':
        value = prevItem > nextItem

      if item == '>=':
        value = prevItem >= nextItem

      if item == '<>':
        value = prevItem != nextItem

      parts[i - 1] = value
      del parts[i + 1]
      del parts[i]

    i =   i + 1

  return [parts, 'OK']


#  helper to find operators

def findOperator(parts, op):
  try:
    i = parts.index(op)
  except:
    i = -1
  return i
