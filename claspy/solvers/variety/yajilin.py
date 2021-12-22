from claspy import *
from _base_ import Base
import utils

U = 1
D = 2
L = 3
R = 4

class Yajilin(Base):
  def _solve(self):
    horizontalFences = [[] for i in range(self.rows)]
    verticalFences = [[] for i in range(self.cols)]
    for y in range(self.rows):
      for x in range(self.cols-1):
        cellLeft = self.board.getCell(x,y) 
        cellRight = self.board.getCell(x+1,y) 
        horizontalFences[y].append(BoolVar() if cellLeft == None and cellRight == None else False)
    for x in range(self.cols):
      for y in range(self.rows-1):
        cellUp = self.board.getCell(x,y) 
        cellDown = self.board.getCell(x,y+1) 
        verticalFences[x].append(BoolVar() if cellUp == None and cellDown == None else False)
    
    utils.require_single_closed_loop_v2(horizontalFences, verticalFences)
    shaded = [[BoolVar() if self.board.getCell(x,y) == None else False for x in range(self.cols)] for y in range(self.rows)]
    # Shaded squares are those without loops or clues
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) == None:
          require(shaded[y][x] == ~(\
            utils.idx(horizontalFences,y,x-1,False) |\
            utils.idx(horizontalFences,y,x,False) |\
            utils.idx(verticalFences,x,y-1,False) |\
            utils.idx(verticalFences,x,y,False)))
    # Shaded squares do not touch.
    for y in range(self.rows-1):
      for x in range(self.cols):
        require(~(shaded[y][x]&shaded[y+1][x]))
    for y in range(self.rows):
      for x in range(self.cols-1):
        require(~(shaded[y][x]&shaded[y][x+1]))
    # Require clue sums
    for y in range(self.rows):
      for x in range(self.cols):
        cell = self.board.getCell(x,y)
        if cell == None:
          continue
        direction = cell[0]
        count = cell[1]
        if direction == U:
          require(sum_bools(count, [shaded[i][x] for i in range(y)]))
        elif direction == D:
          require(sum_bools(count, [shaded[i][x] for i in range(y+1,self.rows)]))
        elif direction == L:
          require(sum_bools(count, [shaded[y][i] for i in range(x)]))
        elif direction == R:
          require(sum_bools(count, [shaded[y][i] for i in range(x+1,self.cols)]))

    num_solutions = solve(quiet=True)
    solution = {
      'horizontalFences': [[1 if str(x) == '1' else 0 for x in r] for r in horizontalFences],
      'verticalFences': [[1 if str(x) == '1' else 0 for x in r] for r in verticalFences],
    }
    return (num_solutions, solution)

  def decode(self):
    self.decodeArrowNumber16()
