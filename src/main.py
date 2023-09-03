#  TI 99/4A BASIC
#  By Rick Leander
#  Copyright (c) 2023 by Rick Leander - all rights reserved
#
# main.py -main program
#

import data
import commands

#  main control loop

print (data.title + ' ready')
while data.quitFlag is False:
  cmd = input('>')
  msg = commands.executeCommand(cmd)
  if msg != '':
    print (msg)
