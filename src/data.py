# global variables

codeList = {}
variables = {}

index = []
parserList = {}

gosubStack = []
forNextStack = []

firstLine = -1
quitFlag = False


#  codeList contains each line of code in the form codeList[lineNumber] = full line of code

#  index contains list of line numbers in sequence#

#  parseList contains parsed code with parseList[line number] = parsed item{}
#  item can contain the following keys:
#    code - full line of code
#    statement: type  of statement (LET, PRINT, FOR...)
#  part1 - first part of statement
#  part2 - second part of statement
#  part3 - third part of statement
#    nextLine: next line number in sequence
#  error - error message or 'OK'
#

# 