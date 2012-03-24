#!/usr/bin/env python
#
# Thumbtack Challenge #2
# Simple DB
# Jameson Lee
#
# Implement DB with
# GET, SET, UNSET
# BEGIN, END, ROLLBACK, COMMIT
#
# Initial thoughts:
# - dict to store
# - use list to queue current dicts
# - COMMIT merges into base dict

cmds = ["end", "get", "set", "unset", "begin", "rollback", "commit"]
base = {}
curr = base
dicts = [base]

#
# flatten everything onto base
#
def flatten():
  global curr, dicts, base
  for d in dicts:
    if d is base: continue
    for key in d.iterkeys():
      base[key] = d[key]
  dicts = [base]
  curr = base

#one-line _get (see process)
def _get(key):
  global curr, dicts, base
  for i in xrange(len(dicts),0,-1):
    if dicts[i-1].has_key(key):
      return dicts[i-1][key]
  return "NULL"

# mm switches
def process(words):
  global curr, dicts, base
  if (words[0] == cmds[0]):
    # this is "end", should have been handled before
    print "I should not be in here"
    exit(-1)
  elif (words[0] == cmds[1] and len(words) is 2):
    print _get(words[1])
  elif (words[0] == cmds[2] and len(words) is 3):
    curr[words[1]] = words[2]
  elif (words[0] == cmds[3] and len(words) is 2):
    curr[words[1]] = "NULL"
  elif (words[0] == cmds[4] and len(words) is 1):
    curr = {}
    dicts.append(curr)
  elif (words[0] == cmds[5] and len(words) is 1):
    if curr is base:
      print "INVALID ROLLBACK"
    else:
      #del curr
      dicts.pop() #remove curr
      curr = dicts[len(dicts)-1] #rebind to last
  elif (words[0] == cmds[6] and len(words) is 1):
    flatten()
  else:
    # should not be able to get here
    print "Malformed Input, Try Again"
  #end processing this line
  return 0


if __name__ == "__main__":
  line = ""
  while(1):
    line = raw_input("")
    words = line.split()
    if (len(words) < 1): continue
    words[0] = words[0].lower() # for all versions of command
    if (words[0] not in cmds):
      print "Unknown Command, Try Again"
    elif (words[0] == "end"):
      exit()
    process(words)
