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


MAX_DAYS = 20

servicers = []
requests = deque()
# servicers.sort(key = len)
servicers.sort(lambda a,b: cmp(len(a), len(b)))

def _reset():
  global servicers, requests, MAX_DAYS
  servicers = []
  requests = deque([[] for i in xrange(MAX_DAYS)])
  return True

def _match():
  global servicers, requests
  return 0

def _process(servicers, requests, query):
  return True

if __name__ == "__main__":
  _reset() #initialize actually
  # allow fast run
  if len(sys.argv) > 1:
    lines = open(sys.argv[1])
  else:
    lines = sys.stdin
  for line in lines:
    if len(line) is 0:
      print _match()
      _reset()
    else:
      this is old instand
      # old instance

