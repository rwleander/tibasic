# main repl loop

import data
import monitor

#main loop

while (data.quitFlag == False):
  cmd = input('>')
  print (monitor.executeCommand(cmd))
      