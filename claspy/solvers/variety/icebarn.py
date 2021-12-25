from claspy import *
from ._base_ import Base
from . import utils


class Solver(Base):
  def _solve(self):
    # Create path of dimensions (width+2) x (height+2) to accomodate for the border.
    h, v = utils.path(self.cols+2, self.rows+2)
    utils.require_directed(h,v)

    # Disallow paths on the outside, except for the in and out.
    i, o = (self.arrowIn, self.arrowOut)
    for y in range(self.rows+1):
      require(v[0][y] == 0)
      require(v[self.cols+1][y] == 0)
      if 1 <= y <= self.rows:
        w = utils.R if (-1,y-1) == i else utils.L if (-1,y-1) == o else 0
        require(h[0][y] == w)
        w = utils.L if (self.cols,y-1) == i else utils.R if (self.cols,y-1) == o else 0
        require(h[self.cols][y] == w)
    for x in range(self.cols+1):
      require(h[x][0] == 0)
      require(h[x][self.rows+1] == 0)
      if 1 <= x <= self.cols:
        w = utils.D if (x-1,-1) == i else utils.U if (x-1,-1) == o else 0
        require(v[x][0] == w)
        w = utils.U if (x-1,self.rows) == i else utils.D if (x-1,self.rows) == o else 0
        require(v[x][self.rows] == w)

    # Require in to be connected to out.
    utils.require_two_points_connected_directed(h,v,i[0]+1,i[1]+1,o[0]+1,o[1]+1)

    # Require givens
    for y in range(self.rows):
      for x in range(self.cols-1):
        if self.arrowsH[y][x]:
          require(h[x+1][y+1] == self.arrowsH[y][x])
    for x in range(self.cols):
      for y in range(self.rows-1):
        if self.arrowsV[x][y]:
          require(v[x+1][y+1] == self.arrowsV[x][y])

    # Require directed path must continue along ice
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.cell[y*self.cols+x] == 0:
          continue
        u,d,l,r = utils.edges(h,v,x+1,y+1)
        require(l == r)
        require(u == d)

    # Require no crossings on non-ice cells.
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.cell[y*self.cols+x] != 0:
          continue
        utils.require_no_self_intersection_directed(h,v,x+1,y+1)

    # Require single path.
    (comp, ph, pv) = utils.number_components(h,v)
    require(sum_bools(1, comp))
    require(sum_bools(2, utils.number_ends(h,v)))

    # Require each icebarn is used.
    barn_proof = [[Atom() for y in range(self.rows)] for x in range(self.cols)]
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.cell[y*self.cols+x] == 0:
          continue
        require(barn_proof[x][y])
        u,d,l,r = utils.edges(h,v,x+1,y+1)
        barn_proof[x][y].prove_if(at_least(1, [u != 0, d != 0, l != 0, r != 0]))
        if y > 0 and self.board.cell[(y-1)*self.cols+x] != 0:
          barn_proof[x][y].prove_if(barn_proof[x][y-1])
        if y < self.rows-1 and self.board.cell[(y+1)*self.cols+x] != 0:
          barn_proof[x][y].prove_if(barn_proof[x][y+1])
        if x > 0 and self.board.cell[y*self.cols+x-1] != 0:
          barn_proof[x][y].prove_if(barn_proof[x-1][y])
        if x < self.cols-1 and self.board.cell[y*self.cols+x+1] != 0:
          barn_proof[x][y].prove_if(barn_proof[x+1][y])
    
    num_solutions = solve(quiet=True)
    solution = [
      [[utils.intify(i) for i in r] for r in h],
      [[utils.intify(i) for i in c] for c in v],
    ]
    #print(ph, pv)
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
