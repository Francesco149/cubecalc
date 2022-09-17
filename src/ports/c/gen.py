#!/usr/bin/env python3

import sys
from utils import enum_bits
sys.path.append("../../")
from common import *
from cubecalc import prime_chances, find_line_values
import itertools
import inspect
import pickle
from functools import reduce
from operator import or_
import json

from kms import cubes
from tms import event
from familiars import familiars

indent = 0

def p(x):
  global indent
  print("  " * indent + x)

class Block:
  def __init__(self, delim="{}"):
    self.delim = delim

  def __enter__(self):
    global indent
    if self.delim:
      p(self.delim[0])
    indent += 1

  def __exit__(self, exc_type, exc_val, exc_tb):
    global indent
    indent -= 1
    if self.delim:
      p(self.delim[1])

def BlockCol():
  return Block(["{", "};"])

def BlockComma():
  return Block(["{", "},"])

def IndentBlock():
  return Block(None)

# -------------------------------------------------------------------------------------------------
# bake the value ranges into a map of (maxlvl, cube_mask, category_mask, region_mask) -> lines

values = {}

def get_lval(lvals, level, tier, line):
  v = lvals[tier][line]
  if isinstance(v, list):
    try:
      for maxlvl, amt in v:
        if level <= maxlvl:
          return amt
    except:
      print(level, tier, line, v)
      raise
    raise RuntimeError(f"failed to find {Tier(tier).name} {Line(line).name} "+
        f"for level {level}: {v}")
  return v

try:
  with open("gen_find_line_values.py") as f:
    source = f.read()
except:
  source = ""

# this is a very inefficient way to run the values function for every combination of params and
# generate all the level ranges that have the same values/region/category etc
cursource = inspect.getsource(find_line_values)
if source != cursource:
  source = cursource
  NonSpecialCategory = [x for x in Category if x not in { LINE_CACHE, NAME, DEFAULT_CUBE }]

  # map params by values returned
  merge = {}
  for cube, category, region in itertools.product(Cube, NonSpecialCategory, Region):
    vals = find_line_values(cube, category, region)
    for level in range(301):
      valsmap = {
        tier: {
          line: get_lval(vals, level, tier, line) for line in vals[tier]
        } for tier in vals
      }
      k = json.dumps(valsmap, sort_keys=True, default=str)
      if k not in merge:
        merge[k] = (valsmap, [])
      merge[k] = (valsmap, merge[k][1] + [(level, cube, category, region)])

  for _, (valsmap, params) in merge.items():
    # group parameters by region
    regions = {}
    for level, cube, category, region in params:
      if region not in regions:
        regions[region] = []
      regions[region] += [(level, cube, category)]

    # generate a map of region_mask -> minlvl, maxlvl, cube_mask, category_mask
    # making sure to merge all overlapping ranges
    region_ranges = {}
    for k, v in regions.items():
      maxlvl = max([level for level, cube, category in v])
      minlvl = min([level for level, cube, category in v])
      cubemask = reduce(or_, [cube for level, cube, category in v])
      categorymask = reduce(or_, [category for level, cube, category in v])

      # see if we can merge with any existing range
      found = False
      for ok, (other_minlvl, other_maxlvl, other_cube, other_category) in region_ranges.items():
        if other_maxlvl == maxlvl and other_minlvl == minlvl:
          found = True
          break

      if found:
        # merge
        del region_ranges[ok]
        region_ranges[ok | k] = (
            minlvl,
            maxlvl,
            other_cube | cubemask,
            other_category | categorymask,
        )
      else:
        # new range
        region_ranges[k] = (minlvl, maxlvl, cube, category)

    # finally generate the values map
    for region, (_, maxlvl, cube, category) in region_ranges.items():
      values[(maxlvl, cube, category, region)] = valsmap

  with open("gen_find_line_values.pickle", "wb") as f:
    pickle.dump(values, f)

  with open("gen_find_line_values.py", "w") as f:
    f.write(source)
else:
  with open("gen_find_line_values.pickle", "rb") as f:
    values = pickle.load(f)

# -------------------------------------------------------------------------------------------------

p(f"/* generated by {sys.argv[0]} - don't edit, edit the script */")
p("#ifndef CUBECALC_GENERATED_H")
p("#define CUBECALC_GENERATED_H")
p("#include \"common.c\"")
p("#include \"utils.c\"")

p(f"void cubecalcGeneratedGlobalInit();")
p(f"void cubecalcGeneratedGlobalFree();")
maps = [ "primeChances", "kms", "tms", "fams" ]

for x in maps:
  p(f"extern Map* {x};");

p(f"extern int const valueGroupsMaxLevel[{len(values)}];")
p(f"extern int const valueGroupsCubeMask[{len(values)}];")
p(f"extern int const valueGroupsCategoryMask[{len(values)}];")
p(f"extern int const valueGroupsRegionMask[{len(values)}];")
p(f"extern Map* valueGroups[{len(values)}];")


lines_hi = [(x.name, (x >> 32) & 0xFFFFFFFF) for x in Line]
lines_lo = [(x.name, (x >>  0) & 0xFFFFFFFF) for x in Line]

p(f"extern int const allLinesHi[{len(lines_hi)}];")
p(f"extern int const allLinesLo[{len(lines_hi)}];")
p(f"extern char const* const allLineNames[{len(lines_hi)}];")

def enum(e):
  p(f"enum {e.__name__}")
  with BlockCol():
    for x in e:
      p(f"{x.name} = 0x{x.value:x},")

for x in [Cube, Tier, Category, Region]:
  enum(x)

for name, x in lines_hi:
  p(f"#define {name}_HI 0x{x:x}")

for name, x in lines_lo:
  p(f"#define {name}_LO 0x{x:x}")

masks = [x for x in LineMasks] + [x for x in LineVariants]

for name, x in [(x.name, (x >> 32) & 0xFFFFFFFF) for x in masks]:
  p(f"#define {name}_HI {enum_bits(Line, x, '_HI') or 0}")

for name, x in [(x.name, (x >>  0) & 0xFFFFFFFF) for x in masks]:
  p(f"#define {name}_LO ({enum_bits(Line, x, '_LO') or 0})")

p("#endif")
p("#if defined(CUBECALC_GENERATED_IMPLEMENTATION) && !defined(CUBECALC_GENERATED_UNIT)")
p("#define CUBECALC_GENERATED_UNIT")

for x in maps:
  p(f"Map* {x};");

def arr(x, ctyp, name="buf"):
  p(f"static const BufStatic({ctyp} const, {name},")
  with IndentBlock():
    for val in x:
      p(f"{val},")
  p(f");")

def arr_flag(x, e, suff="", name="buf"):
  p(f"static const BufStatic(int const, {name},")
  with IndentBlock():
    for val in x:
      s = enum_bits(e, val, suff) if val else "0"
      p(f"{s},")
  p(f");")

p(f"int const allLinesHi[{len(lines_hi)}] = ")
with BlockCol():
  for name, _ in lines_hi:
    p(f"{name}_HI,")

p(f"int const allLinesLo[{len(lines_hi)}] = ")
with BlockCol():
  for name, _ in lines_lo:
    p(f"{name}_LO,")

p(f"char const* const allLineNames[{len(lines_hi)}] = ")
with BlockCol():
  for name, _ in lines_lo:
    p(f"\"{name}\",")

init_funcs = []

def init_func(x):
  global init_funcs
  p(f"static void {x}()")
  init_funcs.append(x)

def container(t, d):
  p("static Container container =")
  with BlockCol():
    p(f".type = CONTAINER_{t.upper()},")
  p(f"container.data = {d};")

init_func("primeChancesInit")
with Block():
  p("primeChances = MapInit();")
  for cube, data in prime_chances.items():
    with Block():
      if isinstance(data, dict):
        p("Map* cube = MapInit();")
        for tier, x in data.items():
          with Block():
            arr(x, "float")
            p(f"MapSet(cube, {Tier(tier).name}, (void*)buf);")
        container("map", "cube")
      else:
        arr(data, "float")
        container("buf", "(void*)buf")
      p(f"MapSet(primeChances, {Cube(cube).name}, (void*)&container);")


def lines_map(name, x):
  p(f"{name} = MapInit();")
  for cube_mask, categories in x.items():
    with Block():
      p(f"Map* categories = MapInit();")
      for category_mask, tiers in categories.items():
        with Block():
          p(f"Map* tiers = MapInit();")
          for tier, linedata in tiers.items():
            with Block():
              lines = [x[0] for x in linedata]
              linesHi = [x & 0xFFFFFFFF00000000 if (x >> 32) & 0xFFFFFFFF else 0 for x in lines]
              linesLo = [x & 0x00000000FFFFFFFF if (x >>  0) & 0xFFFFFFFF else 0 for x in lines]
              arr_flag(linesHi, Line, "_HI", name="lineHi")
              arr_flag(linesLo, Line, "_LO", name="lineLo")
              arr([x[1] for x in linedata], "float", name="onein")
              # tcc can't figure out that these arrays are compile time const
              p("static LineData linedata;")
              p("linedata.onein = onein;")
              p("linedata.lineHi = lineHi;")
              p("linedata.lineLo = lineLo;")
              p(f"MapSet(tiers, {Tier(tier).name}, (void*)&linedata);")
          p(f"MapSet(categories, {enum_bits(Category, category_mask)}, tiers);")
        p(f"MapSet({name}, {enum_bits(Cube, cube_mask)}, categories);")


init_func("dataInit")
with Block():
  lines_map("kms", cubes)
  lines_map("tms", event)
  lines_map("fams", familiars)

p(f"void cubecalcGeneratedGlobalFree()")
with Block():
  for x in maps:
    p(f"{x}Free();");
  p(f"valueGroupsFree();");

p(f"int const valueGroupsMaxLevel[{len(values)}] = ")
with BlockCol():
  for k, v in values.items():
    level, cube, category, region = k
    p(f"{level},")

p(f"int const valueGroupsCubeMask[{len(values)}] = ")
with BlockCol():
  for k, v in values.items():
    level, cube, category, region = k
    p(f"{enum_bits(Cube, cube)},")

p(f"int const valueGroupsCategoryMask[{len(values)}] = ")
with BlockCol():
  for k, v in values.items():
    level, cube, category, region = k
    p(f"{enum_bits(Category, category)},")

p(f"int const valueGroupsRegionMask[{len(values)}] = ")
with BlockCol():
  for k, v in values.items():
    level, cube, category, region = k
    p(f"{enum_bits(Region, region)},")

p(f"Map* valueGroups[{len(values)}];")

LineHi = [x for x in Line if (x >> 32) & 0xFFFFFFFF]
LineLo = [x for x in Line if (x >>  0) & 0xFFFFFFFF]
init_func("valuesInit")
with Block():
  for i, (k, v) in enumerate(values.items()):
    level, cube, category, region = k
    for tier, values in v.items():
      lines_hi = []
      lines_lo = []
      for line, value in values.items():
        line_hi = " | ".join([f"{x.name}_HI" for x in LineHi if line & x])
        if not line_hi:
          line_hi = 0
        line_lo = " | ".join([f"{x.name}_LO" for x in LineLo if line & x])
        if not line_lo:
          line_lo = 0
        lines_hi.append(line_hi)
        lines_lo.append(line_lo)
      with Block():
        p(f"static const int linesHi[{len(values)}] = ")
        with BlockCol():
          for x in lines_hi:
            p(f"{x},")
        p(f"static const int linesLo[{len(values)}] = ")
        with BlockCol():
          for x in lines_lo:
            p(f"{x},")
        p(f"static const int vals[{len(values)}] = ")
        with BlockCol():
          for k, v in values.items():
            p(f"{v},")
        p(f"valueGroupsSet({i}, {tier}, {len(values)}, linesHi, linesLo, vals);")


p(f"void cubecalcGeneratedGlobalInit()")
with Block():
  [p(f"{x}();") for x in init_funcs]

p("#endif")
