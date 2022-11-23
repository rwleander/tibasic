# main repl loop

import data
import commands

#main loop

while (data.quitFlag == False):
  cmd = input('>')
  msg = commands.executeCommand(cmd)
  if (msg != ''):
    print (msg)
      