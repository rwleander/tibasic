# parse expressions

import data
import helpers

#  evaluate an expression

def evaluate (expr):
  value = -1
  try:
    value = float(expr)    
  except:
    value = expr
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
    
  return [tree, 'OK']
  
  