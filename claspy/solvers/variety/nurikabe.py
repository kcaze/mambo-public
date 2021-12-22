from claspy import *
from _base_ import Base
import utils

class Nurikabe(Base):
  def _solve(self):
    set_max_val(self.rows*self.cols)
    ans = [[] for i in range(self.rows)]
    values = []
    for y in range(self.rows):
      for x in range(self.cols):
        cell = self.board.getCell(x,y)
        if cell != None:
          values.append(y*self.cols+x)
    for y in range(self.rows):
      for x in range(self.cols):
        cell = self.board.getCell(x,y)
        if cell == None:
          possibleValues = ['*'] + [v for v in values if (abs(x-(v%self.cols)) + abs(y-int(v/self.cols))) < self.board.getCell(v%self.cols, int(v/self.cols))]
          ans[y].append(MultiVar(*possibleValues))
        else:
          ans[y].append(y*self.cols+x)

    # Require connectedness
    connected = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    startingConnectedIndex = IntVar()
    for y in range(self.rows):
      for x in range(self.cols):
        require(cond(ans[y][x] == '*', startingConnectedIndex <= y*self.cols+x, True))
        require(~(connected[y][x] ^ (ans[y][x] == '*')))
        connected[y][x].prove_if(startingConnectedIndex == y*self.cols+x)
        if y-1 >= 0:
          connected[y][x].prove_if((ans[y][x] == '*')&(ans[y-1][x] == '*')&connected[y-1][x])
        if y+1 < self.rows:
          connected[y][x].prove_if((ans[y][x] == '*')&(ans[y+1][x] == '*')&connected[y+1][x])
        if x-1 >= 0:
          connected[y][x].prove_if((ans[y][x] == '*')&(ans[y][x-1] == '*')&connected[y][x-1])
        if x+1 < self.cols:
          connected[y][x].prove_if((ans[y][x] == '*')&(ans[y][x+1] == '*')&connected[y][x+1])

    # Require no 2x2's
    for y in range(self.rows-1):
      for x in range(self.cols-1):
        require(~((ans[y][x]=='*')&(ans[y+1][x]=='*')&(ans[y][x+1]=='*')&(ans[y+1][x+1]=='*')))

    # Require each nonshaded cell connected to a root
    islandConnected = [[] for r in range(self.rows)]
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) == None:
          islandConnected[y].append(Atom())
        else:
          islandConnected[y].append(True)
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) != None:
          continue
        require(~(islandConnected[y][x]^(ans[y][x]!='*')))
        if y-1 >= 0:
          islandConnected[y][x].prove_if((ans[y][x]==ans[y-1][x]) & islandConnected[y-1][x])
        if y+1 < self.rows:
          islandConnected[y][x].prove_if((ans[y][x]==ans[y+1][x]) & islandConnected[y+1][x])
        if x-1 >= 0:
          islandConnected[y][x].prove_if((ans[y][x]==ans[y][x-1]) & islandConnected[y][x-1])
        if x+1 < self.cols:
          islandConnected[y][x].prove_if((ans[y][x]==ans[y][x+1]) & islandConnected[y][x+1])

    # Require numbers equal island sizes
    for v in values:
      y = int(v / self.cols)
      x = v % self.cols 
      c = self.board.getCell(x,y)
      cells = [ans[int(i/self.cols)][i%self.cols] == v for i in range(self.rows*self.cols) if abs(x-(i%self.cols)) + abs(y-int(i/self.cols)) < c]
      require(sum_bools(c, cells))

    # Ensure different groups with the same number don't touch
    for y in range(self.rows):
      for x in range(self.cols-1):
        require((ans[y][x]=='*')|(ans[y][x+1]=='*')|(ans[y][x]==ans[y][x+1]))
    for y in range(self.rows-1):
      for x in range(self.cols):
        require((ans[y][x]=='*')|(ans[y+1][x]=='*')|(ans[y][x]==ans[y+1][x]))

    num_solutions = solve(quiet=True)
    solution = [1 if str(ans[int(i/self.cols)][i%self.cols]=='*') == '1' else 0 for i in range(self.cols*self.rows)]
    return (num_solutions, solution)

  def decode(self):
    self.decodeNumber16()
