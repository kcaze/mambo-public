import math
import re
import utils

class Board:
  def __init__(self, cols, rows):
    self.cell = initCell(cols, rows)
    self.excell = initExcell(cols, rows)
    self.border = initBorder(cols, rows)
    self.cols = cols
    self.rows = rows
    
  def getCell(self, x, y):
    return self.cell[y*self.cols + x]

class Base:
  NO_SOLUTIONS = 0
  UNIQUE_SOLUTION = 1
  MULTIPLE_SOLUTIONS = 2

  def __init__(self, url):
    self.decodeURL(url)
    self.decode()
  
  def solve(self):
    (num_solutions, solution) = self._solve()
    solution_type = Base.NO_SOLUTIONS if num_solutions == 0 else Base.UNIQUE_SOLUTION if num_solutions == 1 else Base.MULTIPLE_SOLUTIONS
    return {
      'solutionType': solution_type,
      'solution': solution
    }

  def decodeURL(self, url):
      (self.pid, self.cols, self.rows, self.body, self.pflag) = parseURL(url)
      self.board = Board(self.cols, self.rows)

  def decode4Cell(self):
    c = 0
    i = 0
    bstr = self.body
    bd = self.board
    for i in range(len(bstr)):
      ca = bstr[i]
      if utils.include(ca, "0", "4"):
        bd.cell[c] = int(ca, 16)
      elif utils.include(ca, "5", "9"):
        bd.cell[c] = int(ca, 16) - 5
        c += 1
      elif utils.include(ca, "a", "e"):
        bd.cell[c] = int(ca,16)-10
        c += 2
      elif utils.include(ca, "g", "z"):
        c += int(ca, 36) - 16
      elif ca == ".":
        bd.cell[c] = -2
      c += 1
      if c >= len(bd.cell):
        break
    self.body = self.body[i+1:]

  def decodeNumber16(self):
      bstr = self.body
      c = 0
      i = 0
      while i < len(bstr):
          ca = bstr[i]
          if utils.include(ca, "0", "9") or utils.include(ca, "a", "f"):
              self.board.cell[c] = int(ca, 16)
          elif ca == "-":
              self.board.cell[c] = int(bstr[i+1:i+1+2], 16)
              i += 2
          elif ca == "+":
              self.board.cell[c] = int(bstr[i+1:i+1+3], 16)
              i += 3
          elif ca == "=":
              self.board.cell[c] = int(bstr[i+1:i+1+3], 16) + 4096
              i += 3
          elif ca == "%":
              self.board.cell[c] = int(bstr[i+1:i+1+3], 16) + 8192
              i += 3
          elif ca == ".":
              self.board.cell[c] = -2
          elif ca >= "g" and ca <= "z":
              c += int(ca,36) - 16
          c += 1
          if c >= len(self.board.cell):
              break
          i += 1
      self.body = self.body[i+1:]

  def decodeBorder(self):
    pos1 = 0
    pos2 = 0
    bstr = self.body
    twi = [16,8,4,2,1]
    bd = self.board
    if bstr != "":
      pos1 = min(((self.cols-1)*self.rows+4)/5, len(bstr))
      pos2 = min((self.cols*(self.rows-1)+4)/5 + pos1, len(bstr))
    id_ = 0
    for i in range(pos1):
      ca = int(bstr[i], 32)
      for w in range(5):
        if id_ < (self.cols-1)*self.rows:
          self.board.border[1][id_ / (self.cols-1)][id_ % (self.cols-1)] = 1 if ca & twi[w] != 0 else 0
          id_ += 1
    id_ = 0
    for i in range(pos1, pos2):
      ca = int(bstr[i], 32)
      for w in range(5):
        if id_ < self.cols*(self.rows-1):
          self.board.border[0][id_ / self.rows][id_ % self.rows] = 1 if ca & twi[w] != 0 else 0
          id_ += 1
    self.body = self.body[pos2:]

  def decodeArrowNumber16(self):
    c = 0
    i = 0
    bstr = self.body
    while i < len(bstr):
      ca = bstr[i]
      if utils.include(ca, "0", "4"):
        ca1 = bstr[i+1]
        self.board.cell[c] = (int(ca,16), int(ca1,16) if ca1 != "." else -2)
        i += 1
      elif utils.include(ca, "5", "9"):
        self.board.cell[c] = (int(ca,16) - 5, int(bstr[i+1:i+1+2],16))
        i += 2
      elif ca == "-":
        self.board.cell[c] = (int(bstr[i+1:i+1+1],16), int(bstr[i+2:i+2+3],16))
        i += 4
      elif ca >= "a" and ca <= "z":
        c += int(ca,36)-10
      c += 1
      if c >= self.rows*self.cols:
        break
      i += 1
    self.body = bstr[i+1:]
      

  def decodeCircle(self):
    bstr = self.body
    c = 0
    tri = [9,3,1]
    pos = min((self.cols*self.rows+2)/3, len(bstr))
    for i in range(pos):
      ca = int(bstr[i],27)
      for w in range(3):
        val = (ca/tri[w])%3
        if val > 0:
          self.board.cell[c] = val
        c += 1
    self.body = self.body[pos:]

def initCell(cols, rows):
    return [None for i in range(cols*rows)]

def initExcell(cols, rows):
    return [None for i in range(2*cols + 2*rows)]

def initBorder(cols, rows):
    horizontals = [[False for c in range(cols)] for r in range(rows-1)]
    verticals = [[False for r in range(cols-1)] for c in range(rows)]
    return (horizontals, verticals)

def parseURL(url):
    # Translation of parse() in parser.js
    qs = url.find("/", url.find("?"))
    pid = url[url.find("?")+1:qs]
    qdata = url[qs+1:]
    inp = qdata.split("/")
    if inp[0] != "" and not math.isnan(int(inp[0])):
        inp.insert(0, "")
    pflag = inp.pop(0)
    cols = int(inp.pop(0))
    rows = int(inp.pop(0))
    if inp[-1] == "":
        inp.pop()
    body = "/".join(inp)
    if pid == 'ichimaga':
        if "m" in pflag: pid = "ichimagam"
        elif "x" in pflag: pid = "ichimagax"
    elif pid == "icelom":
        if "a" not in pflag: pid = "icelom2"
    elif pid == "pipelink":
        if re.match('[0-9]', body): pid = 'pipelinkr'
    elif pid == "bonsan":
        if "c" not in pflag:
            col = cols
            row = rows
            if re.match('[^0]', body[0:((col-1)*row+4)/5 + (col*(row-1)+4)/5]):
                pid = 'heyabon'
    elif pid == 'kramma':
        if 'c' not in pflag:
            _len = (cols - 1) * (rows - 1)
            cc = 0
            for i in range(len(body)):
                ca = body[i]
                if re.match('\w', ca):
                    cc += int(ca, 36)
                    if (cc < len):
                        pid = 'kramman'
                        break
                elif ca == '.':
                    cc += 36
                if cc >= len:
                    break
    return (pid, cols, rows, body, pflag)
