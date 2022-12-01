# global variables

codeList = {}
variables = {}
strings = {}

index = []
parserList = {}

address = -1
firstLine = -1
quitFlag = False


#  codeList contains each line of code in the form codeList[lineNumber] = full line of code

#  index contains list of line numbers in sequence#

#  parseList contains parsed code with parseList[line number] = parsed item{}
#  item can contain the following keys:
#    code - full line of code
#    statement: type  of statement (LET, PRINT, FOR...)
#    nextLine: next line number in sequence
#  error - error message or 'OK'
#

# 