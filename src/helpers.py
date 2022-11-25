#  helper functions created to reproduce functions missing from Circuit Python

#  is this string numeric

def isnumeric(str):
  i = 0
  while (i < len(str)):
    if (str[i] < '0' or str[i] > '9'):
      return False
    i = i + 1
  return True

# get file name from cammand line

def parseFileName(cmdWork):
  parts = cmdWork.split()
  if (len(parts) < 2):
    return ['', 'Missing file name']
    
  if (len(parts) > 2):
    return ['', 'Too many arguments']

  fileName = parts[1] + '.ti'
  return [fileName, 'OK']

