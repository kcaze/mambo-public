from importlib import import_module
from os import path
from ._base_ import parseURL
from .solvers import SOLVERS

solvers = {}

directory = path.dirname(__file__)
for name in SOLVERS:
  solvers[name] = import_module("."+name, __name__).Solver

def getPid(url):
  return parseURL(url)[0]
