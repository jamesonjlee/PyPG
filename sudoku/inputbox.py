# inputbox.py originally by Timothy Downs
# Original at:
# www.pygame.org/pcr/inputbox/inputbox.py
#
# modified to allow full screen writing (display_box_big)
# redraws when backspacing
# handles shifts
# only accepts regular alpha numberics
#
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      key = event.key
      if key >= ord('a') and key <= ord('z') and event.mod & (KMOD_LSHIFT | KMOD_RSHIFT | KMOD_SHIFT | KMOD_CAPS):
        return key - 32
      return key
    else:
      pass

def display_box_big(screen, messages):
  "display a large box with a line per item in message"
  fontobject = pygame.font.Font(None,25)
  h = screen.get_height()
  w = screen.get_width()
  pygame.draw.rect(screen, (0,0,0),
                    (10, 10, w-10,h-10), 0)
  pygame.draw.rect(screen, (255,255,255),
                    (5, 5, w-5, h-5)
                    , 1)
  for i in xrange(0,len(messages),1):
    if len(messages[i]) != 0:
      screen.blit(fontobject.render(messages[i], 1, (255,255,255)),
                (10,10+20*i))
  pygame.display.flip()

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      if len(current_string) > 0:
        current_string.pop()
    elif inkey == K_RETURN:
      break
    elif inkey <= 255:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name") + " was entered"

if __name__ == '__main__': main()
