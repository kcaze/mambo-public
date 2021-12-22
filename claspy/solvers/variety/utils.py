from claspy import *

def include(ca, bottom, up):
    return bottom <= ca and ca <= up

def idx(arr, y, x, default):
  if y < 0 or y >= len(arr):
    return default
  if x < 0 or x >= len(arr[y]):
    return default
  return arr[y][x]

def makeGrid(w, h, fn):
  return [[fn() for i in range(w)] for j in range(h)]

# Convert an IntVar() to an int.
def intify(intvar):
  return int(str(intvar))

# Require that the edges form a single closed loop, a common requirement in puzzles like slitherlink,
# masyu, and yajilin.
# h is a list of horizontal edges. It should be a list of height + 1 lists of width BoolVar's.
# v is a list of vertical edges. It should be a list of width + 1 lists of height BoolVar's.
def require_single_closed_loop(h, v):
  width = len(v)-1
  height = len(h)-1
  # Require that each intersection point has either 2 or 0 edges connecting to it.
  # This constraint guarantees that the edges form closed loop(s) that don't self-intersect.
  for y in range(height+1):
    for x in range(width+1):
      edges = [
        h[y][x-1] if x > 0 else False,
        h[y][x] if x < width else False,
        v[x][y-1] if y > 0 else False,
        v[x][y] if y < height else False,
      ]
      require(sum_bools(2, edges) | sum_bools(0, edges))
    
  # To prove that the edges form a single loop, we compute the winding number.
  # To compute the winding number efficiently, we need to first determine which squares lie
  # outside and which lie inside the loop. `outside` is a list of atoms for this purpose.
  # A 1 square thick border is added to the grid which is guaranteed to be part of the outside.
  # The outside is computed with a flood-fill through prove_if's
  outside = [[True if i == 0 or i == width+1 or j == 0 or j == height+1 else Atom() for i in range(width+2)] for j in range(height+2)]
  for y in range(1,height+1):
   for x in range(1, width+1):
     if x-1 >= 0 and y-1 < height and y-1 >= 0:
       outside[y][x].prove_if(outside[y][x-1] & ~v[x-1][y-1])
     if x < width+1 and y-1 < height and y-1 >= 0:
       outside[y][x].prove_if(outside[y][x+1] & ~v[x][y-1])
     if y-1 >= 0 and x-1 < width and x-1 >= 0:
       outside[y][x].prove_if(outside[y-1][x] & ~h[y-1][x-1])
     if y < height+1 and x-1 < width and x-1 >= 0:
       outside[y][x].prove_if(outside[y+1][x] & ~h[y][x-1])
   
  # Requires that each fence has one side outside and one not outside according to the flood fill.
  # This ensures the outside is one connected region.
  for y in range(height+1):
    for x in range(width+1):
      if x < width:
        require(cond(h[y][x], outside[y][x+1] ^ outside[y+1][x+1], True))
      if y < height:
        require(cond(v[x][y], outside[y+1][x] ^ outside[y+1][x+1], True))
    
  # Require winding number is 1 so that the inside is one connected region.
  # We compute the number of clockwise turns and the number of counterclockwise turns and
  # require that their difference is exactly 4 (since 4 * 90 degree turns = 360 degrees = 1 wind).
  cw = [[BoolVar() for i in range(width+1)] for j in range(height+1)] 
  ccw = [[BoolVar() for i in range(width+1)] for j in range(height+1)] 
  for y in range(height+1):
    for x in range(width+1):
      edges = [
        h[y][x-1] if x > 0 else False,
        v[x][y-1] if y > 0 else False,
        h[y][x] if x < width else False,
        v[x][y] if y < height else False,
      ]
      require(cw[y][x] == ((edges[0] & ((~outside[y][x] & edges[1]) | (~outside[y+1][x] & edges[3]))) | (edges[2] & ((~outside[y][x+1] & edges[1]) | (~outside[y+1][x+1] & edges[3])))))
      require(ccw[y][x] == ((edges[0] & ((outside[y][x] & edges[1]) | (outside[y+1][x] & edges[3]))) | (edges[2] & ((outside[y][x+1] & edges[1]) | (outside[y+1][x+1] & edges[3])))))
  require(sum_vars(sum(cw,[])) - sum_vars(sum(ccw,[])) == 4)

def require_single_closed_loop_v2(h, v):
  width = len(v)-1
  height = len(h)-1
  # Require that each intersection point has either 2 or 0 edges connecting to it.
  # This constraint guarantees that the edges form closed loop(s) that don't self-intersect.
  for y in range(height+1):
    for x in range(width+1):
      edges = [
        h[y][x-1] if x > 0 else False,
        h[y][x] if x < width else False,
        v[x][y-1] if y > 0 else False,
        v[x][y] if y < height else False,
      ]
      require(sum_bools(2, edges) | sum_bools(0, edges))

  # Atom's for proving connectivity
  connectedH = makeGrid(len(h[0]), len(h), lambda: Atom())
  connectedV = makeGrid(len(v[0]), len(v), lambda: Atom())
  for y in range(len(h)):
    for x in range(len(h[0])):
      H = connectedH[y][x]
      H.prove_if(h[y][x] &
        (idx(connectedH, y, x-1, False) |
        idx(connectedH, y, x+1, False) |
        idx(connectedV, x, y, False) |
        idx(connectedV, x, y-1, False) |
        idx(connectedV, x+1, y, False) |
        idx(connectedV, x+1, y-1, False)))
      require(h[y][x] == H)
  for x in range(len(v)):
    for y in range(len(v[0])):
      V = connectedV[x][y]
      V.prove_if(v[x][y] &
        (idx(connectedV, x, y-1, False) |
        idx(connectedV, x, y+1, False) |
        idx(connectedH, y, x, False) |
        idx(connectedH, y, x-1, False) |
        idx(connectedH, y+1, x, False) |
        idx(connectedH, y+1, x-1, False))) 
      require(v[x][y] == V)
  # Use the smallest idx in connectedH to start the proof chain
  startingConnectedHIdx = IntVar(0, len(h[0])*len(h))
  for y in range(len(h)):
    for x in range(len(h[0])):
      i = y*len(h[0])+x
      require(cond(h[y][x], startingConnectedHIdx <= i, True))
      connectedH[y][x].prove_if(h[y][x] & (startingConnectedHIdx == i))
  return connectedH
