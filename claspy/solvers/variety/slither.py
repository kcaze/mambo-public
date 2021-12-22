from claspy import *
from _base_ import Base
import utils

class Slither(Base):
  def _solve(self):
    # Use 8 bits for efficiency
    set_bits(8)

    horizontalFences = utils.makeGrid(self.cols, self.rows+1, lambda: BoolVar())
    verticalFences = utils.makeGrid(self.rows, self.cols+1, lambda: BoolVar())

    utils.require_single_closed_loop_v2(horizontalFences, verticalFences)
   
    # Require numbers are surrounded by that many fences.
    for y in range(self.rows):
      for x in range(self.cols):
        if self.board.getCell(x,y) is not None:
          edges = [
            horizontalFences[y][x],
            horizontalFences[y+1][x],
            verticalFences[x][y],
            verticalFences[x+1][y]
          ]
          require(sum_bools(self.board.getCell(x,y), edges))
    
    num_solutions = solve(quiet=True)
    solution = {
      'horizontalFences': [[utils.intify(x) for x in r] for r in horizontalFences],
      'verticalFences': [[utils.intify(x) for x in r] for r in verticalFences],
    }
    return (num_solutions, solution)

  def decode(self):
    self.decode4Cell()
