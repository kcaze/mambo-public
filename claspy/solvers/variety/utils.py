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

# Require pred1 if and only if pred2.
def require_iff(pred1, pred2):
  require(~(pred1 ^ pred2))


# Returns two grids, one for horizontal edges and one for vertical edges.
# The paths are assumed to be drawn between the centers of squares in a w x h grid.
# hori[x][y] is the horizontal edge from the center of square (x,y) to (x+1,y).
# vert[x][y] is the vertical edge from the center of square (x,y) to (x,y+1).
U,D,L,R = (1,2,1,2)
def path(w, h):
  return (
    [[IntVar() for y in range(h)] for x in range(w-1)],
    [[IntVar() for y in range(h-1)] for x in range(w)]
  )

# For undirected edges, 0 = no edge and 1 = edge.
def require_undirected(h,v):
  for r in h + v:
    for c in r:
      require((c == 0) | (c == 1))

# For directed edges, 0 = no edge, L = U = 1 is an edge directed left or up, and
# R = D = 2 is an edge directed right or down.
def require_directed(h,v):
  for r in h + v:
    for c in r:
      require((c == 0) | (c == 1) | (c == 2))

# Returns the edges coming out of the center of square (x,y).
# The edges are returned in order U, D, L, R.
# h and v are the horizontal and vertical edges.
def edges(h,v,x,y,default=lambda: 0):
  width = len(v)
  height = len(h[0])
  return [
    v[x][y-1] if y > 0 else default(),
    v[x][y] if y < height-1 else default(),
    h[x-1][y] if x > 0 else default(),
    h[x][y] if x < width-1 else default(),
  ]

# Require's that the degree at the center of square (x,y) is 0, 1, or 2.
# h and v are the horizontal and vertical edges.
def require_no_self_intersection_undirected(h,v,x,y):
  s = sum_vars(edges(h,v,x,y))
  require((s == 0) | (s == 1) | (s == 2))

# Require's that the degree at the center of square (x,y) is 0 or 2.
# h and v are the horizontal and vertical edges.
def require_part_of_simple_loop_undirected(h,v,x,y):
  s = sum_vars(edges(h,v,x,y))
  require((s == 0) | (s == 2))

# Require's that the degree at the center of square (x,y) is 0, 2, or 4.
# h and v are the horizontal and vertical edges.
def require_part_of_loop_undirected(h,v,x,y):
  s = sum_vars(edges(h,v,x,y))
  require((s == 0) | (s == 2) | (s == 4))

# Require's that there is a path from the center of square (x1, y1) to the center of
# square (x2, y2).
# h and v are the horizontal and vertical edges.
def require_two_points_connected_undirected(h,v,x1,y1,x2,y2):
  width = len(v)
  height = len(h[0])

  connected = [[Atom() for y in range(height)] for x in range(width)]
  connected[x1][y1].prove_if(True)

  for x in range(width):
    for y in range(height):
      u,d,l,r = edges(h,v,x,y)
      if y > 0:
        connected[x][y].prove_if(u & connected[x][y-1])
      if y < height-1:
        connected[x][y].prove_if(d & connected[x][y+1])
      if x > 0:
        connected[x][y].prove_if(l & connected[x-1][y])
      if x < width-1:
        connected[x][y].prove_if(r & connected[x+1][y])
  require(connected[x2][y2])

# Returns an array of BoolVar's. Use sum_bools/at_least/at_most to place constraints
# on the number of components.
# If there are path intersections, we assume the 2 intersecting path pieces have to
# go straight at the intersection (i.e. there cannot be an intersection where the paths
# bend as an L and a 7).
def number_components(h,v):
  width = len(v)
  height = len(h[0])
  H = [[IntVar() for y in range(height)] for x in range(width-1)]
  V = [[IntVar() for y in range(height-1)] for x in range(width)]
  proofH = [[Atom() for y in range(height)] for x in range(width-1)]
  proofV = [[Atom() for y in range(height-1)] for x in range(width)]
  ret = []
  for x in range(width):
    for y in range(height):
      e = edges(h,v,x,y)
      E = edges(H,V,x,y)
      p = edges(proofH,proofV,x,y,lambda: Atom())

      # degree 4
      C = True
      for i in range(4):
        C = C & (e[i] != 0)
      require(cond(C, (E[0] == E[1]) & (E[2] == E[3]), True))
      p[0].prove_if(C & p[1])
      p[1].prove_if(C & p[0])
      p[2].prove_if(C & p[3])
      p[3].prove_if(C & p[2])
      # all the degree 2 cases
      for i in range(4):
        for j in range(i+1, 4):
          C = True
          for c in range(4):
            C = C & (e[c] != 0 if c == i or c == j else e[c] == 0)
          require(cond(C, E[i] == E[j], True))
          p[i].prove_if(C & p[j])
          p[j].prove_if(C & p[i])

      for i in range(4):
        require(cond(e[i] != 0, p[i], True))
      require(cond(e[1] == 0, E[1] == 0, E[1] <= x+y*width+1))
      compRoot = E[1] == x+y*width+1
      p[1].prove_if(compRoot)
      ret.append(compRoot)

      require(cond(e[3] == 0, E[3] == 0, E[3] <= width*height + x+y*width+1))
      compRoot = E[3] == width*height + x+y*width+1
      p[3].prove_if(compRoot)
      ret.append(compRoot)
  return (ret, H, V)

# Returns an array of BoolVar's representing whether a square contains the end of a path.
# Use sum_bools/at_least/at_most to place constraints on the number of components.
def number_ends(h,v):
  width = len(v)
  height = len(h[0])
  ret = []
  for x in range(width):
    for y in range(height):
      u,d,l,r = edges(h,v,x,y)
      ret.append(sum_bools(1, [u != 0, d != 0, l != 0, r != 0]))
  return ret

# Require's that the in-degree and out-degree at the center of square (x,y) is at most 1
# h and v are the horizontal and vertical edges.
def require_no_self_intersection_directed(h,v,x,y):
  u,d,l,r = edges(h,v,x,y)
  in_edges = [u == D, d == U, l == R, r == L]
  out_edges = [u == U, d == D, l == L, r == R]
  require(sum_bools(0, in_edges) | sum_bools(1, in_edges))
  require(sum_bools(0, out_edges) | sum_bools(1, out_edges))

# Require's that the in-degree and out-degree at the center of square (x,y) is either
# both 0 or both 1
# h and v are the horizontal and vertical edges.
def require_part_of_simple_loop_directed(h,v,x,y):
  u,d,l,r = edges(h,v,x,y)
  in_edges = [u == D, d == U, l == R, r == L]
  out_edges = [u == U, d == D, l == L, r == R]
  require(
    (sum_bools(0, in_edges) & sum_bools(0, out_edges))
    | (sum_bools(1, in_edges) & sum_bools(1, out_edges))
  )

# Require's that the in-degree and out-degree at the center of square (x,y) are
# both 0, both 1, or both 2
# h and v are the horizontal and vertical edges.
def require_part_of_loop_undirected(h,v,x,y):
  u,d,l,r = edges(h,v,x,y)
  in_edges = [u == D, d == U, l == R, r == L]
  out_edges = [u == U, d == D, l == L, r == R]
  require(
    (sum_bools(0, in_edges) & sum_bools(0, out_edges))
    | (sum_bools(1, in_edges) & sum_bools(1, out_edges))
    | (sum_bools(2, in_edges) & sum_bools(2, out_edges))
  )

# Require's that there is a directed path from the center of square (x1, y1) to the
# center of square (x2, y2).
# h and v are the horizontal and vertical edges.
def require_two_points_connected_directed(h,v,x1,y1,x2,y2):
  width = len(v)
  height = len(h[0])

  connected = [[Atom() for y in range(height)] for x in range(width)]
  connected[x1][y1].prove_if(True)

  for x in range(width):
    for y in range(height):
      (u,d,l,r) = edges(h,v,x,y)
      if y > 0:
        connected[x][y].prove_if((u == D) & connected[x][y-1])
      if y < height-1:
        connected[x][y].prove_if((d == U) & connected[x][y+1])
      if x > 0:
        connected[x][y].prove_if((l == R) & connected[x-1][y])
      if x < width-1:
        connected[x][y].prove_if((r == L) & connected[x+1][y])
  require(connected[x2][y2])


# Require that the edges form a single closed loop, a common requirement in puzzles like slitherlink,
# masyu, and yajilin.
# h is a list of horizontal edges. It should be a list of height + 1 lists of width BoolVar's.
# v is a list of vertical edges. It should be a list of width + 1 lists of height BoolVar's.
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
