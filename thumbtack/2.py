#! /usr/bin/env python
#
# Thumbtack Challenge #2
# Simple DB
#
# Implement DB with
# GET, SET, UNSET
# BEGIN, END, ROLLBACK, COMMIT
#
# Initial thoughts:
# - dict to store
# - use list to queue current dicts
# - COMMIT merges into BASE dict

import sys

dicts = []
cmds = ["end", "get", "set", "unset", "begin", "rollback", "commit"]

BASE = {}
CURR = BASE
dicts.append(BASE)

def process(words):
  if (words[0] == cmds[0]):
    # already handled
    print "I should not be in here"
    return
  elif (words[0] == cmds[1]):
  elif (words[0] == cmds[2]):
  elif (words[0] == cmds[3]):
  elif (words[0] == cmds[4]):
  elif (words[0] == cmds[5]):
  elif (words[0] == cmds[6]):
  else:
    # should not be able to get here
    print "I should not be in here (not a known command)"
    return


if __name__ == "__main__":
  line = ""
  while(1):
    line = raw_input("$")
    words = line.split()
    words[0] = words[0].lower()
    if (words[0] not in cmds):
      print "bad input, crashing hard"
      exit()
    elif (words[0] == "end"):
      exit()
    process(words)




  print "derp"
