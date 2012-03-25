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
#
# comment on solution:
# may not produce the optimal matching, just a possible matching
# servicers are sorted by # of jobs they can perform
# requests could be sorted by servicer rarity

import sys
import readline


MAX_DAYS = 20

servicers = []
requests = []

def _reset():
  global servicers, requests, MAX_DAYS
  servicers = []
  requests = [[] for i in xrange(MAX_DAYS+1)]
  return True

def _match():
  global servicers, requests
  count = 0
  servicers.sort(key=len)
  #servicers.sort(key = lambda a: len(a))
  for day, jobs in enumerate(requests):
    #print day, jobs
    #process the day, a new set of workers everyday
    workers = list(servicers)
    for job in jobs:
      _j, _d = job[0], job[2]
      for worker in workers:
        if _j in worker:
          workers.remove(worker)
          _d = day
          count += 1
          break
      if _d > day:
        jobs.remove(job)
        requests[day+1].append(job)
  return count

#
# servicer: [name, service, service...]
# request: [service, name, end-date]
#  - 'end-date' used to remove from working queue
#
def _process(servicers, requests, query):
  _type = query[0].lower()
  #_name = query[1]
  if (_type == "service"):
    servicers.append(query[1:])
  elif (_type == "request"):
    _event, _job, _date = query[1:]
    if _date.isdigit():
      requests[int(_date)].append([_job, _event, int(_date)])
    else:
      _d = _date.split('-')
      requests[int(_d[0])].append([_job, _event, int(_d[1])])
  else:
    print "line is not [service] or [request], skipping"
    return False
  return True

if __name__ == "__main__":
  _reset() #initialize actually
  # allow fast run
  if len(sys.argv) > 1:
    lines = open(sys.argv[1])
  else:
    lines = False

  lline = ''
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

