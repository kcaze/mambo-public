from claspy import *
from ._base_ import Base
from . import utils
class Solver(Base):
  def _solve(self):
    set_max_val(self.rows*self.cols)
    ans = utils.makeGrid(self.cols, self.rows, lambda: IntVar())
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) != None:
          require(ans[y][x] == self.board.getCell(x,y))

    flow = utils.makeGrid(self.cols, self.rows, lambda: MultiVar('.','>','<','v','^'))
    # Require cells that flow into each other to have the same value.
    for y in range(self.rows):
      for x in range(self.cols):
        if y-1 >= 0:
          require(cond(flow[y][x] == '^', ans[y][x] == ans[y-1][x], True))
        else:
          require(flow[y][x] != '^') 
        if y+1 < self.rows:
          require(cond(flow[y][x] == 'v', ans[y][x] == ans[y+1][x], True))
        else:
          require(flow[y][x] != 'v')
        if x-1 >= 0:
          require(cond(flow[y][x] == '<', ans[y][x] == ans[y][x-1], True))
        else:
          require(flow[y][x] != '<')
        if x+1 < self.cols:
          require(cond(flow[y][x] == '>', ans[y][x] == ans[y][x+1], True))
        else:
          require(flow[y][x] != '>')
    # Require each cell connected to a root
    connected = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    for y in range(self.rows):
      for x in range(self.cols):
        require(connected[y][x])
        connected[y][x].prove_if(flow[y][x] == '.')
        if y-1 >= 0:
          connected[y][x].prove_if((flow[y][x] == '^') & connected[y-1][x])
        if y+1 < self.rows:
          connected[y][x].prove_if((flow[y][x] == 'v') & connected[y+1][x])
        if x-1 >= 0:
          connected[y][x].prove_if((flow[y][x] == '<') & connected[y][x-1])
        if x+1 < self.cols:
          connected[y][x].prove_if((flow[y][x] == '>') & connected[y][x+1])
    # Count each spanning tree and make sure the cell numbers match
    counts = utils.makeGrid(self.cols, self.rows, lambda: IntVar())
    for y in range(self.rows):
      for x in range(self.cols):
        count = 1
        if y-1 >= 0:
          count += cond((flow[y-1][x] == 'v'), counts[y-1][x], 0)
        if y+1 < self.rows:
          count += cond((flow[y+1][x] == '^'), counts[y+1][x], 0)
        if x-1 >= 0:
          count += cond((flow[y][x-1] == '>'), counts[y][x-1], 0)
        if x+1 < self.cols:
          count += cond((flow[y][x+1] == '<'), counts[y][x+1], 0)
        require(counts[y][x] == count)
        require(~((flow[y][x] == '.')^(counts[y][x] == ans[y][x])))
    # Compute the root indexes for cells in each group.
    rootIdxs = [[IntVar(0,y*self.cols+x) for x in range(self.cols)] for y in range(self.rows)]
    for y in range(self.rows):
      for x in range(self.cols):
        require(~((flow[y][x]=='.')^(rootIdxs[y][x] == y*self.cols+x)))
        if y-1 >= 0:
          require(cond(flow[y][x] == '^', rootIdxs[y][x] == rootIdxs[y-1][x], True))
        if y+1 < self.rows:
          require(cond(flow[y][x] == 'v', rootIdxs[y][x] == rootIdxs[y+1][x], True))
        if x-1 >= 0:
          require(cond(flow[y][x] == '<', rootIdxs[y][x] == rootIdxs[y][x-1], True))
        if x+1 < self.cols:
          require(cond(flow[y][x] == '>', rootIdxs[y][x] == rootIdxs[y][x+1], True))
    # Check that every pair of grid cells with the same number belong to adjacent regions.
    """
    special_rule = {}
    for y1 in range(self.rows):
      for x1 in range(self.cols):
        for y2 in range(self.rows):
          for x2 in range(self.cols):
            if (x1,y1) == (x2,y2):
              continue
            special_rule[(x1,y1,x2,y2)] = Atom()
            require(special_rule[(x1,y1,x2,y2)])
    for y1 in range(self.rows):
      for x1 in range(self.cols):
        for y2 in range(self.rows):
          for x2 in range(self.cols):
            if (x1,y1) == (x2,y2):
              continue
            if abs(x1-x2) + abs(y1-y2) == 1:
              special_rule[(x1,y1,x2,y2)].prove_if(True)
            else:
              special_rule[(x1,y1,x2,y2)].prove_if(ans[y1][x1] != ans[y2][x2])
              for (dx,dy) in [(-1,0), (1,0), (0,1), (0,-1)]:
                if 0 <= x1+dx < self.rows and 0 <= y1+dy < self.cols:
                  special_rule[(x1,y1,x2,y2)].prove_if(
                    special_rule[(x1+dx,y1+dy,x2,y2)]&
                    (ans[y1+dy][x1+dx] == ans[y1][x1])&
                    ((rootIdxs[y1][x1] == rootIdxs[y1+dy][x1+dx])|(rootIdxs[y2][x2] == rootIdxs[y1+dy][x1+dx])))
                if 0 <= x2+dx < self.rows and 0 <= y2+dy < self.cols:
                  special_rule[(x1,y1,x2,y2)].prove_if(
                    special_rule[(x1,y1,x2+dx,y2+dy)]&
                    (ans[y2+dy][x2+dx] == ans[y2][x2])&
                    ((rootIdxs[y1][x1] == rootIdxs[y2+dy][x2+dx])|(rootIdxs[y2][x2] == rootIdxs[y2+dy][x2+dx]))
                    )
    """

    num_solutions = solve(quiet=True)
    solution = [utils.intify(ans[i//self.cols][i%self.cols]) for i in range(self.rows*self.cols)]
    return (num_solutions, solution)

  def decode(self):
    self.decodeNumber16()
