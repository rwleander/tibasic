#  functions.py - evaluate functions

import math
import random

import scanner
import data

#  call appropriate function based on first part of the expression

def evaluate(parts):

  functionList = {
    'ABS': doAbs,
    'ASC': doAsc,
    'ATN': doAtn,
    'CHR$': doChr,
    'COS': doCos,
    'EOF': doEof,
    'EXP': doExp,
    'INT': doInt,
    'LEN': doLen,
    'LOG': doLog,
    'MAX': doMax,
    'MIN': doMin,
    'PI': doPi,
    'POS': doPos,
    'RND': doRnd,
    'RPT$': doRpt,
    'SEG$': doSeg,
    'SGN': doSgn,
    'SIN': doSin,
    'SQR': doSqr,
    'STR$': doStr,
    'TAB': doTab,
    'TAN': doTan,
    'VAL': doVal
  }

  if len(parts) == 0:
    return [0, 'Bad function']

  func = parts[0]
  if func in functionList:
    return functionList[func](parts)

  return [0, 'Unknown function - ' + str(parts)]

# ABS - absolute value

def doAbs(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  if n < 0:
    return [0 - n, 'OK']

  return [n, 'OK']

#  atn - return arc tangent

def doAtn(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    a = math.atan(n)
    return [a, 'OK']

  return [0, msg]

#  cosine

def doCos(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    c = math.cos(n)
    return [c, 'OK']

  return [0, msg]

#  EOF function
#  not yet implemented

def doEof(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, 'Bad argument']
  if n not in data.fileList:
    return [0, 'Bad argument']
  fileItem = data.fileList[n]
  return [fileItem['eof'], 'OK']

#  exponent function

def doExp(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    x = math.exp(n)
    return [x, 'OK']

  return [0, msg]

# int return integer value

def doInt(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    i = math.floor(n)
    return [i, 'OK']

  return [0, 'msg']

# log function

def doLog(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  if n > 0:
    l = math.log(n)
    return [l, 'OK']

  return [0, 'Bad value']

#  random number

def doRnd(parts):
  r = random.random()
  return [r, 'OK']

# sgn - return sign (-1, 0 or +1)

def doSgn(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  if n == 0:
    return [0, 'OK']

  if n < 0:
    return [-1, 'OK']

  return [1, 'OK']

#  sine function

def doSin(parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    s = math.sin(n)
    return [s, 'OK']

  return [0, msg]

#  SQR - square root

def doSqr (parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  if n >= 0:
    sqr = n ** 0.5
    return [sqr, 'OK']

  return [0, 'Bad argument']

#  tab - return spaces

def doTab(parts):
  [n, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  txt = '"' + ' ' * int(n) + '"'
  return [txt, 'OK']





# tangent

def doTan (parts):
  [n, msg] = getNumber(parts)
  if msg == 'OK':
    t = math.tan(n)
    return [t, 'OK']

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

  chrWork = scanner.addQuotes(chr(int(value)))
  return [chrWork, 'OK']

#  get string length

def doLen(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]

  n = len(strWork) - 2
  if n < 0:
    return [0, 'OK']

  return [n, 'OK']

#  return max of two numbers

def doMax(parts):
  if len(parts) != 3:
    return [0, 'Bad arguments']

  if parts[1] < parts[2]:
    return [parts[2], 'OK']
  return [parts[1], 'OK']
#  return min of two numbers

def doMin(parts):
  if len(parts) != 3:
    return [0, 'Bad arguments']

  if parts[1] > parts[2]:
    return [parts[2], 'OK']
  return [parts[1], 'OK']

#  return pi

def doPi(parts):
  return [math.pi, 'OK']

  #  position function

def doPos(parts):
  [str1, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]

  if len(parts) < 3:
    return [0, 'Bad expression']

  str2 = parts[2]
  num = 1

  if len(parts) > 3:
    num = parts[3]
    if type(num) != float:
      return [0, 'Bad value']

  str1 = str1[0: len(str1) - 1]
  str2 = scanner.stripQuotes(str2)
  n = str1.find(str2, int(num))

  if n > 0:
    return [n, 'OK']
  return [0, 'OK']

#   repeat string

def doRpt(parts):
  if len(parts) < 3:
    return ['""', 'Bad arguments']
  oldString = str(parts[1])
  oldString = scanner.stripQuotes(oldString)

  if scanner.isnumeric(parts[2]) is False:
    return ['""', 'Bad arguments']
  n = int(parts[2])
  if n < 1:
    return ['""', 'Bad arguments']
  strWork = oldString
  for n in range(1, n):
    strWork = strWork + oldString
  return [scanner.addQuotes(strWork), 'OK']

  #  segment function

def doSeg(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]

  strWork = strWork[0: len(strWork) - 1]
  num1 = 1
  num2 = 1
  if len(parts) < 3:
    return [0, 'Bad expression']

  num1 = parts[2]
  if type(num1) != float:
    return [0, 'Bad expression']

  if len(parts) > 3:
    num2 = parts[3]
    if type(num2) != float:
      return [0, 'Bad expression']

  if num1 < 1 or num1 > len(strWork) or num2 < 1:
    return [0, 'Bad value']

  strNew = scanner.addQuotes(strWork[int(num1): int(num1 + num2)])
  return [strNew, 'OK']

#  str$ - convert number to string

def doStr(parts):
  [value, msg] = getNumber(parts)
  if msg != 'OK':
    return [0, msg]

  #  note: if number ends with.0, remove and just show the integer value

  strWork = str(value)
  if strWork[len(strWork) - 2: len(strWork)] == '.0':
    strWork = strWork[0: len(strWork) - 2]

  strWork = scanner.addQuotes(strWork)
  return [strWork, 'OK']

#  value function

def doVal(parts):
  [strWork, msg] = getString(parts)
  if msg != 'OK':
    return [0, msg]

  strWork = strWork[1: len(strWork) - 1]
  if scanner.isnumeric(strWork) is False:
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

  return [0, 'Bad argument']

  # get string

def getString(parts):
  if len(parts) < 2:
    return [0, 'Bad argument']

  strWork = parts[1]
  if type(strWork) != str:
    return [0, 'Bad argument']

  return [strWork, 'OK']
