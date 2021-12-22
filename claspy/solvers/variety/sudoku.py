from claspy import *
from _base_ import Base
import utils

class Sudoku(Base):
  def _solve(self):
    ans = utils.makeGrid(9,9,lambda: IntVar(1,9))

    for i in range(9):
      require_all_diff(ans[i])
      require_all_diff([ans[j][i] for j in range(9)])
      require_all_diff([ans[j/3+i/3*3][j%3+i%3*3] for j in range(9)])

    for y in range(9):
      for x in range(9):
        if self.board.getCell(x,y) is not None:
          require(ans[y][x] == self.board.getCell(x,y))

    num_solutions = solve(quiet=True)
    solution = [utils.intify(ans[i/9][i%9]) for i in range(81)]
    return (num_solutions, solution)

  def decode(self):
    self.decodeNumber16()
