#  language definition
#  program title and version

title = 'TI Extended Basic'
version = 'version 0.1.0'

#  line number values

defaultStart = 100
defaultStep = 10
maxLine = 32767

#  tokens

delimiters = [' ', ',', ';', ':', '"', '(', ')']
operators = ['+', '-', '*', '/', '^', '<>', '<=', '>=']

reservedWords = ['ABS', 'APPEND', 'ASC', 'ATN', 'BASE', 'BREAK', 'BYE',
                 'CALL', 'CHR$', 'CLOSE', 'CON', 'CONTINUE', 'COS',
                 'DATA', 'DEF', 'DIM', 'DELETE', 'DISPLAY',
'EDIT', 'ELSE', 'END', 'EOF', 'EXP', 'FIXED', 'FOR',
'GO', 'GOSUB', 'GOTO', 'IF', 'INPUT', 'INT', 'INTERNAL',
'LEN', 'LET', 'LIST', 'LOG', 'NEW', 'NEXT', 'NUM', 'NUMBER', 'MIN', 'MAX',
'OLD', 'ON', 'OPEN', 'OPTION', 'OUTPUT', 'PERMANENT', 'PI', 'POS',
'PRINT', 'RANDOMIZE', 'READ', 'REC', 'RELATIVE', 'REM',
'RES', 'RESEQUENCE', 'RESTORE', 'RETURN', 'RND', 'RUN',
'SAVE', 'SEG$', 'SEQUENTIAL', 'SGN', 'SIN', 'SQR',
'STEP', 'STOP', 'STR$', 'SUB', 'TAB', 'TAN', 'THEN',
'TO', 'TRACE', 'UNBREAK', 'UNTRACE', 'UPDATE', 'VAL', 'VARIABLE']

functionNames = ['ABS', 'ATN', 'COS', 'EOF', 'EXP',
          'INT', 'LOG', 'MAX', 'MIN','PI', 'RND', 'SGN', 'SIN', 'SQR', 'TAN',
          'ASC', 'CHR$', 'LEN', 'POS', 'RPT$', 'SEG$', 'STR$', 'TAB', 'VAL']

statements = {
  'BREAK': 'BREAK [ line ]',
  'CALL': 'CALL name ( args )',
  'CLEAR': 'CLEAR',
  'CONTINUE': 'CONTINUE',
  'DATA': 'DATA list',
  'DEF': 'DEF name ( arg ) = expr',
  'DELETE': 'DELETE file',
  'DIM': 'DIM var ( dims )',
  'END': 'END [ option ]',
  'EXIT': 'EXIT SUB',
  'FILES': 'FILES',
  'FOR': 'FOR var = expr1 TO expr2 [ STEP expr3 ]',
  'GOSUB': 'GOSUB line',
  'GOTO': 'GOTO line',
  'IF': 'IF expr THEN line1 [ ELSE line2 ]',
  'INPUT': 'INPUT list',
  'LET': 'LET var = expr',
  'LINPUT': 'LINPUT list',
  'LIST': 'LIST [ range ]',
  'MERGE': 'MERGE file',
  'NEW': 'NEW',
  'NEXT': 'NEXT [ var ]',
  'NUMBER': 'NUMBER [ sequence ]',
  'OLD': 'OLD file',
  'ON_GOSUB': 'ON expr GOSUB list',
  'ON_GOTO': 'ON expr GOTO list',
  'OPTION': 'OPTION BASE n',
  'PRINT': 'PRINT [ list ]',
  'QUIT': 'QUIT',
  'RANDOMIZE': 'RANDOMIZE',
  'READ': 'READ list',
  'REM': 'REM [ remark ]',
  'RESEQUENCE': 'RESEQUENCE [ sequence ]',
  'RESTORE': 'RESTORE',
  'RETURN': 'RETURN',
  'RUN': 'RUN [ option ]',
  'SAVE': 'SAVE file',
  'STOP': 'STOP [ option ]',
  'SUB': 'SUB name ( args )',
  'TRACE': 'TRACE',
  'UNBREAK': 'UNBREAK [ line ]',
  'UNTRACE': 'UNTRACE',
  'VERSION': 'VERSION'
}

#  command synonyms

synonyms = {
  'NUM': 'NUMBER',
  'RES': 'RESEQUENCE'
}
