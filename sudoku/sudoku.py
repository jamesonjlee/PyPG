#!/usr/bin/python
#
# A single importable sudoku solver
# Save/Load to a File (as a String)
# Reset, Current vs Original
# Interface is not fully implemented
#
# The solver is a refactor version of Peter Norvig's Sudoku Solver
# you can get the original source and information about how it works
# http://norvig.com/sudoku.html
# The algorithm is Brute Force with Pruning, quiet fast even on the most
# difficult of boards
#
# Comment from Norvig are in ##
## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
#
#  Addtional comments can be found in norvig's source

import random

###########################Utility Functions#####################
def __cross(A,B):
  "Utility Function used to generate the board"
  return [a+b for a in A for b in B]
#Some Globals
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
#Every Single Square
squares = __cross(rows,cols)
#Values used to Generate and Track Numbers
#for testing of validity
unitlist = ([__cross(rows,c) for c in cols] +
           [__cross(r,cols) for r in rows] +
           [__cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)


#Game that defines this current sudoku board
class Game:
  """ Represent the Entire Sudoku Game Board, self-sufficient"""
  def __init__(self):
    " Initialization of the Game "
    self.values = {}
    self.__grid = ""
    self.__ready = False
  def Solved(self):
    "Returns true if and only if I am solved"
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    values = self.values
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)
  def __assign(self,values,s,d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(self.__eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False
  def __eliminate(self,values,s,d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
      return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
      return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
      d2 = values[s]
      if not all(self.__eliminate(values, s2, d2) for s2 in peers[s]):
        return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
      dplaces = [s for s in u if d in values[s]]
      if len(dplaces) == 0:
        return False ## Contradiction: no place for this value
      elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
        if not self.__assign(values, dplaces[0], d):
          return False
      return values
  def __some(self,seq):
    "Return some element of seq that is true."
    for e in seq:
      if e: return e
    return False
  def __solve(self,values):
    "Solve helper, (due to recursion)"
    if values is False:
      return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
      return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return self.__some(self.__solve(self.__assign(values.copy(), s, d)) for d in
        random.sample(values[s],len(values[s])))
  def Solve(self):
    "Using depth-first search and propagation, try all possible values."
    "Brute force solver"
    self.values = self.__solve(self.values)
    if not self.Solved():
      raise Exception("Unsolvable")
    return self.values
  def Load(self,grid):
    "load a valid grid from a saved file"
    self.__grid = grid
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    def _grid_values(grid):
      "Convert grid into a dict of {square: char} with '0' or '.' for empties."
      chars = [c for c in grid if c in digits or c in '0.']
      assert len(chars) == 81
      return dict(zip(squares,chars))
    for s,d in _grid_values(grid).items():
      if d in digits and not self.__assign(values, s, d):
        return False ## (Fail if we can't assign d to square s.)
    self.values = values
    return True
  def Save(self,fname):
    "Saves the current state into a file"
    values = self.values
    s = ''
    for r in rows:
      for c in cols:
        if(len(values[r+c]) == 1):
          s += values[r+c]
        else:
          s += '.'
    #return s
    return self.__grid
  def Dump(self):
    "Display these values as a 2-D grid."
    values = self.values
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print
  def New(self,N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    _t = list(squares)
    self.values = {}
    random.shuffle(_t)
    for s in _t:
        if not self.__assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            self.Load(''.join(values[s] if len(values[s])==1 else '.' for s in squares))
            return
    self.New(N) ## Give up and make a new puzzle
  def Reset(self):
    self.Load(self.__grid)

grid1  = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
  Sudoku = Game()
  Sudoku.Load(grid1)
  if Sudoku.Solve() is False:
    #complain
    raise Exception("unsolvable")
  Sudoku.New()
  if Sudoku.Solve() is False:
    raise Exception("unsolvable")

