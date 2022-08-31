from common import *
from functools import reduce
from operator import or_, add
import sys

def percent(lines):
  for k in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]:
    if k in lines:
      lines[k] = [[x[0], 1/x[1]*100] for x in lines[k]]
  return lines


empty_tiers = {x: [] for x in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]}

def find_probabilities(data, cubes_mask, categories_mask):
  """
  find all the dicts that match both the desired cubes and categories and merge them
  data format is assumed to be the same as tms.py
  """
  cubedatas = [v for k, v in data.items() if k & cubes_mask]
  probabilities = reduce(add, [[v for k, v in x.items() if k & categories_mask] for x in cubedatas])
  info = {
    NAME: category_name(categories_mask),
    DEFAULT_CUBE: MEISTER if cubes_mask & NONCASH_MAIN else [x for x in Cube if x & cubes_mask],
  }
  return empty_tiers | info | reduce(or_, probabilities, {})


skip = lambda x: next(nonempty(x), None)

def nonempty(f):
  while True:
    l = f.readline()
    if not l:
      break
    s = l.strip()
    if s:
      yield s

def line_name(l):
  if l in Line:
    return Line(l).name
  if l in LineVariants:
    return LineVariants(l).name
  if l in LineMasks:
    return LineMasks(l).name
  return " | ".join([Line(x).name for x in Line if l & x])

def validate_probabilities(data):
  """raises an error if data is not valid for cube_calc"""
  for tier, lines in data.items():
    if tier not in Tier:
      continue
    seen = set()
    for l in lines:
      if l[0] is None:
        raise RuntimeError(f"found None stat at tier {Tier(tier).name}")
      if l[0] in seen:
        raise RuntimeError(f"found duplicate stat {line_name(l[0])} at tier {Tier(tier).name}")
      seen.add(l[0])

def find_validate_probabilities(data, cubes_mask, categories_mask):
  res = find_probabilities(data, cubes_mask, categories_mask)
  validate_probabilities(res)
  return res

def merge_duplicate_lines(cubedata):
  """finds duplicate stats (same line, prob) for each tier of cubedata and sums their probability"""
  for tier, tierdata in cubedata.items():
    counts = {}

    def unique_stats():
      for x in tierdata:
        stat = x[0]
        if stat not in counts:
          counts[stat] = 1
          yield x
        else:
          counts[stat] += 1

    cubedata[tier] = list(unique_stats())

    def merged_stats():
      for x in cubedata[tier]:
        stat = x[0]
        percent = float(x[1])
        if counts[stat] > 1:
          new_percent = percent * counts[stat]
          sys.stderr.write(f"{tier.name}: merging duplicate line " +
              f"{stat.name} from {percent}% to {new_percent}%\n")
          percent = new_percent
        yield [stat, percent]

    cubedata[tier] = list(merged_stats())
