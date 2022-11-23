#  helper functions created to reproduce functions missing from Circuit Python

#  is this string numeric

def isnumeric(str):
  i = 0
  while (i < len(str)):
    if (str[i] < '0' or str[i] > '9'):
      return False
    i = i + 1
  return True

