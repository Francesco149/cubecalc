#!/usr/bin/env python3

from functools import reduce, partial
from operator import mul, or_, and_, add
import numpy as np
from enum import IntEnum, IntFlag, auto
from collections import namedtuple

disclaimer = """
even though the numbers look reasonable, I cannot guarantee that the math here
is correct. this is a calculator I made for myself and you should never
blindly trust anything like this. before you gamble your time and/or money,
double check the math yourself

I also make a few assumptions that might not be true but we just don't know
because GMS hasn't released any official data:
  - that line rates are the same as KMS
  - that line rates for TMS cubes like violet, uni are the same as TMS
  - that prime chance for violets on strategywiki applies to GMS
    (it's lower than TMS)

the assumptions are reasonable in my opinion but we just don't know for sure

you can check line probabilities in the source and see where I got them from

NOTE: for simplicity, all the values use lvl<160 lines, so for example
      30% att means 12 9 9 and it's the same as 33% on a lvl 160+ item
NOTE: for cases where the tier is lower than the max tier of the cube
      (such as red cubes on unique) it's assumed that you won't tier up
"""

def global_enum(enum):
  globals().update(enum.__members__)
  return enum

@global_enum
class Line(IntFlag):
  LINE_NULL = 0
  BOSS_30 = auto()
  BOSS_35 = auto()
  BOSS_40 = auto()
  BOSS = BOSS_30 | BOSS_35 | BOSS_40
  IED_30 = auto()
  IED_35 = auto()
  IED_40 = auto()
  IED = IED_30 | IED_35 | IED_40
  ATT = auto()
  ANY = auto()
  MAINSTAT = auto()
  ALLSTAT = auto()
  STAT = MAINSTAT | ALLSTAT
  HP = auto()
  COOLDOWN_1 = auto()
  COOLDOWN_2 = auto()
  COOLDOWN = COOLDOWN_1 | COOLDOWN_2
  CRITDMG = auto()
  MESO = auto()
  DROP = auto()

  LINE_LAST = auto()

  # special keys for matching lines
  LINES = auto() # match by number of lines and what lines are allowed

@global_enum
class Tier(IntEnum):
  TIER_NULL = auto()
  COMMON = auto()
  RARE = auto()
  EPIC = auto()
  UNIQUE = auto()
  LEGENDARY = auto()

  TIER_LAST = auto()
  TIER_DEFAULT = LEGENDARY

@global_enum
class Cube(IntEnum):
  CUBE_NULL = auto()
  RED = auto()
  MEISTER = auto()
  MASTER = auto()
  OCCULT = auto()
  BLACK = auto()
  VIOLET = auto()
  EQUALITY = auto()
  BONUS = auto()
  UNI = auto()

  CUBE_LAST = auto()

tier_limits = {
  OCCULT: EPIC,
  MASTER: UNIQUE,
}

def debug_print_combos(good, exit=True):
  a = np.dstack((good.types, good.values, good.onein, good.is_prime)).tolist()
  a = [[[Line(c[0]), c[1], c[2], c[3]] for c in x] for x in a]
  from pprint import pprint
  pprint(a)
  if exit:
    import sys
    sys.exit(0)

COMBOS = "combos"
COMBOS_VIOLET = "combos (violet)"
NAME = "name"
DEFAULT_CUBE = "default cube"

# official KMS probabilities:
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/red
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/black
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/strange
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/master
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/artisan

# strategywiki page which converts the KMS probabilities in a format that's easier to work with
# since the official probabilities gives you different probabilities for 1st, 2nd, 3rd line
# pre-adjusted for prime chance instead of just giving the base line chance + the prime chance
#   https://strategywiki.org/wiki/MapleStory/Potential_System

# TMS violet prime chance from the strategywiki page

prime_chances = {
  RED: [1, 0.1, 0.01],
  BLACK: [1, 0.2, 0.05],
  VIOLET: [1, 0.1, 0.01, 0.01, 0.1, 0.01],
  EQUALITY: [1, 1, 1],
  BONUS: {
    RARE: [1] + [1.0/51]*2,
    EPIC: [1] + [1.0/21]*2,
    UNIQUE: [1] + [1.0/51]*2,
    LEGENDARY: [1] + [0.004975]*2,
  },
  OCCULT: {
    RARE: [1] + [1.0/1001]*2,
    EPIC: [1] + [1.0/101]*2,
  },
  MASTER: {
    RARE: [1] + [1.0/6]*2,
    EPIC: [1] + [1.0/21]*2,
    UNIQUE: [1] + [1.0/84.3333]*2,
  },
  MEISTER: {
    RARE: [1] + [1.0/6]*2,
    EPIC: [1] + [1.0/12.5008]*2,
    UNIQUE: [1] + [1.0/58.9666]*2,
    LEGENDARY: [1] + [0.001996]*2,
  },
  UNI: [0.15],
}

LINE_TYPE = 0
LINE_ONEIN = 1

weapon = {
  NAME: "weapon",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [BOSS_30, 14.3333],
    [IED_30, 14.3333],
    [ATT, 14.3333],
  ],

  LEGENDARY: [
    [BOSS_40, 20.5],
    [BOSS_35, 20.5],
    [BOSS_30, 20.5],
    [IED_40, 20.5],
    [IED_35, 20.5],
    [ATT, 20.5],
  ],

}

weapon_noncash = {
  NAME: "weapon",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [ATT, 57],
  ],

  EPIC: [
    [ATT, 26],
  ],

  UNIQUE: [
    [BOSS_30, 15],
    [IED_30, 15],
    [ATT, 15],
  ],

  LEGENDARY: [
    [BOSS_40, 36],
    [BOSS_35, 18],
    [BOSS_30, 18],
    [IED_40, 36],
    [IED_35, 18],
    [ATT, 18],
  ],

}

secondary = {
  NAME: "secondary",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [BOSS_30, 17.0],
    [IED_30, 17.0],
    [ATT, 17.0],
  ],

  LEGENDARY: [
    [BOSS_40, 23.5],
    [BOSS_35, 23.5],
    [BOSS_30, 23.5],
    [IED_40, 23.5],
    [IED_35, 23.5],
    [ATT, 23.5],
  ],

}

secondary_noncash = {
  NAME: "secondary",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [ATT, 57],
  ],

  EPIC: [
    [ATT, 35],
  ],

  UNIQUE: [
    [BOSS_30, 21],
    [IED_30, 21],
    [ATT, 21],
  ],

  LEGENDARY: [
    [BOSS_40, 24],
    [BOSS_35, 24],
    [BOSS_30, 48],
    [IED_40, 48],
    [IED_35, 24],
    [ATT, 24],
  ],

}

emblem = {
  NAME: "emblem",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [IED_30, 13.3333],
    [ATT, 13.3333],
  ],

  LEGENDARY: [
    [IED_40, 17.5],
    [IED_35, 17.5],
    [ATT, 17.5],
  ],

}

emblem_noncash = {
  NAME: "emblem",
  DEFAULT_CUBE: MEISTER,

  RARE: [
    [ATT, 57],
  ],

  EPIC: [
    [ATT, 26],
  ],

  UNIQUE: [
    [IED_30, 14],
    [ATT, 14],
  ],

  LEGENDARY: [
    [IED_40, 15.5],
    [IED_35, 31],
    [ATT, 15.5],
  ],

}

weapon_bonus = {
  NAME: "weapon",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 21.5],
  ],

  LEGENDARY: [
    [ATT, 19.5],
  ],

}

secondary_bonus = {
  NAME: "secondary",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 21.5],
  ],

  LEGENDARY: [
    [ATT, 20.5],
  ],

}

emblem_bonus = {
  NAME: "emblem",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 21],
  ],

  LEGENDARY: [
    [ATT, 19],
  ],

}

top_overall = {
  NAME: "top/overall",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 13.3333],
    [HP, 20],
  ],

  EPIC: [
    [MAINSTAT, 7.6],
    [HP, 7.6],
    [ALLSTAT, 19],
  ],

  UNIQUE: [
    [MAINSTAT, 13.2],
    [HP, 11],
    [ALLSTAT, 16.5],
  ],

  LEGENDARY: [
    [MAINSTAT, 10.75],
    [ALLSTAT, 10.75],
    [HP, 10.75],
  ],

}

top_overall_noncash = {
  NAME: "top/overall",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 18],
    [HP, 12],
  ],

  EPIC: [
    [MAINSTAT, 15],
    [HP, 10],
    [ALLSTAT, 30],
  ],

  UNIQUE: [
    [MAINSTAT, 16.5],
    [HP, 11],
    [ALLSTAT, 33],
  ],

  LEGENDARY: [
    [MAINSTAT, 17],
    [ALLSTAT, 17],
    [HP, 11.3333],
  ],

}

bottom = {
  NAME: "bottom",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 13.3333],
    [HP, 20],
  ],

  EPIC: [
    [MAINSTAT, 7],
    [HP, 7],
    [ALLSTAT, 17.5],
  ],

  UNIQUE: [
    [MAINSTAT, 11.2],
    [HP, 9.3333],
    [ALLSTAT, 14],
  ],

  LEGENDARY: [
    [MAINSTAT, 9.25],
    [HP, 9.25],
    [ALLSTAT, 12.3333],
  ],
}

bottom_noncash = {
  NAME: "bottom",
  DEFAULT_CUBE: [MEISTER],

  COMMON: [],

  RARE: [
    [MAINSTAT, 18],
    [HP, 12],
  ],

  EPIC: [
    [MAINSTAT, 13.5],
    [HP, 9],
    [ALLSTAT, 27],
  ],

  UNIQUE: [
    [MAINSTAT, 14.5],
    [HP, 9.6666],
    [ALLSTAT, 29],
  ],

  LEGENDARY: [
    [MAINSTAT, 17],
    [HP, 11.3333],
    [ALLSTAT, 17],
  ],
}

hat = {
  NAME: "hat",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 13.3333],
    [HP, 20],
  ],

  EPIC: [
    [MAINSTAT, 7],
    [HP, 7],
    [ALLSTAT, 17.5],
  ],

  UNIQUE: [
    [MAINSTAT, 11.2],
    [HP, 9.3333],
    [ALLSTAT, 14],
  ],

  LEGENDARY: [
    [MAINSTAT, 11.25],
    [HP, 11.25],
    [ALLSTAT, 15],
    [COOLDOWN_1, 15],
    [COOLDOWN_2, 22.5],
  ],

}

hat_noncash = {
  NAME: "hat",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 21],
    [HP, 14],
  ],

  EPIC: [
    [MAINSTAT, 9],
    [HP, 6],
    [ALLSTAT, 18],
  ],

  UNIQUE: [
    [MAINSTAT, 14.5],
    [HP, 9.6666],
    [ALLSTAT, 29],
  ],

  LEGENDARY: [
    [MAINSTAT, 18],
    [HP, 12],
    [ALLSTAT, 18],
    [COOLDOWN_1, 12],
    [COOLDOWN_2, 18],
  ],

}

accessory = {
  NAME: "accessory",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 13.3333],
    [HP, 20],
  ],

  EPIC: [
    [MAINSTAT, 7],
    [HP, 7],
    [ALLSTAT, 17.5],
  ],

  UNIQUE: [
    [MAINSTAT, 8.8],
    [HP, 7.3333],
    [ALLSTAT, 11],
  ],

  LEGENDARY: [
    [MAINSTAT, 10.75],
    [HP, 10.75],
    [ALLSTAT, 14.3333],
    [MESO, 14.3333],
    [DROP, 14.3333],
  ],

}

accessory_noncash = {
  NAME: "accessory",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 21],
    [HP, 14],
  ],

  EPIC: [
    [MAINSTAT, 9],
    [HP, 6],
    [ALLSTAT, 18],
  ],

  UNIQUE: [
    [MAINSTAT, 10.5],
    [HP, 7],
    [ALLSTAT, 21],
  ],

  LEGENDARY: [
    [MAINSTAT, 17],
    [HP, 11.3333],
    [ALLSTAT, 17],
    [MESO, 11.3333],
    [DROP, 11.3333],
  ],
}

def percents(lines):
  for k in [COMMON, EPIC, UNIQUE, LEGENDARY]:
    if k in lines:
      lines[k] = [[x[0], 1/x[1]*100] for x in lines[k]]
  return lines

# TMS probabilities for violet, equality and unicube lines
#   https://tw.beanfun.com/beanfuncommon/EventAD_Mobile/EventAD.aspx?EventADID=8421

weapon_secondary_violet_equality = percents({
  NAME: "weapon",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [BOSS_30, 6.52],
    [ATT, 6.52],
    [IED_30, 8.7],
  ],

  LEGENDARY: [
    [BOSS_40, 4.44],
    [BOSS_35, 4.44],
    [BOSS_30, 4.44],
    [ATT, 4.44],
    [IED_40, 6.67],
    [IED_35, 6.67],
  ],

})

emblem_violet_equality = percents({
  NAME: "emblem",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [ATT, 6.98],
    [IED_30, 9.3],
  ],

  LEGENDARY: [
    [ATT, 5.13],
    [IED_40, 7.69],
    [IED_35, 7.69],
  ],

})

weapon_secondary_uni = percents({
  NAME: "weapon/secondary",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [BOSS_30, 5.48],
    [ATT, 8.22],
    [IED_30, 20.55],
  ],

  LEGENDARY: [
    [BOSS_40, 1.13],
    [BOSS_35, 2.10],
    [BOSS_30, 3.07],
    [ATT, 3.24],
    [IED_40, 16.18],
    [IED_35, 25.89],
  ],

})

emblem_uni = percents({
  NAME: "emblem",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [ATT, 8.7],
    [IED_30, 21.74],
  ],

  LEGENDARY: [
    [ATT, 3.45],
    [IED_40, 17.27],
    [IED_35, 27.63],
  ],

})

# pendants, rings, face, eye, earrings
accessory_violet_equality = percents({
  NAME: "accessory",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9.8],
    [HP, 11.76],
    [ALLSTAT, 7.84],
  ],

  LEGENDARY: [
    [MAINSTAT, 7.84],
    [ALLSTAT, 5.88],
    [HP, 7.84],
    [MESO, 5.88],
    [DROP, 5.88],
  ],

})

accessory_uni = percents({
  NAME: "accessory",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 11.63],
    [HP, 11.63],
    [ALLSTAT, 2.33],
  ],

  LEGENDARY: [
    [MAINSTAT, 6.06],
    [ALLSTAT, 1.52],
    [HP, 6.06],
    [MESO, 9.09],
    [DROP, 9.09],
  ],

})

cape_belt_shoulder_violet_equality = percents({
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 8.47],
    [HP, 10.17],
    [ALLSTAT, 6.78],
  ],

  LEGENDARY: [
    [MAINSTAT, 8.89],
    [HP, 8.89],
    [ALLSTAT, 6.67],
  ],

})

cape_belt_shoulder_uni = percents({
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 7.69],
    [HP, 7.69],
    [ALLSTAT, 1.54],
  ],

  LEGENDARY: [
    [MAINSTAT, 8.89],
    [HP, 8.89],
    [ALLSTAT, 6.67],
  ],

})

shoe_violet_equality = percents({
  NAME: "shoe",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 7.94],
    [HP, 9.52],
    [ALLSTAT, 6.35],
  ],

  LEGENDARY: [
    [MAINSTAT, 8.33],
    [HP, 8.33],
    [ALLSTAT, 6.25],
  ],

})

shoe_uni = percents({
  NAME: "shoe",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 6.33],
    [HP, 6.33],
    [ALLSTAT, 1.27],
  ],

  LEGENDARY: [
    [MAINSTAT, 7.27],
    [HP, 7.27],
    [ALLSTAT, 1.82],
  ],

})

glove_violet_equality = percents({
  NAME: "glove",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 7.46],
    [HP, 8.96],
    [ALLSTAT, 5.97],
  ],

  LEGENDARY: [
    [MAINSTAT, 7.69],
    [HP, 7.69],
    [ALLSTAT, 5.77],
    [CRITDMG, 7.69],
  ],

})

glove_uni = percents({
  NAME: "glove",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 5.26],
    [HP, 5.26],
    [ALLSTAT, 1.05],
  ],

  LEGENDARY: [
    [MAINSTAT, 5.8],
    [HP, 5.8],
    [ALLSTAT, 1.45],
    [CRITDMG, 2.9],
  ],

})

bottom_violet_equality = percents({
  NAME: "bottom",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 7.94],
    [HP, 9.52],
    [ALLSTAT, 6.35],
  ],

  LEGENDARY: [
    [MAINSTAT, 8.89],
    [HP, 8.89],
    [ALLSTAT, 6.67],
  ],

})

bottom_uni = percents({
  NAME: "bottom",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 6.35],
    [HP, 6.35],
    [ALLSTAT, 1.59],
  ],

  LEGENDARY: [
    [MAINSTAT, 8.89],
    [HP, 8.89],
    [ALLSTAT, 2.22],
  ],

})

top_overall_violet_equality = percents({
  NAME: "top/overall",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 6.85],
    [HP, 8.22],
    [ALLSTAT, 5.48],
  ],

  LEGENDARY: [
    [MAINSTAT, 7.84],
    [HP, 7.84],
    [ALLSTAT, 5.88],
  ],

})

top_overall_uni = percents({
  NAME: "top/overall",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 4.08],
    [HP, 4.08],
    [ALLSTAT, 1.02],
  ],

  LEGENDARY: [
    [MAINSTAT, 6.15],
    [HP, 6.15],
    [ALLSTAT, 1.54],
  ],

})

hat_violet_equality = percents({
  NAME: "hat",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 7.94],
    [HP, 9.52],
    [ALLSTAT, 6.35],
  ],

  LEGENDARY: [
    [MAINSTAT, 7.55],
    [HP, 7.55],
    [ALLSTAT, 5.66],
    [COOLDOWN_2, 3.77],
    [COOLDOWN_1, 5.66],
  ],

})

hat_uni = percents({
  NAME: "hat",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 5.8],
    [HP, 5.8],
    [ALLSTAT, 1.45],
  ],

  LEGENDARY: [
    [MAINSTAT, 5.0],
    [HP, 5.0],
    [ALLSTAT, 1.25],
    [COOLDOWN_2, 10.0],
    [COOLDOWN_1, 10.0],
  ],

})

# -------------------------------------------------------------------------------------------------

line_values = {
  COMMON: { ANY: 0 },

  RARE: {
    ATT: 3,
    ANY: 0,
    MAINSTAT: 3,
    HP: 3,
  },

  EPIC: {
    ATT: 6,
    ANY: 0,
    MAINSTAT: 6,
    ALLSTAT: 3,
    HP: 6,
  },

  UNIQUE: {
    BOSS_30: 30,
    IED_30: 30,
    ATT: 9,
    ANY: 0,
    MAINSTAT: 9,
    ALLSTAT: 6,
    HP: 9,
  },

  LEGENDARY: {
    BOSS_30: 30,
    BOSS_35: 35,
    BOSS_40: 40,
    IED_30: 30,
    IED_35: 35,
    IED_40: 40,
    ATT: 12,
    ANY: 0,
    MAINSTAT: 12,
    ALLSTAT: 9,
    HP: 12,
    COOLDOWN_2: 2,
    COOLDOWN_1: 1,
    CRITDMG: 8,
    MESO: 20,
    DROP: 20,
  },
}

def tabulate(rows):
  max_len = max((len(text) for (text, _) in rows))
  for (text, result) in rows:
    print(f"{text.rjust(max_len)} {result}")


def fmt_chance(text, wants, combos, combo_chance):
  chance = sum([combo_chance(want, combos) for want in wants])
  return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

def __cube_calc(print_combos, type, tier, lines):
  if type in tier_limits:
    tier = min(tier_limits[type], tier)

  print(f" {lines[NAME]} ({type.name.lower()} at {tier.name.lower()}) ".center(80, "="))

  def make_lines():
    # to represent all the lines we don't care about I generate an ANY line that
    # has 1-(sum of the chances of all lines we care about) chance
    def make_any_line(x):
      return x + [[ANY, 0]] # chance is calculated later

    lines_prime = make_any_line(lines[tier])
    return lines_prime + make_any_line(lines[tier - 1]), len(lines_prime)

  def cache_combos(cache):
    if tier not in cache:
      lines, num_prime = make_lines()

      # convert each column into a numpy array. we want them packed together for performance
      class LineCache:
        def __init__(self, lines):
          self.lines = lines
          self.__update()

        def __update(self):
            self.types, self.values, self.onein, self.is_prime = self.lines

        def filt(self, mask):
          self.lines = tuple([x[mask] for x in self.lines])
          self.__update()
          return self

        def copy(self):
          return LineCache(self.lines)

      def col(c, dtype=None):
        return np.array([x[c] for x in lines], dtype=dtype)

      # generate numpy arrays for each column
      types_col = col(LINE_TYPE)
      types_l = [Line(x) for x in types_col]
      values_col = np.array(
        [line_values[tier][x] for x in types_l[:num_prime]] +
        [line_values[tier - 1][x] for x in types_l[num_prime:]]
      )
      is_prime_pn = np.concatenate((np.repeat(True, num_prime),
                                    np.repeat(False, len(types_col) - num_prime)))
      c = LineCache((types_col, values_col, col(LINE_ONEIN, 'float64'), is_prime_pn))
      cache[tier] = c
    else:
      c = cache[tier]

    return c

  # cache combos for each set of lines
  combos_i = COMBOS_VIOLET if type == VIOLET else COMBOS
  if combos_i not in lines:
    lines[combos_i] = {}
  line_cache = cache_combos(lines[combos_i])

  # unicubes are 1/3rd the line chances because you roll 3 cubes on average to select
  chance_multiplier = 3 if type == UNI else 1

  prime_chance = prime_chances[type]
  if not isinstance(prime_chance, list):
      prime_chance = prime_chance[tier]

  # prime_chance = [prime_chance]
  prime_chance =         np.array(prime_chance, dtype='float64') .reshape(1, -1)
  nonprime_chance = (1 - np.array(prime_chance, dtype='float64')).reshape(1, -1)

  def combo_chance(want):
    c = line_cache.copy()

    # filter out lines that are not in our want dict to exponentially reduce combinations
    relevant_line_bits = reduce(or_, [x for x in want.keys() if x != LINES]) | ANY
    c.filt(c.types & relevant_line_bits != 0)

    # remember to update the number of prime lines
    num_prime = np.count_nonzero(c.is_prime)

    # calculate ANY line chance
    any_p = sum(1/c.onein[:num_prime-1])
    any_n = sum(1/c.onein[num_prime:-1])
    c.onein[num_prime - 1] = 1/(1 - any_p)
    c.onein[-1] = 1/(1 - any_n)

    # arrays of line indices to generate combinations
    p = np.arange(num_prime)
    n = np.arange(len(c.types))

    if type == VIOLET:
      combo_idxs = np.array(np.meshgrid(p, n, n, n, n, n)).T.reshape(-1, 6)
    elif type == UNI:
      combo_idxs = np.array(np.meshgrid(n)).T.reshape(-1, 1)
    else:
      combo_idxs = np.array(np.meshgrid(p, n, n)).T.reshape(-1, 3)

    c.filt(combo_idxs)
    # combo_idxs is an array of line combos as indices into pn: [[1, 2, 3], [1, 3, 2], ...]

    # when we do x[mask] in filt() and mask is an array of indices, we replace those indices
    #  with elements from x
    # so for example [a, b, c][ [[1, 2, 0], [0, 0, 0]] ] returns [[b, c, a], [a, a, a]]

    # when we do x[mask] in filt() and mask is an array of bools, we filter only the elements
    #  that are True in mask
    # so for example [a, b, c][ [True, False, True] ] returns [a, c]

    # can't have more than 2 of these in a combo
    # note: we AND with the line type because some lines match multiple lines. for example
    #       when we look for stat we also want to match allstat, so we set up the lines enum
    #       to be a bitmask so we can match multiple things such as MAINSTAT | ALLSTAT
    forbidden = [BOSS, IED, DROP]
    if np.any(c.types & reduce(or_, forbidden) != 0):
      mask = reduce(or_, [np.count_nonzero(c.types & x != 0, axis=1) > 2 for x in forbidden])
      c.filt(np.logical_not(mask))

    types, values, _, _ = c.lines
    if LINES in want:
      # all combinations that contains at least n lines of any of the stats specified
      # TODO: allow specifying minimum amount for the lines
      mask = sum([np.count_nonzero(types & x != 0, axis=1)
                  for x in want.keys() if x != LINES]) >= want[LINES]
    else:
      # all combinations that contain all of the stats and with at least the requested amt.
      mask = reduce(and_, [np.sum(values * (types & x != 0).astype(int), axis=1) >= want[x]
                           for x in want.keys()])

    good = c.filt(mask)

    # adjust the probability of prime lines by their prime chance,
    # and the probability of non-prime lines by the inverse of the prime chance.
    # this way, the sum of all proababilities of prime and non-prime lines will add up to 1
    good.onein /= np.where(good.is_prime, np.repeat(prime_chance, len(good.onein), axis=0),
                           np.repeat(nonprime_chance, len(good.onein), axis=0))

    return sum(np.prod(1/(good.onein * chance_multiplier), axis=1))

  def fmt_chance(text, wants):
    chance = sum([combo_chance(want) for want in wants])

    return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

  tabulate([fmt_chance(text, want) for (text, want) in print_combos])


def single_or_list(x):
  return x if isinstance(x, list) else [x]


def cube_calc(print_combos, types, tier, *args):
  for l in args:
    lt = types
    if not lt:
      lt = l[DEFAULT_CUBE]
    for t in single_or_list(lt):
      __cube_calc(print_combos, t, tier, l)


class Combos:
  def __init__(self, combos, types=[], tier=TIER_DEFAULT):
    self.calc = partial(cube_calc, combos, types, tier)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    pass


def cube_calcs():
  combos_wse_occult = [
    ("6+ att", [{ATT: 6}]),
    ("9+ att", [{ATT: 9}]),
    ("12+ att", [{ATT: 12}]),
  ]

  combos_any_ws = [
    ("any 2l combo of att+boss", [{ATT: 1, BOSS: 1, LINES: 2}]),
    ("any 2l combo of att+boss+ied", [{ATT: 1, BOSS: 1, IED: 1, LINES: 2}]),
    ("any 3l combo of att+boss", [{ATT: 1, BOSS: 1, LINES: 3}]),
    ("any 3l combo of att+boss+ied", [{ATT: 1, BOSS: 1, IED: 1, LINES: 3}]),
  ]

  combos_wse_master = [
    ("9+ att", [{ATT: 9}]),
    ("12+ att", [{ATT: 12}]),
    ("15+ att", [{ATT: 15}]),
    ("21+ att", [{ATT: 21}]),
  ]

  combos_ws_master = combos_any_ws + combos_wse_master + [
    ("any boss", [{BOSS: 1}]),
  ]

  combos_ws = combos_any_ws + [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
    ("21+ att and boss", [{ATT: 21, BOSS: 1}]),
    ("21+ att and ied", [{ATT: 21, IED: 1}]),
    ("18+ att and boss", [{ATT: 18, BOSS: 1}]),
    ("18+ att and ied", [{ATT: 18, IED: 1}]),
    ("60+ied", [{IED: 60}]),
    ("70+ied", [{IED: 70}]),
    ("60+ied and att", [{IED: 60, ATT: 1}]),
    ("60+ied and boss", [{IED: 60, BOSS: 1}]),
  ]

  combos_any_e = [
    ("any 2l combo of att+ied", [{ATT: 1, IED: 1, LINES: 2}]),
    ("any 3l combo of att+ied", [{ATT: 1, IED: 1, LINES: 3}]),
  ]

  combos_e_master = combos_any_e + combos_wse_master

  combos_e = combos_any_e + [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
    ("21+ att and ied", [{ATT: 21, IED: 1}]),
  ]

  combos_wse_b = [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
  ]

  combos_stat = [
    ("18+ stat", [{STAT: 18}]),
    ("21+ stat", [{STAT: 21}]),
    ("30+ stat", [{STAT: 30}]),
    ("33+ stat", [{STAT: 33}]),
    ("18+ hp", [{HP: 18}]),
    ("21+ hp", [{HP: 21}]),
    ("30+ hp", [{HP: 30}]),
    ("33+ hp", [{HP: 33}]),
    ("12+ all stat", [{ALLSTAT: 12}]),
    ("15+ all stat", [{ALLSTAT: 15}]),
    ("21+ all stat", [{ALLSTAT: 21}]),
  ]

  combos_mesodrop = [
    ("20+ meso or 20+ drop", [{MESO: 20}, {DROP: 20}]),
    ("20+ meso", [{MESO: 20}]),
    ("20+ drop", [{DROP: 20}]),
    ("40 meso or 40 drop", [{MESO: 40}, {DROP: 40}]),
    ("40 meso", [{MESO: 40}]),
    ("40 drop", [{DROP: 40}]),
    ("20+ meso and 20+ drop", [{MESO: 20, DROP: 20}]),
  ]

  combos_glove = combos_stat + [
    ("8+ crit damage", [{CRITDMG: 8}]),
    ("8+ crit damage and 6+ stat", [{CRITDMG: 8, STAT: 6}]),
    ("8+ crit damage and 9+ stat", [{CRITDMG: 8, STAT: 9}]),
    ("8+ crit damage and 12+ stat", [{CRITDMG: 8, STAT: 12}]),
    ("8+ crit damage and 18+ stat", [{CRITDMG: 8, STAT: 18}]),
    ("8+ crit damage and 24 stat", [{CRITDMG: 8, STAT: 24}]),
    ("16+ crit damage", [{CRITDMG: 16}]),
    ("16+ crit damage and 6+ stat", [{CRITDMG: 16, STAT: 6}]),
    ("16+ crit damage and 9+ stat", [{CRITDMG: 16, STAT: 9}]),
    ("16+ crit damage and 12 stat", [{CRITDMG: 16, STAT: 12}]),
    ("24 crit damage", [{CRITDMG: 24}]),
  ]

  combos_hat = combos_stat + [
    ("2+s cooldown", [{COOLDOWN: 2}]),
    ("2+s cooldown and any stat", [{COOLDOWN: 2, STAT: 1}]),
    ("2+s cooldown and 9+ stat", [{COOLDOWN: 2, STAT: 9}]),
    ("2+s cooldown and 12+ stat", [{COOLDOWN: 2, STAT: 12}]),
    ("2+s cooldown and 18+ stat", [{COOLDOWN: 2, STAT: 18}]),
    ("3+s cooldown", [{COOLDOWN: 3}]),
    ("3+s cooldown and any stat", [{COOLDOWN: 3, STAT: 1}]),
    ("4+s cooldown", [{COOLDOWN: 4}]),
    ("4+s cooldown and any stat", [{COOLDOWN: 4, STAT: 1}]),
    ("5+s cooldown", [{COOLDOWN: 5}]),
    ("6+s cooldown", [{COOLDOWN: 6}]),
  ]

  combos_occult_stat = [
    ("6+ stat", [{STAT: 6}]),
    ("9+ stat", [{STAT: 9}]),
    ("12+ stat", [{STAT: 12}]),
    ("3+ all stat", [{ALLSTAT: 3}]),
    ("6+ all stat", [{ALLSTAT: 6}]),
    ("6+ hp", [{HP: 6}]),
    ("9+ hp", [{HP: 9}]),
    ("12+ hp", [{HP: 12}]),
  ]

  combos_master_stat = combos_occult_stat + [
    ("15+ stat", [{STAT: 15}]),
    ("9+ all stat", [{ALLSTAT: 9}]),
    ("15+ hp", [{HP: 15}]),
  ]

  Combos(combos_ws).calc(
    weapon,
    weapon_noncash,
    secondary,
    secondary_noncash,
    weapon_secondary_violet_equality,
  )

  Combos(combos_ws_master, MASTER).calc(
    weapon_noncash,
    secondary_noncash,
  )

  Combos(combos_e).calc(
    emblem,
    emblem_noncash,
    emblem_violet_equality,
  )

  Combos(combos_e_master, MASTER).calc(
    emblem_noncash,
  )

  Combos(combos_wse_occult, OCCULT).calc(
    weapon_noncash,
    secondary_noncash,
    emblem_noncash,
  )

  Combos(combos_wse_b).calc(
    weapon_bonus,
    secondary_bonus,
    emblem_bonus,
  )

  Combos(combos_stat).calc(
    top_overall,
    top_overall_noncash,
    top_overall_violet_equality,
    cape_belt_shoulder_violet_equality,
    shoe_violet_equality,
    bottom,
    bottom_noncash,
    bottom_violet_equality,
  )

  Combos(combos_stat + combos_mesodrop).calc(
    accessory,
    accessory_noncash,
    accessory_violet_equality,
  )

  Combos(combos_hat).calc(
    hat,
    hat_noncash,
    hat_violet_equality,
  )

  Combos(combos_occult_stat, OCCULT).calc(
    accessory_noncash,
    top_overall_noncash,
    hat_noncash,
  )

  Combos(combos_master_stat, [MASTER, MEISTER], UNIQUE).calc(
    accessory_noncash,
    top_overall_noncash,
    hat_noncash,
  )

  Combos(combos_master_stat, RED, UNIQUE).calc(
    accessory,
    top_overall,
    hat,
  )

  Combos(combos_glove).calc(
    glove_violet_equality,
  )


def unicube_calcs():
  combos_e_prime = [
    ("12 att", [{ATT: 12}]),
    ("40 ied", [{IED: 40}]),
    ("35+ ied", [{IED: 35}]),
  ]

  combos_e_nonprime = [
    ("9+ att or 30+ ied", [{ATT: 9}, {IED: 30}]),
    ("9+ att", [{ATT: 9}]),
    ("30+ ied", [{IED: 30}]),
  ]

  combos_ws_prime = [
    ("35+ boss", [{BOSS: 35}]),
    ("40 boss", [{BOSS: 40}]),
  ] + combos_e_prime

  combos_ws_nonprime = [
    ("9+ att or 30+ boss or 30+ ied", [{ATT: 9}, {BOSS: 30}, {IED: 30}]),
    ("9+ att or 30+ boss", [{ATT: 9}, {BOSS: 30}]),
    ("30+ boss", [{BOSS: 30}]),
  ] + combos_e_nonprime

  combos_e = combos_e_nonprime + combos_e_prime
  combos_ws = combos_ws_nonprime + combos_ws_prime

  combos_stat_prime = [
    ("12 stat", [{STAT: 12}]),
    ("12 hp", [{HP: 12}]),
    ("9 allstat", [{ALLSTAT: 9}]),
  ]

  combos_stat_nonprime = [
    ("6+ stat", [{STAT: 6}]),
    ("9+ stat", [{STAT: 9}]),
    ("9+ hp", [{HP: 9}]),
    ("6 allstat", [{ALLSTAT: 6}]),
  ]

  combos_hat_prime = combos_stat_prime + [
    ("1+s cooldown", [{COOLDOWN: 1}]),
    ("2s cooldown", [{COOLDOWN: 2}]),
  ]

  combos_mesodrop = [
    ("20 meso", [{MESO: 20}]),
    ("20 drop", [{DROP: 20}]),
    ("20 meso or 20 drop", [{MESO: 20}, {DROP: 20}]),
  ]

  combos_stat = combos_stat_nonprime + combos_stat_prime
  combos_glove_prime = combos_stat_prime + [ ("8 crit damage", [{CRITDMG: 8}]) ]
  combos_glove = combos_stat_nonprime + combos_glove_prime
  combos_hat = combos_stat_nonprime + combos_hat_prime

  Combos(combos_ws).calc(
    weapon_secondary_uni,
  )

  Combos(combos_e).calc(
    emblem_uni,
  )

  Combos(combos_stat).calc(
    cape_belt_shoulder_uni,
    shoe_uni,
    bottom_uni,
    top_overall_uni,
  )

  Combos(combos_stat + combos_mesodrop).calc(
    accessory_uni,
  )

  Combos(combos_glove).calc(
    glove_uni,
  )

  Combos(combos_hat).calc(
    hat_uni,
  )

if __name__ == "__main__":
  print(f" ! DISCLAIMER ! ".center(80, "="))
  print(disclaimer)

  cube_calcs()
  unicube_calcs()
