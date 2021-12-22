from claspy import *
from _base_ import Base
import utils

class Tapa(Base):
  def _solve(self):
    ans = [[BoolVar() if self.board.getCell(x,y) == None else False for x in range(self.cols)] for y in range(self.rows)]

    # Require connectedness
    connected = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    startingConnectedIndex = IntVar()
    for y in range(self.rows):
      for x in range(self.cols):
        require(cond(ans[y][x], startingConnectedIndex <= y*self.cols+x, True))
        require(~(connected[y][x]^ans[y][x]))
        connected[y][x].prove_if(startingConnectedIndex == y*self.cols+x)
        if y-1 >= 0:
          connected[y][x].prove_if(ans[y][x]&ans[y-1][x]&connected[y-1][x])
        if y+1 < self.rows:
          connected[y][x].prove_if(ans[y][x]&ans[y+1][x]&connected[y+1][x])
        if x-1 >= 0:
          connected[y][x].prove_if(ans[y][x]&ans[y][x-1]&connected[y][x-1])
        if x+1 < self.cols:
          connected[y][x].prove_if(ans[y][x]&ans[y][x+1]&connected[y][x+1])

    # Require no 2x2's
    for y in range(self.rows-1):
      for x in range(self.cols-1):
        require(~(ans[y][x]&ans[y+1][x]&ans[y][x+1]&ans[y+1][x+1]))

    # For each type of clue, generate all possible shaded patterns.
    patternsByClue = {}
    for n in range(256):
      pattern = ''.join(['1' if ((n&(1<<i)) != 0) else '0' for i in range(8)])
      groups = pattern.split('0')
      if len(groups) > 1 and groups[0] != '' and groups[-1] != '':
        groups[0] += groups[-1]
        groups.pop()
      groups = [len(s) for s in groups if len(s) > 0]
      groups.sort()
      groups = str(groups)
      if not groups in patternsByClue:
        patternsByClue[groups] = []
      patternsByClue[groups].append([c == "1" for c in pattern])

    # For each clue, require one of the shaded patterns
    for y in range(self.rows):
      for x in range(self.cols):
        cell = self.board.getCell(x,y)
        if cell == None:
          continue
        patterns = patternsByClue[str(cell)]
        condition = False
        for p in patterns:
          patternCondition = ((ans[y-1][x-1] if (y-1 >= 0 and x-1 >= 0) else False)== p[0]) &\
            ((ans[y-1][x] if (y-1 >= 0) else False)== p[1]) &\
            ((ans[y-1][x+1] if (y-1 >= 0 and x+1 < self.cols) else False)== p[2]) &\
            ((ans[y][x+1] if (x+1 < self.cols) else False)== p[3]) &\
            ((ans[y+1][x+1] if (y+1 < self.rows and x+1 < self.cols) else False)== p[4]) &\
            ((ans[y+1][x] if (y+1 < self.rows) else False)== p[5]) &\
            ((ans[y+1][x-1] if (y+1 < self.rows and x-1 >= 0) else False)== p[6]) &\
            ((ans[y][x-1] if (x-1 >= 0) else False)== p[7])
          condition = condition | patternCondition
        require(condition)

    num_solutions = solve(quiet=True)
    solution = [1 if str(ans[int(i/self.cols)][i%self.cols]) == '1' else 0 for i in range(self.cols*self.rows)]
    return (num_solutions, solution)

  def decode(self):
    c = 0
    i = 0
    bstr = self.body
    board = self.board
    while i < len(bstr):
      ca = bstr[i]
      if utils.include(ca,'0','8'):
        self.board.cell[c] = [int(ca,10)]
      elif ca == '9':
        self.board.cell[c] = [1,1,1,1]
      elif ca == '.':
        self.board.cell[c] = [-2]
      elif utils.include(ca, 'a', 'f'):
        num = int(bstr[i:i+2],36)
        val = []
        if 360 <= num < 396:
          num -= 360
          val = [0,0]
          val[0] = int(num/6)
          num -= val[0]*6
          val[1] = num
        elif 396 <= num < 460:
          num -= 396
          val = [0,0,0]
          val[0] = int(num/16)
          num -= val[0]*16
          val[1] = int(num/4)
          num -= val[1]*4
          val[2] = num
        elif 460 <= num < 476:
          num -= 460
          val = [0,0,0,0]
          val[0] = int(num/8)
          num -= val[0]*8
          val[1] = int(num/4)
          num -= val[1]*4
          val[2] = int(num/2)
          num -= val[2]*2
          val[3] = num
        self.board.cell[c] = [v if v != 0 else -2 for v in val]
        i += 1
      elif utils.include(ca, 'g', 'z'):
        c += int(ca,36)-16
      if self.board.cell[c] != None:
        self.board.cell[c].sort()
      c += 1
      if c >= self.rows*self.cols:
        break
      i += 1
    self.body = bstr[i+1:]
