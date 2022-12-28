# global variables

codeList = {}
variables = {}

index = []
parserList = {}

gosubStack = []
forNextStack = []

firstLine = -1
quitFlag = False

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

functionNames = ['ABS', 'ATN', 'COS', 'EXP', 'INT', 'LOG', 'RND', 'SGN', 'SIN', 'SQR', 'TAN',
          'ASC', 'CHR$', 'LEN', 'SEG$', 'STR$', 'VAL']


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