#  parser - scan code for errors and build parseList data structure

import data

#  parse the code list and place in parseList

def parse():
  rslt = createIndex()
  if (rslt != 'OK'):
    return rslt
  rslt = buildParseList()
  return rslt
  

# create an ordered list of line number

def createIndex():
  data.index = []
  data.firstLine = -1  
  if (len(data.codeList) == 0):
    return 'No code'
    
  for lineNumber in data.codeList:
     data.index.append(lineNumber)
  data.index.sort()
  data.firstLine = data.index[0]  
  return 'OK'

#  build the basic parse list from the index

def buildParseList():
  data.parseList = {}
  lastLine = -1
  for lineNumber in data.index:
    item = {}
    code = data.codeList[lineNumber]
    parts = code.split()
    item['code'] = code
    item['statement'] = parts[1]
    item['nextLine'] = -1
    item['error'] = 'OK'
    data.parseList[lineNumber] = item
    
    if (lastLine > 0):
      data.parseList[lastLine]['nextLine'] = lineNumber  
    lastLine = lineNumber
  return 'OK'
  