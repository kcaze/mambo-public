from claspy import *
from _base_ import Base
import utils
class Fillomino(Base):
  def _solve(self):
    set_max_val(self.rows*self.cols)
    ans = utils.makeGrid(self.cols, self.rows, lambda: IntVar())
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) != None:
          require(ans[y][x] == self.board.getCell(x,y))
    # Count number of same neighbors for special restrictions on 1's, 2's, 3's, and 4's.
    edgesHorizontal = [[] for i in range(self.rows)]
    edgesVertical = [[] for i in range(self.rows-1)]
    sameNeighbors = [[] for i in range(self.rows)]
    for y in range(self.rows):
      for x in range(self.cols):
        if y+1 < self.rows:
          edgesVertical[y].append(ans[y][x] == ans[y+1][x]) 
        if x+1 < self.cols:
          edgesHorizontal[y].append(ans[y][x] == ans[y][x+1])
    for y in range(self.rows):
      for x in range(self.cols):
        sameVars = []
        if y-1 >= 0:
          sameVars.append(edgesVertical[y-1][x])
        if y+1 < self.rows:
          sameVars.append(edgesVertical[y][x])
        if x-1 >= 0:
          sameVars.append(edgesHorizontal[y][x-1])
        if x+1 < self.cols:
          sameVars.append(edgesHorizontal[y][x])
        sameNeighbors[y].append(sum_vars(sameVars))
    for y in range(self.rows):
      for x in range(self.cols):
        require(~((ans[y][x] == 1)^(sameNeighbors[y][x] == 0)))
        require(~((ans[y][x] == 2)&(sameNeighbors[y][x] != 1)))
        require(~((ans[y][x] == 3)&(sameNeighbors[y][x] != 1)&(sameNeighbors[y][x]!=2)))
        require(~((ans[y][x] == 4)&(sameNeighbors[y][x] == 4)))

    flow = utils.makeGrid(self.cols, self.rows, lambda: MultiVar('.','>','<','v','^'))
    # Require cells that flow into each other to have the same value.
    for y in range(self.rows):
      for x in range(self.cols):
        if y-1 >= 0:
          require(cond(flow[y][x] == '^', edgesVertical[y-1][x], True))
        else:
          require(flow[y][x] != '^') 
        if y+1 < self.rows:
          require(cond(flow[y][x] == 'v', edgesVertical[y][x], True))
        else:
          require(flow[y][x] != 'v')
        if x-1 >= 0:
          require(cond(flow[y][x] == '<', edgesHorizontal[y][x-1], True))
        else:
          require(flow[y][x] != '<')
        if x+1 < self.cols:
          require(cond(flow[y][x] == '>', edgesHorizontal[y][x], True))
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
    # Ensure different groups with the same number don't touch
    rootIdxs = [[IntVar(0,y*self.cols+x) for x in range(self.cols)] for y in range(self.rows)]
    for y in range(self.rows):
      for x in range(self.cols):
        require(~((flow[y][x]=='.')^(rootIdxs[y][x] == y*self.cols+x)))
        if y-1 >= 0:
          require(~((ans[y][x]==ans[y-1][x])^(rootIdxs[y][x]==rootIdxs[y-1][x])))
        if y+1 < self.rows:
          require(~((ans[y][x]==ans[y+1][x])^(rootIdxs[y][x]==rootIdxs[y+1][x])))
        if x-1 >= 0:
          require(~((ans[y][x]==ans[y][x-1])^(rootIdxs[y][x]==rootIdxs[y][x-1])))
        if x+1 < self.cols:
          require(~((ans[y][x]==ans[y][x+1])^(rootIdxs[y][x]==rootIdxs[y][x+1])))

    num_solutions = solve(quiet=True)
    solution = [utils.intify(ans[i/self.cols][i%self.cols]) for i in range(self.rows*self.cols)]
    return (num_solutions, solution)

  def decode(self):
    self.decodeNumber16()
