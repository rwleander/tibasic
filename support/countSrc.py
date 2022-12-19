# code line counter

import os


# count lines in file

def countLines(fname):
  n = 0
  with open (fname, 'r') as fl:
    while  (line := fl.readline()):      
      line = line.strip()
      if line != '' and line[0] != '#':
        n = n + 1
  
    fl.close()
  return n
 
  

#  main code

total = 0
dir = os.listdir('src')
for fname in dir:
  if fname.find('.py') > 0:
    n = countLines('src\\' + fname)
    total = total + n
    print (fname, str(n))
    
print('Total', str(total))

