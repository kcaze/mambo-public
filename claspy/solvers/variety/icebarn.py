from claspy import *
from ._base_ import Base
from . import utils


class Solver(Base):
  def _solve(self):
    U = 1
    L = 1
    R = 2
    D = 2
    arrowsH = utils.makeGrid(self.cols-1, self.rows, lambda: IntVar(0,2))
    arrowsV = utils.makeGrid(self.rows-1, self.cols, lambda: IntVar(0,2))

    # Require connected to in/out
    in_ = self.arrowIn
    out_ = self.arrowOut
    if in_[0] == -1:
      require(
        (arrowsH[in_[1]][0] == R) |
        (arrowsV[0][in_[1]] == D if in_[1] < self.rows-1 else False) |
        (arrowsV[0][in_[1]-1] == U if in_[1] > 0 else False))
    if out_[0] == -1:
      require(
        (arrowsH[out_[1]][0] == L) |
        (arrowsV[0][out_[1]] == U if out_[1] < self.rows-1 else False) |
        (arrowsV[0][out_[1]-1] == D if out_[1] > 0 else False))
    if in_[0] == self.cols:
      require(
        (arrowsH[in_[1]][self.cols-2] == L) |
        (arrowsV[self.cols-1][in_[1]] == D if in_[1] < self.rows-1 else False) |
        (arrowsV[self.cols-1][in_[1]-1] == U if in_[1] > 0 else False))
    if out_[0] == self.cols:
      require(
        (arrowsH[out_[1]][self.cols-2] == R) |
        (arrowsV[self.cols-1][out_[1]] == U if out_[1] < self.rows-1 else False) |
        (arrowsV[self.cols-1][out_[1]-1] == D if out_[1] > 0 else False))
    if in_[1] == -1:
      require(
        (arrowsV[in_[0]][0] == D) |
        (arrowsH[0][in_[0]] == R if in_[0] < self.cols-1 else False) |
        (arrowsH[0][in_[0]-1] == L if in_[0] > 0 else False))
    if out_[1] == -1:
      require(
        (arrowsV[out_[0]][0] == U) |
        (arrowsH[0][out_[0]] == L if out_[0] < self.cols-1 else False) |
        (arrowsH[0][out_[0]-1] == R if out_[0] > 0 else False))
    if in_[1] == self.rows:
      require(
        (arrowsV[in_[0]][self.rows-2] == U) |
        (arrowsH[self.rows-1][in_[0]] == R if in_[0] < self.cols-1 else False) |
        (arrowsH[self.rows-1][in_[0]-1] == L if in_[0] > 0 else False))
    if out_[1] == self.rows:
      require(
        (arrowsV[out_[0]][self.rows-2] == D) |
        (arrowsH[self.rows-1][out_[0]] == L if out_[0] < self.cols-1 else False) |
        (arrowsH[self.rows-1][out_[0]-1] == R if out_[0] > 0 else False))
    

    # Require givens
    for y in range(self.rows):
      for x in range(self.cols-1):
        if self.arrowsH[y][x]:
          require(arrowsH[y][x] == self.arrowsH[y][x])
    for y in range(self.cols):
      for x in range(self.rows-1):
        if self.arrowsV[y][x]:
          require(arrowsV[y][x] == self.arrowsV[y][x])

    # Require directed path must continue along ice
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.cell[y*self.cols+x] == 0:
          continue

        if y == 0 and self.arrowIn == (x,-1):
          require(arrowsV[x][0] == D)
        if y == 0 and self.arrowOut == (x,-1):
          require(arrowsV[x][0] == U)
        if y == self.rows-1 and self.arrowIn == (x,self.rows):
          require(arrowsV[x][self.rows-2] == U)
        if y == self.rows-1 and self.arrowOut == (x,self.rows):
          require(arrowsV[x][self.rows-2] == D)
        if x == 0 and self.arrowIn == (-1, y):
          require(arrowsH[y][0] == R)
        if x == 0 and self.arrowOut == (-1, y):
          require(arrowsH[y][0] == L)
        if x == self.cols-1 and self.arrowIn == (self.cols, y):
          require(arrowsH[y][0] == L)
        if x == self.cols-1 and self.arrowOut == (self.cols, y):
          require(arrowsH[y][0] == R)

        if 0 < x < self.cols-1:
          require(arrowsH[y][x-1] == arrowsH[y][x])
        if 0 < y < self.rows-1:
          require(arrowsV[x][y-1] == arrowsV[x][y])

    # Require no crossings on non-ice cells.
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.cell[y*self.cols+x] != 0:
          continue
        L = []
        if y > 0:
          L.append(arrowsV[x][y-1] != 0)
        if y < self.rows-1:
          L.append(arrowsV[x][y] != 0)
        if x > 0:
          L.append(arrowsH[y][x-1] != 0)
        if x < self.cols-1:
          L.append(arrowsH[y][x] != 0)
        A = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        if self.arrowIn in A or self.arrowOut in A:
          L.append(True)
        require(sum_bools(2,L) | sum_bools(0,L))

    # TODO: This isn't correct right now.
    """
    # Require single connected path
    flowH = utils.makeGrid(self.cols-1, self.rows, lambda: Atom())
    flowV = utils.makeGrid(self.rows-1, self.cols, lambda: Atom())
    if in_[0] == -1:
      flowH[in_[1]][0].prove_if(True)
      if in_[1] < self.rows-1:
        flowV[0][in_[1]].prove_if(True)
      if in_[1] > 0:
        flowV[0][in_[1]-1].prove_if(True)
    if in_[0] == self.cols:
      flowH[in_[1]][self.cols-2].prove_if(True)
      if in_[1] < self.rows-1:
        flowV[self.cols-1][in_[1]].prove_if(True)
      if in_[1] > 0:
        flowV[self.cols-1][in_[1]-1].prove_if(True)
    if in_[1] == -1:
      flowV[in_[0]][0].prove_if(True)
      if in_[0] < self.cols-1:
        flowH[0][in_[0]].prove_if(True)
      if in_[0] > 0:
        flowH[0][in_[0]-1].prove_if(True)
    if in_[1] == self.rows:
      flowV[in_[0]][self.rows-2].prove_if(True)
      if in_[0] < self.cols-1:
        flowH[self.rows-1][in_[0]].prove_if(True)
      if in_[0] > 0:
        flowH[self.rows-1][in_[0]-1].prove_if(True)
    for y in range(self.rows):
      for x in range(self.cols):
        if y < self.rows-1:
          flowV[x][y].prove_if(
            ((arrowsV[x][y] == D) &
              (
                (((arrowsH[y][x] == L) & flowH[y][x]) if x < self.cols-1 else False) |
                (((arrowsH[y][x-1] == R) & flowH[y][x-1]) if x > 0 else False) |
                (((arrowsV[x][y-1] == D) & flowV[x][y-1]) if y > 0 else False)
              )
            ) |
            ((arrowsV[x][y] == U) &
              (
                (((arrowsH[y+1][x] == L) & flowH[y+1][x]) if x < self.cols-1 else False) |
                (((arrowsH[y+1][x-1] == R) & flowH[y+1][x-1]) if x > 0 else False) |
                (((arrowsV[x][y+1] == U) & flowV[x][y+1]) if y < self.rows-2 else False)
              )
            ))
          require(cond(arrowsV[x][y] != 0, flowV[x][y], True))
        if x < self.cols-1:
          flowH[y][x].prove_if(
            ((arrowsH[y][x] == R) &
              (
                (((arrowsV[x][y] == U) & flowV[x][y]) if y < self.rows-1 else False) |
                (((arrowsV[x][y-1] == D) & flowV[x][y-1]) if y > 0 else False) |
                (((arrowsH[y][x-1] == R) & flowH[y][x-1]) if x > 0 else False)
              )
            ) |
            ((arrowsH[y][x] == L) &
              (
                (((arrowsV[x+1][y] == U) & flowV[x+1][y]) if y < self.rows - 1 else False) |
                (((arrowsV[x+1][y-1] == D) & flowV[x+1][y-1]) if y > 0 else False) |
                (((arrowsH[y][x+1] == L) & flowH[y][x+1]) if x < self.cols-2 else False)
              )
            ))
          require(cond(arrowsH[y][x] != 0, flowH[y][x], True))
    """
    
    num_solutions = solve(quiet=True)
    solution = [
      [[utils.intify(i) for i in r] for r in arrowsH],
      [[utils.intify(i) for i in c] for c in arrowsV],
    ]
    return (num_solutions, solution)

  def decode(self):
    U = 1
    L = 1
    R = 2
    D = 2
    # decode ice
    c = 0
    twi = [16,8,4,2,1]
    i = 0
    while True:
      num = int(self.body[i], 32)
      i += 1
      for w in range(5):
        if c < self.cols*self.rows:
          self.board.cell[c] = 6 if (num&twi[w]) else 0
          c += 1
      if c >= self.cols*self.rows:
        break
    self.body = self.body[i:]

    self.arrowsH = [[None for i in range(self.cols-1)] for j in range(self.rows)]
    self.arrowsV = [[None for i in range(self.rows-1)] for j in range(self.cols)]

    # decode border arrow
    id_ = 0
    a = 0
    bdinside = 2*self.cols*self.rows-self.cols-self.rows
    for i in range(a, len(self.body)):
      ca = self.body[i]
      if ca != "z":
        id_ += int(ca, 36)
        if id_ < bdinside:
          if id_ < (self.cols-1)*self.rows:
            self.arrowsH[id_ // (self.cols-1)][id_ % (self.cols-1)] = L
          else:
            j = id_ - (self.cols-1)*self.rows
            self.arrowsV[j % self.cols][j // self.cols] = U
        id_ += 1
      else:
        id_ += 35
      if id_ >= bdinside:
        a = i+1
        break
    id_ = 0
    for i in range(a, len(self.body)):
      ca = self.body[i]
      if ca != "z":
        id_ += int(ca, 36)
        if id_ < bdinside:
          if id_ < (self.cols-1)*self.rows:
            self.arrowsH[id_ // (self.cols-1)][id_ % (self.cols-1)] = R
          else:
            j = id_ - (self.cols-1)*self.rows
            self.arrowsV[j % self.cols][j // self.cols] = D
        id_ += 1
      else:
        id_ += 35
      if id_ >= bdinside:
        a = i+1
        break
    self.body = self.body[a:]
    self.body = self.body.split("/")
    # In/Out arrows are numbered in order of top edge, bottom edge, left edge, then right edge
    # e.g. for a 3x3 they're labeled:
    #   0 1 2
    #  6x x x9
    #  7x x x10
    #  8x x x11
    #   3 4 5
    A = []
    for i in range(self.cols):
      A.append((i,-1))
    for i in range(self.cols):
      A.append((i,self.rows))
    for i in range(self.rows):
      A.append((-1,i))
    for i in range(self.cols):
      A.append((self.cols,i))
    self.arrowIn = A[int(self.body[1])]
    self.arrowOut = A[int(self.body[2])]
