from common import *
from functools import reduce
from operator import or_, add

def percent(lines):
  for k in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]:
    if k in lines:
      lines[k] = [[x[0], 1/x[1]*100] for x in lines[k]]
  return lines


empty_tiers = {x: [] for x in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]}

def find_probabilities(data, cubes_mask, categories_mask):
  """
  find all the dicts that match both the desired cubes and categories and merge them
  data format is assumed to be the same as data/tms/__init__.py
  """
  cubedatas = [v for k, v in data.items() if k & cubes_mask]
  probabilities = reduce(add, [[v for k, v in x.items() if k & categories_mask] for x in cubedatas])
  info = {
    NAME: category_name(categories_mask),
    DEFAULT_CUBE: MEISTER if cubes_mask & NONCASH_MAIN else [x for x in Cube if x & cubes_mask],
  }
  return empty_tiers | info | reduce(or_, probabilities, {})
