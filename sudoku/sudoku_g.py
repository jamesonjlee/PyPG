#!/usr/bin/python
#
# Graphical Sudoku Game
# Requires:
# sudoku.py (bundled)
# inputbox.py (bundled)
# pygame package
#
# creates a simple 9x9 grid user can use the mouse to play sudoku on
# the solver in sudoku.py is used to generate and solver puzzles

import sudoku, inputbox, pygame 
from pygame.locals import *
import time 

COLOR = {
    'RED': (255,0,0),
    'GREEN': (0,255,0),
    'BLUE': (0,0,255),
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'ORANGE': (255,168,0),
    'DGREY' : (64,64,64),
    'GREY' : (128,128,128),
    'LGREY' : (192,192,192)
    }


####################### 'Display' of the Game ###############
class Board:
  """Game Board Class, the Sudoku Game Board"""
  def __init__(self):
    """hold the values for checking"""
    #each bit represents 1~9 being present in row/col
    self.rows = [ 0x1ff  for i in xrange(9)]
    self.cols = [ 0x1ff  for i in xrange(9)]
    self.tiles = [[0x1ff for i in xrange(3)] for j in xrange(3)]
    self.stat = [[ None for i in xrange(9)] for j in xrange(9)]

    #holds static/default tiles (immutables)
    self.stay = []

  def setStay(self,x,y,val):
    """Sets the immutable/stationary values on this board"""
    self.set(x,y,val)
    self.stay.append((x,y,val))

  def set(self,x,y,val):
    """set values if valid, return False if failed for some reason"""
    bit = self.__num2bit(val)

    #check if it was part of static
    for i in self.stay:
      if (i[0],i[1]) == (x,y):
        return False
    # check r,c,t
    if not (self.rows[x] & bit):
      return False
    if not (self.cols[y] & bit):
      return False
    if not (self.tiles[x/3][y/3] & bit):
      return False
    self.unset(x,y)

    self.stat[x][y] = val
    self.rows[x] &= ~bit
    self.cols[y] &= ~bit
    self.tiles[x/3][y/3] &= ~bit

    return True

  def unset(self,x,y):
    """Unset the value from the Board, return false for invalid unsets"""
    if self.stat[x][y] is None:
      return False
    bit = self.__num2bit(self.stat[x][y])

    #check if it was part of static
    for i in self.stay:
      if (i[0],i[1]) == (x,y):
        return False

    self.stat[x][y] = None
    self.rows[x] |= bit
    self.cols[y] |= bit
    self.tiles[x/3][y/3] |= bit

    return True

  def Save(self,fname, more=''):
    """Save the Current state of the game to a file"""
    f = file(fname,'w')
    for r in self.stat:
      for v in r:
        if v is None:
          f.write('.')
        else:
          f.write(str(v))
    f.write('\n')
    f.flush()
    #if there is additional stuff to write
    f.write(more)
    f.flush()
    f.close()

  def Load(self,line):
    """Load the current state of the game from file"""
    line =  line.rstrip() #remove whitespace
    if len(line) is not 81: 
      raise Exception("Bad file, not 81")
    for i in xrange(81):
      if line[i] in sudoku.digits:
        self.set(i/9,i%9,int(line[i]))

  def solved(self):
    """Returns true Iff the game is solved"""
    for r in self.rows: 
      if r is not 0: return False
    for c in self.cols: 
      if c is not 0: return False
    for a in self.tiles: 
      for t in a: 
        if t is not 0: return False
    return True
  def __num2bit(self,num):
    return 1 << num-1

######################## Utiliy ############################

#This actually just realigns the game board and the solver board
def setup (game, solver):
  values = solver.values
  for i in sudoku.squares:
    if len(values[i]) is 1:
      x,y = i[0],i[1]
      x = ord(x)-ord('A')
      y = int(y)-1
      val = values[i]
      game.setStay(x,y,int(val))

def writeHelp(screen):
  messages = [
      '                       Welcome to Sudoku',
      '           To play, left click on a cell and enter 1-9',
      '           The game wont let you enter duplicates',
      '                         Command Buttons',
      '         Press N - create a New Game',
      '         Press S - save current game to a file',
      '         Press L - load a saved game from file',
      '         Press R - reset the current game',
      '         Press G - give up, and we will solve',
      '         Press H or Right Click - see this menu',
      '         Press Q or ESC - quit',
      '                          Colors of Cells',
#      '        Grey   - given values (immutable)',
      '        Blue   - incomplete group',
#      '        Green  - indicate completed group',
      '        Orange - currently selected cell',
      ' ',
      '                  Press Enter to Start!',
      ]
  inputbox.display_box_big(screen,messages)

#Shortcut to Draw the current game state
def drawBoard(screen, game, Buttons, texts):
  for x in xrange(9):
    for y in xrange(9):
      b = Buttons[x][y]
      screen.fill(b[1],b[0])
      if game.stat[x][y] is not None:
        screen.blit(texts[game.stat[x][y]],b[0].move(10,10))
     #check if it was part of static, paint it special
      font = pygame.font.Font(None,50)
      for i in game.stay:
        if (i[0],i[1]) == (x,y):
          screen.blit(texts[i[2]+9],b[0].move(10,10))    


############################main #######################333
"""Begin Main"""
if __name__ == '__main__':
  pygame.init()
  screen = pygame.display.set_mode((455,455))
  pygame.display.set_caption('Sudoku 4 IBG')

  #get the background drawable (maybe just use screen?)
  background = pygame.Surface(screen.get_size()) 
  background = background.convert()
  background.fill(COLOR['WHITE'])
  background.fill(COLOR['BLACK'],Rect(5,5,445,445))
  #drawing tile differences
  background.fill(COLOR['WHITE'],Rect(150,0,155,455))
  background.fill(COLOR['WHITE'],Rect(0,150,455,155))
  #redraw center BG
  background.fill(COLOR['BLACK'],Rect(155,155,145,145))
 
  #setup the drawing area for buttons
  Buttons = [[[None, COLOR['BLUE']] for x in xrange(9)] for y in xrange(9)]
  spacing = 5
  for x in xrange(9):
    for y in xrange(9):
      Buttons[x][y][0] = Rect(5+y*50,5+x*50,45,45)
  #text for drawing 1~9
  texts = {}
  if pygame.font:
    font = pygame.font.Font(None,50)
    for i in xrange(1,10,1):
      texts[i] = font.render(str(i),False,COLOR['LGREY'])
      texts[i+9] = font.render(str(i),False,COLOR['DGREY'])
  else:
    pygame.quit()

  running = 1
  #start a new game
  Game = Board()
  Solver = sudoku.Game()
  Solver.New()
  #align the boards
  setup(Game, Solver)

  #show Help screen
  writeHelp(screen)
  
  x,y = -1, -1
  while running:
    #do something cute
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
     running = 0
    elif event.type == KEYDOWN:
      key = event.key
      if   key is K_n:
        Game = Board()
        Solver.New()
        setup(Game, Solver)
      elif key is K_l:
        fname = inputbox.ask(screen,"Load")
        if len(fname) > 0:
          f = file(fname,"r")
          line1 = f.readline()
          line2 = f.readline()
          f.close()
          try: 
            Game = Board()
            Solver.Load(line2)
            setup(Game, Solver)
            Game.Load(line1)
            inputbox.display_box(screen,"Loaded %s" % (fname))
          except: 
            inputbox.display_box(screen,"Failed to Load %s" % (fname))
      elif key is K_s:
        fname = inputbox.ask(screen,"Save")
        if len(fname) > 0:
          try:
            Game.Save(fname, Solver.Save(fname))
            inputbox.display_box(screen,"Saved to %s" % (fname))
          except:
            inputbox.display_box(screen,"Failed to Save to %s" %s (fname))
      elif key is K_q or key is K_ESCAPE:
        pygame.quit()
#        print "Good Bye"
        running = 0
        break
      elif key is K_r:
        Game = Board()
        Solver.Reset()
        setup(Game, Solver)
      elif key is K_g:
        Solver.Solve()
        Game = Board()
        setup(Game, Solver)
      elif key is K_h:
        writeHelp(screen)
      elif key in range(K_1,K_9+1):
        if not Game.set(x,y,key-48):
          inputbox.display_box(screen,"Duplicate Value!")
      elif key is K_BACKSPACE:
        if not Game.unset(x,y):
          inputbox.display_box(screen,"Can't Touch This")
#      elif key is K_RETURN:
      drawBoard(background,Game,Buttons,texts)
      screen.blit(background,(0,0))
      if Game.solved():
        inputbox.display_box(screen,"Game Soooooooooooolllvveeedd")

      pygame.display.flip()
    elif event.type is MOUSEBUTTONDOWN:
      if event.button is not 1:
        writeHelp(screen)
      else:
        #reset the last color
        if x is not -1:
          Buttons[x][y][1] = COLOR['BLUE']
        #get the new positions
        x = event.pos[1]/50
        y = event.pos[0]/50
        #apply selected color
        Buttons[x][y][1] = COLOR['ORANGE']
        drawBoard(background,Game,Buttons,texts)
        screen.blit(background,(0,0))
        pygame.display.flip()
      
    #
    #screen is updated

  #do cleanup here
