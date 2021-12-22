from _base_ import parseURL

import akari
import building
import fillomino
import hashi
import mashu
import nurikabe
import slither
import starbattle
import sudoku
import tapa
import yajilin

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
