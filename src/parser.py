#  parser - scan code for errors and build parseList data structure

import data
import helpers

#  parse the code list and place in parseList

def parse():
  rslt = createIndex()
  if (rslt != 'OK'):
    return rslt
    
  rslt = buildParseList()
  if (rslt != 'OK'):
    return rslt
  
  rslt = parseStatements()
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
  
#  parse individual statements based on statement keyword
  
def parseStatements():
  for lineNumber in data.index:
    item = data.parseList[lineNumber]
    newItem = {}
    if (item['statement'] == 'LET'):
      newItem = parseLet(item)
     
    if (item['statement'] == 'IF'):
      newItem = parseIf(item)
       
    if (item['statement'] == 'PRINT'):
      newItem = parsePrint(item)
    if (len(newItem) == 0):
      item['error'] = 'Unknown command'
      newItem = item

    data.parseList[lineNumber] = newItem
  return 'OK'  

# parse the let statement

def parseLet(item):
  code = item['code']
  parts = code.split()
  if (len(parts) < 5):
    item['error'] = 'Missing arguments'
    return item  
    
  item['part1'] =  parts[2]
  i = code.find('=')
  if (i >  1):
    item['part2'] = code[i + 2: len(code)]
  else:
    item['error'] = 'Missing ='
  return item
    
    
    # parse if statement
    
def parseIf(item):
  code = item['code']
  parts = code.split()
  if (len(parts) < 4):
    item['error'] = 'Missing arguments'
    return item  
  
  i = code.find('IF')
  j = code.find('THEN')
  if (j < 1):
    item['error'] = 'Missing THEN'
    return item
  k = code.find('ELSE')
  item['part1'] = code [i + 3: j - 1]  
  if (item['part1'] == ''):
    item['error'] = 'Missing expression'  
    return item
  if (k > 1):
    part2 = code[j + 5: k -1]
    part3 = code[k + 5: len(code)]
  else:
    part2 = code[j + 5: len(code)]
    part3 = str(item['nextLine'])
  if ((helpers.isnumeric(part2) == False) or (helpers.isnumeric(part3) == False)):
    item['error'] =  'Bad line number' 
    return item
  if (int(part2) not in data.codeList) or (int(part3) not in data.codeList): 
    if (part3 != '-1'):
      item['error'] = 'Unknown line number'
      return item    
  item['part2'] = part2
  item['part3'] = part3    
  return item
      
  # parse print cstatement
    
def parsePrint(item):
  code = item['code']
  parts = code.split()
  if (len(parts) < 3):
    item['error'] = 'Missing arguments'
    return item  
  
  i = code.find('PRINT') 
  item['part1'] = code[ i + 6: len(code)]
  return item


    
    
  