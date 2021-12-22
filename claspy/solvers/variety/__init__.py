from ._base_ import parseURL

from . import akari
from . import building
from . import fillomino
from . import hashi
from . import mashu
from . import nurikabe
from . import slither
from . import starbattle
from . import sudoku
from . import tapa
from . import yajilin

solvers = {
  'akari': akari.Akari,
  'building': building.Building,
  'fillomino': fillomino.Fillomino,
  'hashi': hashi.Hashi,
  'mashu': mashu.Mashu,
  'nurikabe': nurikabe.Nurikabe,
  'slither': slither.Slither,
  'starbattle': starbattle.Starbattle,
  'sudoku': sudoku.Sudoku,
  'tapa': tapa.Tapa,
  'yajilin': yajilin.Yajilin,
}

def getPid(url):
  return parseURL(url)[0]
