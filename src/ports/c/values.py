#!/usr/bin/env python3

import sys
import pickle
from utils import enum_bits

sys.path.append("../../")
from common import *

with open("gen_find_line_values.pickle", "rb") as f:
  values = pickle.load(f)

for (level, cube, category, region), v in values.items():
  print("=" * 80)
  print(f"Level: {level}")
  print(f"Cubes: {enum_bits(Cube, cube)}")
  print(f"Categories: {enum_bits(Category, category)}")
  print(f"Regions: {enum_bits(Region, region)}")
  for tier, lines in v.items():
    print("")
    print(f":: {tier.name}")
    for line, value in lines.items():
      print(f"{enum_bits(Line, line)} -> {value}")
