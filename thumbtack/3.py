#!/usr/bin/env python
# 3.py
# Thumbtack Challenge #3
# Service Request matching
# Jameson Lee
#
# approach:
# create a service stack -> order by # of possible jobs
# create a requests array (each day holds a stack)
# assume every job has equal pay

from collections import deque
import sys
import readline


MAX_DAYS = 20

servicers = []
requests = deque()

def _reset():
  global servicers, requests, MAX_DAYS
  servicers = []
  requests = deque([[] for i in xrange(MAX_DAYS)])
  return True

def _match():
  global servicers, requests
  servicers.sort(key = len, reverse = True)
  #servicers.sort(lambda a,b: cmp(len(a), len(b)))
  print servicers
  print requests
  return 0

def _process(servicers, requests, query):
  _type = query[0].lower()
  #_name = query[1]
  if (_type == "service"):
    servicers.append(query[1:])
  elif (_type == "request"):
    _event, _job, _date = query[1:]
    if _date.isdigit():
      requests[int(_date)-1].append([_job, _event])
    else:
      _d = _date.split('-')
      for _date in xrange(int(_d[0]),int(_d[1])+1):
        requests[int(_date)-1].append([_job, _event])
  else:
    print "line is not [service] or [request], skipping"
  return True

if __name__ == "__main__":
  _reset() #initialize actually
  # allow fast run
  if len(sys.argv) > 1:
    lines = open(sys.argv[1])
  else:
    lines = False

  while (1):
    line = lines.readline() if lines else sys.stdin.readline()
    #line = line.lower().split() #caps shouldn't matter...
    line = line.split()
    if len(line) is 0:
      if (lline == line): exit(0)
      print _match()
      _reset()
    else:
      _process(servicers, requests, line)
    lline = line

