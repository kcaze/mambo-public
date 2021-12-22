from claspy import *
from _base_ import Base
import utils

# Note: This puzzle is more commonly known as Skyscrapers.
class Building(Base):
  def _solve(self):
    top = self.board.excell[0:self.cols]
    bottom = self.board.excell[self.cols:2*self.cols]
    left = self.board.excell[2*self.cols:2*self.cols+self.rows]
    right = self.board.excell[2*self.cols+self.rows:]

    ans = utils.makeGrid(self.cols, self.rows, lambda: IntVar(1,self.cols))
    topViewable = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    bottomViewable = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    leftViewable = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    rightViewable = utils.makeGrid(self.cols, self.rows, lambda: Atom())

    # All numbers in columns and rows are distinct
    for i in range(self.rows):
      require_all_diff(ans[i])
    for i in range(self.cols):
      require_all_diff([ans[j][i] for j in range(self.rows)])
    # Prove skyscraper viewability
    for y in range(self.rows):
      for x in range(self.cols):
        t = True
        for k in range(y):
          t = t & (ans[y][x] > ans[k][x])
        topViewable[y][x].prove_if(t)
        b = True
        for k in range(y+1,self.rows):
          b = b & (ans[y][x] > ans[k][x])
        bottomViewable[y][x].prove_if(b)
        l = True
        for k in range(x):
          l = l & (ans[y][x] > ans[y][k])
        leftViewable[y][x].prove_if(l)
        r = True
        for k in range(x+1,self.cols):
          r = r & (ans[y][x] > ans[y][k])
        rightViewable[y][x].prove_if(r)
    # Ensure skyscraper viewable numbers
    for x in range(self.cols):
      if top[x] != None:
        require(sum_bools(top[x], [topViewable[y][x] for y in range(self.rows)]))
      if bottom[x] != None:
        require(sum_bools(bottom[x], [bottomViewable[y][x] for y in range(self.rows)]))
    for y in range(self.rows):
      if left[y] != None:
        require(sum_bools(left[y], [leftViewable[y][x] for x in range(self.cols)]))
      if right[y] != None:
        require(sum_bools(right[y], [rightViewable[y][x] for x in range(self.cols)]))

    num_solutions = solve(quiet=True)
    solution = [utils.intify(ans[i/self.cols][i%self.cols]) for i in range(self.rows*self.cols)]
    return (num_solutions, solution)

  def decode(self):
    ec = 0
    i = 0
    bstr = self.body
    while i <= len(bstr):
      ca = bstr[i]
      if utils.include(ca, "0", "9") or utils.include(ca, "a", "f"):
        self.board.excell[ec] = int(bstr[i:i+1],16)
      elif ca == "-":
        self.board.excell[ec] = int(bstr[i:i+2],16)
        i += 2
      elif ca == ".":
        self.board.excell[ec] = -2
      elif "g" <= ca <= "z":
        ec += int(ca,36)-16
      ec += 1
      if (ec >= len(self.board.excell)):
        break
      i += 1
    self.body = bstr[i+1:]
