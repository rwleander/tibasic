# parse expressions

import data
import helpers
import functions

#  evaluate an expression

def evaluate (expr):
  [parts, msg] = splitLine(expr)
  if msg != 'OK':
    return [0, msg]
  
  [tree, msg] = buildTree(parts)
  if msg != 'OK':
    return [0, msg]
  
  [value, msg] = calculate(tree)
  if msg != 'OK':
    return [0, msg]
  
  return [value, 'OK']

  
# split the expression into its parts
  
def splitLine(expr):
  symbols = ['+', '-', '*', '/', '^', '(', ')', '&', ',']
  parts = []
  item = ''
  inString = False
  
  for char in expr:
    if inString:
      if char == '"':
        inString = False
        item = item + char
        parts.append(item)
        item = ''
      else:
        item = item + char
  
    elif char == '"':
      if item != '':
        parts.append (item)
      item = char
      inString = True
    
    elif char in symbols:
      if item == '':
        parts.append (char)
      else:
        parts.append(item)
        parts.append(char)
      item = ''
    
    elif char == ' ':
      if item != '':
        parts.append(item)
        item = ''
      
    else:
      item = item + char  
  
  if item != '':
    parts.append(item)
    
  if inString == True:
      return [parts, 'Missing quote']

  return [parts, 'OK']
  
  
  #  build the tree structure from the parts
  
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
    if item in data.functionNames:
      id = tree['end'] + 1
      tree['end'] = id 
      branch['parts'].append('~' + str(id))
      
      newBranch = {}
      newBranch['type'] = 'func'
      newBranch['parts'] = [item]
      newBranch['value'] = 0
      newBranch['id'] = id
      newBranch['parent'] = branch['id']
      tree[id] = newBranch
      branch = newBranch
                
    elif item == '(':
      id = tree['end'] + 1
      tree['end'] = id 
      branch['parts'].append('~' + str(id))
      
      newBranch = {}
      newBranch['type'] = 'expr'
      newBranch['parts'] = []
      newBranch['value'] = 0
      newBranch['id'] = id
      newBranch['parent'] = branch['id']
      tree[id] = newBranch
      
      branch = newBranch
      
    elif item == ',':
      oldBranchId = branch['parent']
      branch = tree[oldBranchId]
      
      id = tree['end'] + 1
      tree['end'] = id 
      branch['parts'].append('~' + str(id))
      
      newBranch = {}
      newBranch['type'] = 'expr'
      newBranch['parts'] = []
      newBranch['value'] = 0
      newBranch['id'] = id
      newBranch['parent'] = branch['id']
      tree[id] = newBranch
      
      branch = newBranch
      
    elif item == ')':      
      oldBranch = branch
      oldId = oldBranch['id']
      tree[oldId] = oldBranch
      branch = tree[oldBranch['parent']]
      
      #  note: if this is a function call, pop the stach twice
      
      if branch['type'] == 'func':
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
  
def calculate(tree):  
  i = tree['end']
  while i >= 0:
    branch = tree[i]
    parts = branch['parts']
    parts = setVariables(parts, tree)           
   
    if  branch['type'] == 'expr':      
      try:
        parts = minusParts(parts)
        parts = calcParts(parts, '^')
        parts = calcParts(parts, '/')
        parts = calcParts(parts, '*')    
        parts = calcParts(parts, '+')
        parts = calcParts(parts, '-')
        parts = joinStrings(parts)        
        parts = compareParts(parts)
      except:
        return [0, 'Bad expression']
       
      if len(parts) > 1:
        return [0, 'Bad expression']
        
      if len(parts) == 0:
        branch['value'] = 0
      else:
        branch['value'] = parts[0]        
    
    else:
      [value, msg] = functions.evaluate(parts)
      if (msg != 'OK'):
        return [0, msg]           
      branch['value'] = value    
  
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
    
    elif item in data.variables:
      newParts.append(data.variables[item])
    
    elif helpers.isnumeric(item) and item != '-':
      newParts.append (float(item))
    
    elif item[0] == '"':
      newParts.append(item)
    
    elif helpers.isValidVariable(item):      
      if item[len(item) - 1] == '$':
        data.variables[item] = ""        
        newParts.append("")
      else:
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
    if parts[i] == '-':
      item = parts[i]
      nextItem = parts[i + 1]
      lastItem = 'xxx'
      if i > 0:
        lastItem = parts[i - 1]
    
      if  (isinstance(lastItem, float) == False) and (isinstance(nextItem, float) == True):        
        parts[i] = 0 -nextItem 
        del(parts[i + 1])
    i = i - 1    
    
  return parts

# calculate parts

def calcParts(parts, op):            
  if len(parts) < 3:
    return parts
    
  i = 1
  while i > 0:
    i = findOperator(parts, op)    
    if (i == 0) or (i == len(parts) - 1):
      raise Exception
      
    if i > 0:
      lastItem = parts[i - 1]
      item = parts[i]
      nextItem = parts[i + 1]
      
      if (isinstance(lastItem, float) == False) or (isinstance(nextItem, float) == False):
        raise Exception
        
      newItem = 0
      if op == '^':
        newItem = lastItem ** nextItem
        
      if op == '/':
        if nextItem == 0.0:
          raise Exception
        newItem = lastItem / nextItem        
        
      if op == '*':
        newItem = lastItem * nextItem
  
      if op == '+':
        newItem = lastItem + nextItem
  
      if op == '-':
        newItem = lastItem - nextItem
    
      parts[i - 1] = newItem
      del parts[i + 1]
      del parts[i]
            
  return parts

# join strings

def joinStrings(parts):            
  if len(parts) < 3:
    return parts
    
  i = 1
  while i > 0:
    i = findOperator(parts, '&')    
    if (i == 0) or (i == len(parts) - 1):
      raise Exception
      
    if i > 0:
      lastItem = parts[i - 1]
      item = parts[i]
      nextItem = parts[i + 1]
      
      if type(lastItem) != str or type(nextItem) != str:
        raise Exception
      
      newItem = lastItem[0: len(lastItem) - 1] + nextItem[1: len(nextItem)]        
      parts[i - 1] = newItem
      del parts[i + 1]
      del parts[i]
            
  return parts
  
  # comparisons
  
def compareParts(parts):
  if len(parts) < 3:
    return parts
    
  i = 1
  while i < len(parts) - 1:
    item = parts[i]
    if item in ['=', '<', '>', '<=', '>=', '<>']:
      prevItem = parts[i - 1]
      nextItem = parts[i + 1] 
      
      if type(prevItem) != type(nextItem):
        raise Exception
        
      value = False
      if item == '=':
        value = (prevItem == nextItem)
          
      if item == '<':
        value = (prevItem < nextItem)
            
      if item == '<=':
        value = (prevItem <= nextItem)
        
      if item == '>':
        value = (prevItem > nextItem)
        
      if item == '>=':
        value = (prevItem >= nextItem)
        
      if value == '<>':
        value = (prevItem != nextItem)  
  
      parts[i - 1] = value
      del parts[i + 1]
      del parts[i]
            
  return parts
  
  
  #  helper to find operators
  
def findOperator(parts, op):
  try:
    i = parts.index(op)
  except:
    i = -1
  return i
    
  
  