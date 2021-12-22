from claspy import *
from _base_ import Base
import utils

class Hashi(Base):
  def _solve(self):
    set_max_val(3)
    horiAns = utils.makeGrid(self.cols-1, self.rows, lambda: IntVar(0,2))
    vertAns = utils.makeGrid(self.cols, self.rows-1, lambda: IntVar(0,2))
    # Require bridges extend all the way and don't intersect
    for y in range(self.rows):
      for x in range(self.cols-1):
        require(cond(
          horiAns[y][x] > 0,
          ((self.board.getCell(x,y) != None) | (horiAns[y][x-1] == horiAns[y][x] if x-1 >= 0 else False)) &\
          ((self.board.getCell(x+1,y) != None) | (horiAns[y][x+1] == horiAns[y][x] if x+1 < self.cols-1 else False)),
          True))
        require(cond(
          horiAns[y][x] > 0,
          (self.board.getCell(x,y) == None) | (self.board.getCell(x+1,y) == None),
          True))
    for y in range(self.rows-1):
      for x in range(self.cols):
        require(cond(
          vertAns[y][x] > 0,
          ((self.board.getCell(x,y) != None) | (vertAns[y-1][x] == vertAns[y][x] if y-1 >= 0 else False)) &\
          ((self.board.getCell(x,y+1) != None) | (vertAns[y+1][x] == vertAns[y][x] if y+1 < self.rows-1 else False)),
          True))
        require(cond(
          vertAns[y][x] > 0,
          (self.board.getCell(x,y) == None) | (self.board.getCell(x,y+1) == None),
          True))
    # Require numbers to match up
    for y in range(self.rows):
      for x in range(self.cols):
        cell = self.board.getCell(x,y)
        connections = [
          horiAns[y][x-1] if x-1 >= 0 else 0,
          horiAns[y][x] if x < self.cols-1 else 0,
          vertAns[y-1][x] if y-1 >= 0 else 0,
          vertAns[y][x] if y < self.rows-1 else 0,
        ]
        if cell != None:
          require(sum_vars(connections) == cell)
    # Disallow bridge intersections
    for y in range(1, self.rows-1):
      for x in range(1, self.cols-1):
        if self.board.getCell(x,y) == None:
          require((horiAns[y][x-1] == 0) | (horiAns[y][x] == 0) | (vertAns[y-1][x] == 0) | (vertAns[y][x] == 0))
    # Require all islands to be connected
    isConnected = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    firstIsland = False
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y):
          require(isConnected[y][x])
          if not firstIsland:
            isConnected[y][x].prove_if(True)
            firstIsland = True
          # Left
          for xx in range(x-1,-1,-1):
            if self.board.getCell(xx,y):
              isConnected[y][x].prove_if(isConnected[y][xx] & horiAns[y][x-1] > 0)
              break
          # Right
          for xx in range(x+1,self.cols):
            if self.board.getCell(xx,y):
              isConnected[y][x].prove_if(isConnected[y][xx] & horiAns[y][x] > 0)
              break
          # Top
          for yy in range(y-1,-1,-1):
            if self.board.getCell(x,yy):
              isConnected[y][x].prove_if(isConnected[yy][x] & vertAns[y-1][x] > 0)
              break
          # Down
          for yy in range(y+1,self.rows):
            if self.board.getCell(x,yy):
              isConnected[y][x].prove_if(isConnected[yy][x] & vertAns[y][x] > 0)
              break

    num_solutions = solve(quiet=True)
    solution = [
      [utils.intify(horiAns[i/(self.cols-1)][i%(self.cols-1)]) for i in range((self.cols-1)*self.rows)],
      [utils.intify(vertAns[i/self.cols][i%self.cols]) for i in range(self.cols*(self.rows-1))],
    ]
    return (num_solutions, solution)

  def decode(self):
    self.decodeNumber16()
