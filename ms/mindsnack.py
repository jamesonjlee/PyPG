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
#  python 2.6.6
##########################################

import sys

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


### main body ###
def main():



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

  #
