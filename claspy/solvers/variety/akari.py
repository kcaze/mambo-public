from claspy import *
from _base_ import Base
import utils

class Akari(Base):
  def _solve(self):
    ans = utils.makeGrid(self.cols, self.rows, lambda: BoolVar())
    lit = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    for y in range(self.rows):
      for x in range(self.cols):
        # Lights can't be on black squares
        cell = self.board.getCell(x,y)
        if cell != None:
          require(~ans[y][x])
        # Require the right number of neighbors for lights
        if cell != None and cell >= 0:
          neighbors = [
            ans[y-1][x] if y-1 >= 0 else False,
            ans[y+1][x] if y+1 < self.rows else False,
            ans[y][x-1] if x-1 >= 0 else False,
            ans[y][x+1] if x+1 < self.cols else False,
          ]
          require(sum_bools(cell, neighbors))
        # Prevent lights from shining on each other and ensure each non-black cell is lit
        if cell == None:
          require(lit[y][x])
          if y == 0 or self.board.getCell(x,y-1) != None:
            arr = []
            litArr = []
            yy = y
            while yy < self.rows and self.board.getCell(x,yy) == None:
              arr.append(ans[yy][x])
              litArr.append(lit[yy][x])
              yy += 1
            require(at_most(1, arr))
            for a in arr:
              for l in litArr:
                l.prove_if(a)
          if x == 0 or self.board.getCell(x-1,y) != None:
            arr = []
            litArr = []
            xx = x
            while xx < self.cols and self.board.getCell(xx,y) == None:
              arr.append(ans[y][xx])
              litArr.append(lit[y][xx])
              xx += 1
            require(at_most(1, arr))
            for a in arr:
              for l in litArr:
                l.prove_if(a)

    num_solutions = solve(quiet=True)
    solution = [utils.intify(ans[i/self.cols][i%self.cols]) for i in range(self.cols*self.rows)]
    return (num_solutions, solution)

  def decode(self):
    self.decode4Cell()
