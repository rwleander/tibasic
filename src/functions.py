#  evaluate functions

import math
import random

import helpers

#  get function results

def evaluate(parts):
  if len(parts) == 0:
    return [0, 'Bad function']
    
  func = parts[0]
  
  # math functions
  
  if func == 'ABS':
    return doAbs(parts)

  if func == 'ATN':
    return doAtn(parts)
  
  if func == 'COS':
    return doCos(parts)
    
  if func == 'EXP':
    return doExp(parts)
    
  if func == 'INT':
    return doInt(parts)
    
  if func == 'LOG':
    return doLog(parts)
      
  if func == 'RND':
    return doRnd(parts)
        
  if func == 'SGN':
    return doSgn(parts)

  if func == 'SIN':
    return doSin(parts)
  
  if func == 'SQR':
    return doSqr(parts)

  if func == 'TAN':
    return doTan(parts)
    
  # string functions
  
  if func == 'ASC':
    return doAsc(parts)
  
  if func == 'CHR$':
    return doChr(parts)
    
  if func == 'LEN':
    return doLen(parts)
      
  if func == 'STR$':
    return doStr(parts)
    
  if func == 'VAL':
    return doVal(parts)
      
  return [0, 'Unknown function']


# ABS - absolute value

def doAbs(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]
  
  if n < 0:
    return [0 - n, 'OK']
  else:
    return [n, 'OK']

#  atn - return arc tangent

def doAtn(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    a = math.atan(n)
    return [a, 'OK']
  else:
    return [0, msg]

#  cosine

def doCos(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    c = math.cos(n)
    return [c, 'OK']
  else:
    return [0, msg]
    
    #  exponent function
    
def doExp(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    x = math.exp(n)
    return [x, 'OK']
  else:
    return [0, msg]
    
# int return integer value

def doInt(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    i = math.floor(n)
    return [i, 'OK']
  else:
    return [0, 'msg']

# log function

def doLog(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':  
    return [0, msg]
    
  if n > 0:
    l = math.log(n)
    return [l, 'OK']
  else:
    return [0, 'Bad value']

#  random number

def doRnd(parts):
  r = random.random()
  return [r, 'OK']

# sgn - return sign

def doSgn(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]
    
  if n == 0:
    return [0, 'OK']
  elif n < 0:
    return [-1, 'OK']
  else:
    return [1, 'OK']

#  sine function

def doSin(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    s = math.sin(n)
    return [s, 'OK']
  else:
    return [0, msg]
    
#  SQR - square root

def doSqr (parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]
    
  if n >= 0:
    sqr = n ** 0.5
    return [sqr, 'OK']
  else:
    return [0, 'Bad argument']
  
# tangent

def doTan (parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    t = math.tan(n)
    return [t, 'OK']
    
  else:
    return [0, msg]
  
# ascii function

def doAsc(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]  
  
  if len(strWork) < 3:
    return [0, 'Bad value']

  ascWork = ord(strWork[1])
  return [ascWork, 'OK']
      
      # convert number to ascii character
      
def doChr(parts):
  [value, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]
    
  chrWork = '"' + chr(int(value)) + '"'
  return [chrWork, 'OK']
  
#  get string length

def doLen(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]

  n = len(strWork) - 2
  if n < 0:
    return [0, 'OK']
  else:
    return [n, 'OK']
  
#  str$ - convert number to string

def doStr(parts):
  [value, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]
  
  #  note: if number ends with.0, remove and just show the integer value
  
  strWork = str(value)
  if strWork[len(strWork) - 2: len(strWork)] == '.0':
    strWork = strWork[0: len(strWork) - 2]
    
  strWork = '"' + strWork + '"'
  return [strWork, 'OK']

#  value function

def doVal(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]
  
  strWork = strWork[1: len(strWork) - 1] 
  if helpers.isnumeric(strWork) == False:
    return [0, 'Bad value']
  
  n = float(strWork)
  return [n, 'OK']
  
  
  #------------------
  #  helpers
  
def getNumber(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) == float or n < 0:
    return [n, 'OK']
  else:
    return [0, 'Bad argument']
  
  # get string
  
def getString(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
   
  strWork = parts[1]
  if type(strWork) != str:
    return [0, 'Bad argument']
    
  return [strWork, 'OK']
  
  