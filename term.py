import curses
import time
import random
from assets import Eminem, Bomb, Gun, Bullet


stdscr = curses.initscr()


win = curses.newwin(24, 80, 0, 0)


class Iterate:
  MAX_BOMBS = 20
  YOU_WIN = 'win'
  YOU_LOST = 'lost'
  YOU_PLAY = 'plaiyng'
  bombs = {}
  shots = {}
  eminems = {}
  
  def __init__(self, window, gun, army):
    
    self.bombs = {}
    self.shots = {}
    self.eminems = {}
    
    self.window = window
    self.gun = gun
    self.eminems = army
    self.max_killed = len(army)
    self.shots_num = 0
    self.score = 0
    self.killed = 0
    self.helth = gun.get_helth()
  
  def show_info(self):
    #self.window.addstr(0,0, f'= {key}')
    self.window.addstr(23,40,f'helth:{self.helth} shots:{self.shots_num}  score:{self.score} killed:{self.killed} ')    
    #win.addstr(4,60,f'score:{[i[0] for i in self.eminems.items()]}')    
    
  
  def shouting(self, shot):
    self.shots[shot.get_id()] = shot
    self.shots_num +=1
    self.score -= 2
    for e in self.eminems.values():
      e.subscribe(shot)
      
  def shot_missing(self, shot):
      for e in self.eminems.values():
        e.unsubscribe(shot) 
      self.shots.pop(shot.get_id())  
  
  def managing(self, key):
    s = self.gun.act(key)
    if isinstance(s, Bullet):
      self.shouting(s)

  
  
  def bombing(self):
    for e in self.eminems.values():
      b = e.bombing()
      if isinstance(b, Bomb):
        self.bombs[b.get_id()] = b
        self.gun.subscribe(b)
        
  def bomb_missing(self, bomb):
    self.bombs.pop(bomb.get_id())
    self.gun.unsubscribe(bomb)
  
  def step(self):
    if len(self.bombs)<=self.MAX_BOMBS:
      self.bombing()
    
    miss = []
    for b in self.bombs.items():
      res = b[1].move()
      if res == 'miss':
        miss.append(b)
      b[1].show()
    for i in miss:
      self.bomb_missing(i[1])

      
    miss = []
    for s in self.shots.items():
      res = s[1].move()
      if res == 'miss':
        miss.append(s)
        #self.shot_missing(s[1])
      s[1].show()
    for i in miss:
      self.shot_missing(i[1])

    self.gun.move()
    self.gun.show()
      
    killed = []
    for e in self.eminems.items():
      kld, scr = e[1].check_crush()
      e[1].show()
      if kld:
        self.killed +=1
        killed.append(e[0])
      self.score += scr*10
    self.eminems = {i[0]:i[1] for i in self.eminems.items() if i[0] not in killed}      
    
    
    self.helth, exploded = self.gun.is_beaten()
    if len(exploded) >0:
      self.score -= len(exploded)*10
      for i in exploded:
        self.bomb_missing(i)
    
    if self.killed == self.max_killed:
      return (True, self.YOU_WIN, self.score)

    if self.helth <=0:
      return (True, self.YOU_LOST, self.score)
    
    return (False, self.YOU_PLAY, self.score)
    
  
borders = (0,80,23)

key = ''
curses.noecho()
curses.curs_set(0)
win.keypad(1)
win.nodelay(1)
shots = []
bombs = []
victory = False

gun = Gun(win,borders[0],borders[1])


army = {i.get_id(): i for i in [Eminem(win, i*2) for i in range(1,7)]}

print(army)

iterate = Iterate(win, gun, army)

while key != 27: 
  time.sleep(0.02)

  try:
    key = win.getch()
    if key != -1:

      iterate.managing(key)
      
    victory, state, score = iterate.step()
    iterate.show_info()
    if victory:
      break
    
    #win.addstr(23,25,f'bullets:{len(shots)}')
    

  except curses.error:
    print('ohh')
    break;
    
    # {str(chr(key))} 
curses.endwin()

if state == 'win':
  print(f'\n\n\nCongratulation! Your final score {score}\n\n\n')
elif state == 'lost':
  print(f'\n\n\nYOU ARE LOST\n\n\n')
if key == 27:
  print(f'\n\n\nGAME ABORTED\n\n\n')