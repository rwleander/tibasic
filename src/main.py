# main repl loop

import data
import commands

#main loop

print ('TI BASIC READY')
while data.quitFlag == False:
  cmd = input('>')
  msg = commands.executeCommand(cmd)
  if msg != '':
    print (msg)
      