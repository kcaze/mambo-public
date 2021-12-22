from claspy import *
from _base_ import Base
import utils

class Mashu(Base):
  def _solve(self):
    horizontalFences = utils.makeGrid(self.cols-1, self.rows, lambda: BoolVar())
    verticalFences = utils.makeGrid(self.rows-1, self.cols, lambda: BoolVar())
    dbg = utils.require_single_closed_loop_v2(horizontalFences, verticalFences)

    def getHori(x,y):
      if y < 0 or y >= self.rows:
        return False
      if x < 0 or x >= self.cols-1:
        return False
      return horizontalFences[y][x]

    def getVert(x,y):
      if y < 0 or y >= self.rows-1:
        return False
      if x < 0 or x >= self.cols:
        return False
      return verticalFences[x][y]

    for y in range(self.rows):
      for x in range(self.cols):
        # Requirements on white circles
        if self.board.getCell(x,y) == 1:
          horiLeft = getHori(x-1,y) & getHori(x,y) & (getVert(x-1,y-1) | getVert(x-1,y))
          horiRight = getHori(x-1,y) & getHori(x,y) & (getVert(x+1,y-1) | getVert(x+1,y))
          vertTop = getVert(x,y-1) & getVert(x,y) & (getHori(x-1,y-1) | getHori(x,y-1))
          vertBottom = getVert(x,y-1) & getVert(x,y) & (getHori(x-1,y+1) | getHori(x,y+1))
          require(horiLeft | horiRight | vertTop | vertBottom)
        # Requirements on black circles
        if self.board.getCell(x,y) == 2:
          topLeft = getHori(x-2,y) & getHori(x-1,y) & getVert(x,y-1) & getVert(x,y-2)
          topRight = getHori(x,y) & getHori(x+1,y) & getVert(x,y-1) & getVert(x,y-2)
          bottomLeft = getHori(x-2,y) & getHori(x-1,y) & getVert(x,y) & getVert(x,y+1)
          bottomRight = getHori(x,y) & getHori(x+1,y) & getVert(x,y) & getVert(x,y+1)
          require(topLeft | topRight | bottomLeft | bottomRight)
    
    num_solutions = solve(quiet=True)
    solution = {
      'horizontalFences': [[utils.intify(x) for x in r] for r in horizontalFences],
      'verticalFences': [[utils.intify(x) for x in r] for r in verticalFences],
    }
    return (num_solutions, solution)

  def decode(self):
    self.decodeCircle();
    self.decodeNumber16()
