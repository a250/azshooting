import random

class Weapon:
  
  def __init__(self, window):
    self.window = window
    self.id = random.randint(0,100_000)    
  
  def get_id(self):
    return self.id  
  
  def get_xy(self):
    return (self.x, self.y)

class Bullet(Weapon):
  FIRE = 'fire'
  MISS = 'miss'
  
  def __init__(self, window, x, y, offset):

    super().__init__(window)
    
    self.x = x+offset
    self.y = 19
    self.y_prev = 19
    self.bullet = '|'
    self.status = self.FIRE

  def move(self):
    self.y_prev = self.y
    if self.status == self.FIRE:
      self.y -=1
    if self.y == 0:
      self.status = self.MISS    
      return self.MISS
    else:
      return self.FIRE
    
  def show(self):
    if self.status == self.FIRE:
      self.window.addstr(self.y, self.x, self.bullet)
    self.window.addstr(self.y_prev, self.x,' ')

class Bomb(Weapon):
  
  FALL = 'fall'
  MISS = 'miss'
  
  def __init__(self, window, x, offset):
    
    super().__init__(window) 
    
    self.x = x+offset
    self.y = 3
    self.y_sc = 3
    self.bomb = 'o'
    self.status = self.FALL
    
  def move(self):
    self.y_prev = self.y
    if self.status == self.FALL:
      self.y_sc += 0.1
      self.y = round(self.y_sc)
    if self.y == 23:
      self.status = self.MISS
      return self.MISS
    else:
      return self.FALL
  
  def show(self, debug = False):
    if self.status == self.FALL:
      self.window.addstr(round(self.y_sc), self.x, self.bomb)
    if self.y_prev != self.y:
      self.window.addstr(round(self.y_prev), self.x,' ')   
      
    if debug:
      self.window.addstr(18, 40, f'id:{self.id}')
    

class Eminem:
  eminem = ['     ', '-----', 'i+++i', 'I---I', 'H===H', 'ШшшшШ']
  
  
  def __init__(self, window, x):
    self.shots = {}
    self.helth = 5
    self.pos_x = x*5
    self.l_area = self.pos_x
    self.r_area = self.pos_x+5
    self.window = window
    self.crush = False
    
    self.id = random.randint(0,100_000)    
    
  def get_id(self):
    return self.id  
    
  def show(self, debug = False):
    self.window.addstr(2, self.pos_x, self.eminem[self.helth])    
    if debug:
      self.window.addstr(3, self.pos_x, f'{[i[0] for i in self.shots.items()]}')      
  
  def act(self, bullet):
    if (bullet.y == 2) and ((self.l_area <= bullet.x) and (self.r_area >= bullet.x)):
      if self.helth >0:
        self.helth -=1
  
  def bombing(self):
    atack = round(random.random()*1000)>990
    
    if self.helth !=0 and atack:
      return Bomb(self.window, self.pos_x, random.randint(0,4))
    else: 
      return None
  
  def subscribe(self, shot):
    self.shots[shot.get_id()] = shot
  
  def unsubscribe(self, shot):
    self.shots.pop(shot.get_id())
    
  def check_crush(self):
    bit = 0
    if not self.crush:
      for s in self.shots.items():
        x,y = s[1].get_xy()
        if (y == 2) and (self.l_area<=x) and (x<=self.r_area):
          self.helth -=1
          bit +=1
          #self.shots.pop(s[1].get_id())
      if self.helth <=0:
          self.crush = True
      return (self.crush, bit)
    else:
      return (False,0)
  
class Gun:

  gun = " ___=|=___ "
  MOVE_LEFT = 'left'
  MOVE_RIGHT = 'right'
  NO_MOVE = 'stop'
  status = NO_MOVE
  gun_length = len(gun)
  gun_position = 5
  
    
  def __init__(self, window, l, r):
    self.x = 1
    self.y = 20
    self.window = window
    self.left_border = l
    self.right_border = r
    self.l_area = self.x
    self.r_area = self.x +9
    self.helth = 10
    self.bombs = {}

  def get_helth(self):
    return self.helth
    
  def act(self, key):
    if key == 260:
      self.status = self.MOVE_LEFT
    if key == 261:
      self.status = self.MOVE_RIGHT
    if key == 259:
      return Bullet(self.window, self.x, self.y, self.gun_position)
    
  def move(self):
    if self.status == self.MOVE_LEFT:
      self.x -=1
    if self.status == self.MOVE_RIGHT:
      self.x +=1

    self.l_area = self.x
    self.r_area = self.x +9
      
    if self.x == self.left_border:
      self.status = self.MOVE_RIGHT
    if self.x == self.right_border - self.gun_length:
      self.status = self.MOVE_LEFT
    
  def show(self, debug = False):
    self.window.addstr(self.y, self.x, self.gun)
    if debug:
      self.window.addstr(23,0,f'x:{self.x} #bombs:{[i.get_xy() for i in self.bombs.values()]}')

  def subscribe(self, bomb):
    self.bombs[bomb.get_id()] = bomb
  
  def unsubscribe(self, bomb):
    self.bombs.pop(bomb.get_id())

  def is_beaten(self):
    exploded = []
    for b in self.bombs.items():
      x,y = b[1].get_xy()
      if (y == 20) and (self.l_area<=x) and (x<=self.r_area):
        self.helth -=1
        exploded.append(b[1])
    return (self.helth, exploded)

if __name__ == "__main__":
  print('No run module')