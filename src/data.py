#  TI 99/4A BASIC 
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
# data.py - global variables

#  codeList - dictionary containing the raw basic code indexed by line number
 
codeList = {}

#  variables - dictionary of variables and their current values

variables = {}

#  index - sorted array of line numbers used to access the basic code in line number order

index = []

#  parseList holds the parse tree
#  each item is indexed by line number 
#  and contains a dictionary containing the code, statement type and additional items depending on statement type

parseList = {}

#  gosubStack holds the line number for the return statement

gosubStack = []

#  forNextStack holds the information needed to execute the for/next loop
#  includes the variable name, limit and line number

forNextStack = []

#  print variables tracks the location of the cursor on the screen
#  printLocation is the current horizontal position of the cursor 
#  printWidth holds the maximum width of the screen

printPosition = 0
printWidth = 48

#  debugger data
#  breakpointList is an array containing the list of line numbers set by the break command 
# when true, traceFlag indicates that each line number will  be displayed on the screen
 
breakpointList = []
traceFlag = False

#  data fields
#  dataList contains the values from all of the data statements
#  dataPointer points to the next item to be read in the data list

dataList = []
dataPointer = 0

#  matrix fields
#  matrixList contains the array variable names as well as dimenstions for each variable 
#  matrixBase contains the lwer bound of each array (0 or 1), set by the option base command

matrixList = {}
matrixBase = 0

#  firstLine points to the first line number of the basic program

#  line number variables
firstLine = -1
#  maxLine is the largest line number allowed
#  address contains the current line number during program execution
#  quitFlag indicates that the python program should close

maxLine = 32767
address = -1
quitFlag = False

#  reservedWords list all reserved words - used to validate variable names

reservedWords = ['ABS', 'APPEND', 'ASC', 'ATN', 'BASE', 'BREAK', 'BYE', 
                 'CALL', 'CHR$', 'CLOSE', 'CON', 'CONTINUE', 'COS',
                 'DATA', 'DEF', 'DIM', 'DELETE', 'DISPLAY',
'EDIT', 'ELSE', 'END', 'EOF', 'EXP', 'FIXED', 'FOR',
'GO', 'GOSUB', 'GOTO', 'IF', 'INPUT', 'INT', 'INTERNAL',
'LEN', 'LET', 'LIST', 'LOG', 'NEW', 'NEXT', 'NUM', 'NUMBER',
'OLD', 'ON', 'OPEN', 'OPTION', 'OUTPUT', 'PERMANENT', 'POS', 'PRINT',
'RANDOMIZE', 'READ', 'REC', 'RELATIVE', 'REM', 'RES', 'RESEQUENCE', 'RESTORE', 'RETURN', 'RND', 'RUN',
'SAVE', 'SEG$', 'SEQUENTIAL', 'SGN', 'SIN', 'SQR', 'STEP', 'STOP', 'STR$', 'SUB',  
'TAB', 'TAN', 'THEN', 'TO', 'TRACE', 'UNBREAK', 'UNTRACE', 'UPDATE', 'VAL', 'VARIABLE']

#  functionNames contains the names of all built-in basic functions

functionNames = ['ABS', 'ATN', 'COS', 'EXP', 'INT', 'LOG', 'RND', 'SGN', 'SIN', 'SQR', 'TAN',
          'ASC', 'CHR$', 'LEN', 'POS', 'SEG$', 'STR$', 'TAB', 'VAL']

