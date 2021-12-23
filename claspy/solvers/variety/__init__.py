from importlib import import_module
from os import path
from ._base_ import parseURL

solvers = {}

directory = path.dirname(__file__)
with open(path.join(directory, "solvers.txt"), "r") as f:
  for line in f.readlines():
    name = line.strip()
    solvers[name] = import_module("."+name, __name__).Solver

def getPid(url):
  return parseURL(url)[0]
