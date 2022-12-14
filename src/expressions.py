# parse expressions

import data
import helpers

#  evaluate an expression

def evaluate (expr):
  [parts, msg] = splitLine(expr)
  if (msg != 'OK'):
    return [0, msg]
  
  [tree, msg] = buildTree(parts)
  if (msg != 'OK'):
    return [0, msg]
  
  [value, msg] = calculate(tree)
  if (msg != 'OK'):
    return [0, msg]
  
  return [value, 'OK']

  
# split the expression into its parts
  
def splitLine(expr):
  symbols = ['+', '-', '*', '/', '^', '(', ')', '&']
  parts = []
  item = ''
  inString = False
  
  for char in expr:
    if (inString):
      if (char == '"'):
        inString = False
        item = item + char
        parts.append(item)
        item = ''
      else:
        item = item + char
  
    elif (char == '"'):
      if (item != ''):
        parts.append (item)
      item = char
      inString = True
    
    elif char in symbols:
      if (item == ''):
        parts.append (char)
      else:
        parts.append(item)
        parts.append(char)
      item = ''
    
    elif (char == ' '):
      if (item != ''):
        parts.append(item)
        item = ''
      
    else:
      item = item + char  
  
  if (item != ''):
    parts.append(item)
    
  if (inString == True):
      return [parts, 'Missing quote']

  return [parts, 'OK']
  
  
  #  build the tree structure from the parts
  
def buildTree(parts):
  tree = {}
  tree['end'] = 0
  
  #  create furst branch
  
  branch = {}
  branch['parts'] = []
  branch['value'] = 0
  branch['id'] = 0
  branch['parent'] = -1
  
  #  add first branch to tree
  
  tree[0] = branch
 
 #  copy parts to branch 
 
  for item in parts:    
    if (item == '('):
      id = tree['end'] + 1
      tree['end'] = id 
      branch['parts'].append('~' + str(id))
      
      newBranch = {}
      newBranch['parts'] = []
      newBranch['value'] = 0
      newBranch['id'] = id
      newBranch['parent'] = branch['id']
      tree[id] = newBranch
      
      branch = newBranch
      
    elif (item == ')'):
      oldBranch = branch
      oldId = oldBranch['id']
      tree[oldId] = oldBranch
      branch = tree[oldBranch['parent']]
      
    else:
      branch['parts'].append (item)
  
  if (branch['id'] > 0):
    return [tree, 'Missing )']
  
  return [tree, 'OK']
  
  
#  calculae the value of the expression
  
def calculate(tree):  
  i = tree['end']
  while (i >= 0):
    branch = tree[i]
    parts = branch['parts']
    parts = setVariables(parts, tree)    
    
    parts = minusParts(parts)
    parts = raiseParts(parts)
    parts = divideParts(parts)
    parts = multiplyParts(parts)    
    parts = addParts(parts)
    parts = subtractParts(parts)
    parts = compareParts(parts)
    
    branch['value'] = parts[0]    
    tree[i] = branch
    i = i - 1
  
  rootBranch = tree[0]  
  value = rootBranch['value']
  return [value, 'OK']
    
#  substitute variables and convert numbers to floats

def setVariables(parts, tree):
  newParts = []
  for item in parts:
    if (item[0] == '~'):
      text = item[1: len(item)]
      index = int(text)
      branch = tree[index]
      newParts.append(branch['value'])
    
    elif item in data.variables:
      newParts.append(data.variables[item])
    
    elif (helpers.isnumeric(item) and item != '-'):
      newParts.append (float(item))
    
    elif helpers.isValidVariable(item):
      data.variables[item] = 0
      newParts.append (0) 
      
    else:
      newParts.append(item)
      
  return newParts

# switch numbers negative if preceded by -

def minusParts(parts):      
  if len(parts) < 2:    
    return parts
  
  i = len (parts) - 2  
  while i >= 0:    
    item = parts[i]
    nextItem = parts[i + 1]
    lastItem = 'xxx'
    if (i > 0):
      lastItem = parts[i - 1]
    
    if  (isinstance(lastItem, float) == False) and (isinstance(nextItem, float) == True):        
      parts[i] = 0 -nextItem 
      del(parts[i + 1])
    i = i - 1    
    
  return parts
           

# raise parts to power

def raiseParts(parts):    
  i = 1
  while (i > 0):
    i = findOperator(parts, '^')    
    if i > 0:
      parts[i] = parts[i - 1] ** parts[ i + 1]
      del parts[i + 1]
      del parts[i - 1]
            
  return parts
            
# do division

def divideParts(parts):    
  i = 1
  while (i > 0):
    i = findOperator(parts, '/')    
    if i > 0:
      parts[i] = parts[i - 1] / parts[ i + 1]
      del parts[i + 1]
      del parts[i - 1]
            
  return parts
 
  
# do multiplication

def multiplyParts(parts):    
  i = 1
  while (i > 0):
    i = findOperator(parts, '*')    
    if i > 0:
      parts[i] = parts[i - 1] * parts[ i + 1]
      del parts[i + 1]
      del parts[i - 1]
            
  return parts
  
#  do additions
  
def addParts(parts):
  i = 1
  while (i > 0):
    i = findOperator(parts, '+')    
    if i > 0:
      parts[i] = parts[i - 1] + parts[ i + 1]
      del parts[i + 1]
      del parts[i - 1]
            
  return parts

#  do subtraction
  
def subtractParts(parts):
  i = 1
  while (i > 0):
    i = findOperator(parts, '-')    
    if i > 0:
      parts[i] = parts[i - 1] - parts[ i + 1]
      del parts[i + 1]
      del parts[i - 1]
            
  return parts
  
  # comparisons
  
def compareParts(parts):
  i = 1
  while i < len(parts) - 1:
    item = parts[i]
    if item in ['=', '<', '>', '<=', '>=']:
      prevItem = parts[i - 1]
      if isinstance(prevItem, float):
        prevItem = str(prevItem)
        
        if item == '=':
          item = '=='
          
      nextItem = parts[i + 1]
      if isinstance(nextItem, float):
        nextItem = str(nextItem)
      
      parts[i] = eval (prevItem + ' ' + item + ' ' + nextItem)
      del parts[i + 1]
      del parts[i - 1]
            
  return parts
  
  
  #  helper to find operators
  
def findOperator(parts, op):
  try:
    i = parts.index(op)
  except:
    i = -1
  return i
    
  
  