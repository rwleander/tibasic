#  shared data objects

#  registers

firstLine = -1
address = -1

#  basic code

codeList = {}

#  control flags

quitFlag = False

#  storage

stack = []
variables = {}
userFunctionList = {}
callList = {}

#  list from data statements

dataList = []
dataPointer = 0

#  matrix storage

matrixList = {}
matrixBase = 0

#  console print data

printArea = {}
printWidth = 56
printTab = 14

#  debug data

breakList = []
breakFlag = False
traceFlag = False
