#!/usr/bin/env python
##########################################
#  MindSnack Code Demo
#  www.mindsnack.com/challenges
#  problem #3, Fun Learning Factor
#  
#
#  by Jameson Lee
#  March-19 2012
#
#  Dependency:
#  python (2.6.6), >2.6, <3.0
#  munkres - (pip install munkres)
##########################################

import sys
from munkres import Munkres

#
# Find the Tutor-Player pair's base FLF
# 
def getBaseFLF(tutor, player):
  vowels = "aeiou"
  flf = 0
  for v in vowels:
    flf += player.count(v)
  if (len(tutor) % 2):
    return flf*1.5
  else:
    return (len(player)-flf)*1.0 #force float

#
# Find the modifier for a tutor-player pair
#  - since minimum match is 2 chars, do sliding window matching
#  - non-alphabets count as valid matches
#
def getModFLF(tutor, player):
  pos = 2
  while(len(tutor) < pos):
    if (tutor[pos-2:pos] in player):
      return 1.5
    else:
      pos+=1
  return 1.0


### Hungarian Style  body ###
#
# uses Hungarian (Kuhn) Algorithm to find best-pairing
# max-flow is found by doing max-local as weight
# the total FLF is found by doing max*len - total
#
# this version is actually really inefficient, both memeory and runtime
#
def main(tutors, players):
  scores = []
  #create cross-scores
  for tutor in tutors:
    # create the score array for each tutor to every player
    scores.append([ getModFLF(tutor, player)*getBaseFLF(tutor,player) for player in players ])
  # print the matrix
  #pretty_print(scores)

  # find max
  maxscore = max(max(row) for row in scores)
  # turn the matrix into a min-problem
  for row in scores:
    for idx,col in enumerate(row):
      row[idx] = maxscore-col
  # using munkres (copy of tutorial)
  m = Munkres()
  indexes = m.compute(scores)

#  pretty_print(scores)
  total = 0
  print "[[Tutor ::: Player]]"
  for row, col in indexes:
    total += scores[row][col]
    print '{0} ::: {1}'.format(tutors[row],players[col])
  print 'total FLF: {0}'.format(maxscore*len(tutors)-total)

def pretty_print(matrix):
  for r in matrix:
    print r

### input handling ###

if __name__ == "__main__":
  # allow one liner execution
  if (len(sys.argv) == 3):
    tFile = sys.argv[1]
    pFile = sys.argv[2]
  else:
    tFile = raw_input("Tutor name file: ")
    pFile = raw_input("Player name file: ")

  try:
    tNames = open(tFile)
    pNames = open(pFile)
  except(IOError):
    print "Was unable to open name files, check'em"
    exit()

  tutors = []
  players = []
  for name in tNames:
    tutors.append(name.strip())
  for name in pNames:
    players.append(name.strip())

  # main loop will actually dump to a file or print
  main(tutors, players)

# EOF
