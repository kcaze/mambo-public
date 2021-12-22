from claspy import *
from _base_ import Base
import itertools
import utils

class Starbattle(Base):
  def _solve(self):
    stars = utils.makeGrid(self.cols, self.rows, lambda: BoolVar())
    # starCount stars per row
    for y in range(self.rows):
      require(sum_bools(self.starCount, stars[y]))
    # starCount stars per column
    for x in range(self.cols):
      require(sum_bools(self.starCount, [stars[y][x] for y in range(self.rows)]))
    # stars can't be adjacent (including diagonal)
    for y in range(self.rows):
      for x in range(self.cols):
        threeByThree = [stars[y+dy][x+dx] if 0 <= y+dy < self.rows and 0 <= x+dx < self.cols else False for (dx,dy) in list(itertools.product([-1,0,1], [-1,0,1]))]
        require(cond(stars[y][x], sum_bools(1, threeByThree), True))
    # starCount stars per region.
    usedInRegion = utils.makeGrid(self.cols, self.rows, lambda: False)
    for y in range(self.rows):
      for x in range(self.cols):
        if usedInRegion[y][x]: continue 
        toProcess = [(x,y)]
        region = []
        while len(toProcess):
          newToProcess = [] 
          for p in toProcess:
            usedInRegion[p[1]][p[0]] = True
            region.append(stars[p[1]][p[0]])
          for p in toProcess:
            if p[0] - 1 >= 0 and not usedInRegion[p[1]][p[0]-1] and not self.board.border[1][p[1]][p[0]-1]:
              newToProcess.append((p[0]-1,p[1]))
            if p[0] + 1 < self.cols and not usedInRegion[p[1]][p[0]+1] and not self.board.border[1][p[1]][p[0]]:
              newToProcess.append((p[0]+1,p[1]))
            if p[1] - 1 >= 0 and not usedInRegion[p[1]-1][p[0]] and not self.board.border[0][p[1]-1][p[0]]:
              newToProcess.append((p[0],p[1]-1))
            if p[1] + 1 < self.rows and not usedInRegion[p[1]+1][p[0]] and not self.board.border[0][p[1]][p[0]]:
              newToProcess.append((p[0],p[1]+1))
          toProcess = list(set(newToProcess))
        require(sum_bools(self.starCount, region))
        
    num_solutions = solve(quiet=True)
    solution = [[utils.intify(x) for x in r] for r in stars]
    return (num_solutions, solution)

  def decode(self):
    self.decodeStarCount()
    self.decodeBorder()

  def decodeStarCount(self):
    barray = self.body.split("/")
    bd = self.board
    self.starCount = int(barray[0])
    self.body = barray[1] if len(barray) > 1 else ""
