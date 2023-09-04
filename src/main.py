#  main program loop

import commands
import language
import data


#  main control loop

print (language.title + ' ready')
commands.cmdNew({})
while data.quitFlag is False:
  cmd = input('>')
  msg = commands.executeCommand(cmd)
  if msg != '':
    print (msg)
