#  evaluate functions

import math

#  get function results

def evaluate(parts):
  if len(parts) == 0:
    return [0, 'Bad function']
    
  func = parts[0]
  if func == 'ABS':
    return doAbs(parts)

  if func == 'ATN':
    return doAtn(parts)
  
  if func == 'COS':
    return doCos(parts)
    
  if func == 'INT':
    return doInt(parts)
    
  if func == 'SGN':
    return doSgn(parts)

  if func == 'SIN':
    return doSin(parts)
  
  if func == 'SQR':
    return doSqr(parts)

  if func == 'TAN':
    return doTan(parts)
  
  return [0, 'Unknown function']


# ABS - absolute value

def doAbs(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  if n < 0:
    return [0 - n, 'OK']
  else:
    return [n, 'OK']

#  atn - return arc tangent

def doAtn(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  a = math.atan(n)
  return [a, 'OK']

#  cosine

def doCos(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  c = math.cos(n)
  return [c, 'OK']

# int return integer value

def doInt(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  i = math.floor(n)
  return [i, 'OK']

# sgn - return sign

def doSgn(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  if n == 0:
    return [0, 'OK']
  elif n < 0:
    return [-1, 'OK']
  else:
    return [1, 'OK']

#  sine function

def doSin(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float:
    return [0, 'Bad argument']
  
  s = math.sin(n)
  return [s, 'OK']
  
    
#  SQR - square root

def doSqr (parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float or n < 0:
    return [0, 'Bad argument']
  
  sqr = n ** 0.5
  return [sqr, 'OK']
  
# tangent

def doTan (parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float or n < 0:
    return [0, 'Bad argument']
  
  t = math.tan(n)
  return [t, 'OK']
    
    
  