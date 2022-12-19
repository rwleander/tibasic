# code line counter for tests

import os


# count lines in file

def countLines(fname):
  t=  0
  n = 0
  with open (fname, 'r') as fl:
    while  (line := fl.readline()):      
      line = line.strip()
      if line != '' and line[0] != '#':
        n = n + 1
        if line.find('def ') == 0:
          t = t + 1
  
    fl.close()
  return [n, t]
 
  

#  main code

tests = 0
total = 0
dir = os.listdir('tests')
for fname in dir:
  if fname.find('.py') > 0:
    [n, t] = countLines('tests\\' + fname)
    total = total + n
    tests = tests + t
    print (fname, str(t), str(n))
    
print('Total', str(tests), str(total))

