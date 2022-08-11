#!/usr/bin/env python3

from functools import reduce, partial
from operator import mul, or_, and_, add
import numpy as np
from enum import IntEnum, IntFlag, auto

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
  BOSS = auto()
  IED = auto()
  ATT = auto()
  ANY = auto()
  MAINSTAT = auto()
  ALLSTAT = auto()
  STAT = MAINSTAT | ALLSTAT
  HP = auto()
  COOLDOWN = auto()
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

def debug_print_combos(good):
  a = np.dstack((good.types, good.values, good.onein, good.is_prime)).tolist()
  a = [[[Line(c[0]), c[1], c[2], c[3]] for c in x] for x in a]
  from pprint import pprint
  pprint(a)
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
LINE_VALUE = 1
LINE_ONEIN = 2

weapon = {
  NAME: "weapon",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [BOSS, 30, 14.3333],
    [IED,  30, 14.3333],
    [ATT,   9, 14.3333],
  ],

  LEGENDARY: [
    [BOSS, 40, 20.5],
    [BOSS, 35, 20.5],
    [BOSS, 30, 20.5],
    [IED,  40, 20.5],
    [IED,  35, 20.5],
    [ATT,  12, 20.5],
  ],

}

weapon_noncash = {
  NAME: "weapon",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [ATT, 3, 57],
  ],

  EPIC: [
    [ATT, 6, 26],
  ],

  UNIQUE: [
    [BOSS, 30, 15],
    [IED,  30, 15],
    [ATT,   9, 15],
  ],

  LEGENDARY: [
    [BOSS, 40, 36],
    [BOSS, 35, 18],
    [BOSS, 30, 18],
    [IED,  40, 36],
    [IED,  35, 18],
    [ATT,  12, 18],
  ],

}

secondary = {
  NAME: "secondary",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [BOSS, 30, 17.0],
    [IED,  30, 17.0],
    [ATT,   9, 17.0],
  ],

  LEGENDARY: [
    [BOSS, 40, 23.5],
    [BOSS, 35, 23.5],
    [BOSS, 30, 23.5],
    [IED,  40, 23.5],
    [IED,  35, 23.5],
    [ATT,  12, 23.5],
  ],

}

secondary_noncash = {
  NAME: "secondary",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [ATT, 3, 57],
  ],

  EPIC: [
    [ATT, 6, 35],
  ],

  UNIQUE: [
    [BOSS, 30, 21],
    [IED,  30, 21],
    [ATT,   9, 21],
  ],

  LEGENDARY: [
    [BOSS, 40, 24],
    [BOSS, 35, 24],
    [BOSS, 30, 48],
    [IED,  40, 48],
    [IED,  35, 24],
    [ATT,  12, 24],
  ],

}

emblem = {
  NAME: "emblem",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    [IED,  30, 13.3333],
    [ATT,   9, 13.3333],
  ],

  LEGENDARY: [
    [IED,  40, 17.5],
    [IED,  35, 17.5],
    [ATT,  12, 17.5],
  ],

}

emblem_noncash = {
  NAME: "emblem",
  DEFAULT_CUBE: MEISTER,

  RARE: [
    [ATT, 3, 57],
  ],

  EPIC: [
    [ATT, 6, 26],
  ],

  UNIQUE: [
    [IED,  30, 14],
    [ATT,   9, 14],
  ],

  LEGENDARY: [
    [IED,  40, 15.5],
    [IED,  35, 31],
    [ATT,  12, 15.5],
  ],

}

weapon_bonus = {
  NAME: "weapon",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 9, 21.5],
  ],

  LEGENDARY: [
    [ATT, 12, 19.5],
  ],

}

secondary_bonus = {
  NAME: "secondary",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 9, 21.5],
  ],

  LEGENDARY: [
    [ATT, 12, 20.5],
  ],

}

emblem_bonus = {
  NAME: "emblem",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    [ATT, 9, 21],
  ],

  LEGENDARY: [
    [ATT, 12, 19],
  ],

}

top_overall = {
  NAME: "top/overall",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 13.3333],
    [HP, 3, 20],
  ],

  EPIC: [
    [MAINSTAT, 6, 7.6],
    [HP, 6, 7.6],
    [ALLSTAT, 3, 19],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 13.2],
    [HP, 9, 11],
    [ALLSTAT, 6, 16.5],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 10.75],
    [ALLSTAT, 9, 10.75],
    [HP, 12, 10.75],
  ],

}

top_overall_noncash = {
  NAME: "top/overall",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 18],
    [HP, 3, 12],
  ],

  EPIC: [
    [MAINSTAT, 6, 15],
    [HP, 6, 10],
    [ALLSTAT, 3, 30],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 16.5],
    [HP, 9, 11],
    [ALLSTAT, 6, 33],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 17],
    [ALLSTAT, 9, 17],
    [HP, 12, 11.3333],
  ],

}

hat = {
  NAME: "hat",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 13.3333],
    [HP, 3, 20],
  ],

  EPIC: [
    [MAINSTAT, 6, 7],
    [HP, 6, 7],
    [ALLSTAT, 3, 17.5],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 11.2],
    [HP, 9, 9.3333],
    [ALLSTAT, 6, 14],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 11.25],
    [HP, 12, 11.25],
    [ALLSTAT, 9, 15],
    [COOLDOWN, 1, 15],
    [COOLDOWN, 2, 22.5],
  ],

}

hat_noncash = {
  NAME: "hat",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 21],
    [HP, 3, 14],
  ],

  EPIC: [
    [MAINSTAT, 6, 9],
    [HP, 6, 6],
    [ALLSTAT, 6, 18],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 14.5],
    [HP, 9, 9.6666],
    [ALLSTAT, 6, 29],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 18],
    [HP, 12, 12],
    [ALLSTAT, 9, 18],
    [COOLDOWN, 1, 12],
    [COOLDOWN, 2, 18],
  ],

}

accessory = {
  NAME: "accessory",
  DEFAULT_CUBE: [RED, BLACK],

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 13.3333],
    [HP, 3, 20],
  ],

  EPIC: [
    [MAINSTAT, 6, 7],
    [HP, 6, 7],
    [ALLSTAT, 6, 17.5],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 8.8],
    [HP, 9, 7.3333],
    [ALLSTAT, 6, 11],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 10.75],
    [HP, 12, 10.75],
    [ALLSTAT, 9, 14.3333],
    [MESO, 20, 14.3333],
    [DROP, 20, 14.3333],
  ],

}

accessory_noncash = {
  NAME: "accessory",
  DEFAULT_CUBE: MEISTER,

  COMMON: [],

  RARE: [
    [MAINSTAT, 3, 21],
    [HP, 3, 14],
  ],

  EPIC: [
    [MAINSTAT, 6, 9],
    [HP, 6, 6],
    [ALLSTAT, 3, 18],
  ],

  UNIQUE: [
    [MAINSTAT, 9, 10.5],
    [HP, 9, 7],
    [ALLSTAT, 6, 21],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 17],
    [HP, 12, 11.3333],
    [ALLSTAT, 9, 17],
    [MESO, 20, 11.3333],
    [DROP, 20, 11.3333],
  ],
}

# TMS probabilities for violet, equality and unicube lines
#   https://tw.beanfun.com/beanfuncommon/EventAD_Mobile/EventAD.aspx?EventADID=8421

weapon_secondary_violet_equality = {
  NAME: "weapon",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [BOSS, 30, 1/6.52*100],
    [ATT, 9, 1/6.52*100],
    [IED, 30, 1/8.7*100],
  ],

  LEGENDARY: [
    [BOSS, 40, 1/4.44*100],
    [BOSS, 35, 1/4.44*100],
    [BOSS, 30, 1/4.44*100],
    [ATT, 12, 1/4.44*100],
    [IED, 40, 1/6.67*100],
    [IED, 35, 1/6.67*100],
  ],

}

emblem_violet_equality = {
  NAME: "emblem",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [ATT, 9, 1/6.98*100],
    [IED, 30, 1/9.3*100],
  ],

  LEGENDARY: [
    [ATT, 12, 1/5.13*100],
    [IED, 40, 1/7.69*100],
    [IED, 35, 1/7.69*100],
  ],

}

weapon_secondary_uni = {
  NAME: "weapon/secondary",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [BOSS, 30, 1/5.48*100],
    [ATT, 9, 1/8.22*100],
    [IED, 30, 1/20.55*100],
  ],

  LEGENDARY: [
    [BOSS, 40, 1/1.13*100],
    [BOSS, 35, 1/2.10*100],
    [BOSS, 30, 1/3.07*100],
    [ATT, 12, 1/3.24*100],
    [IED, 40, 1/16.18*100],
    [IED, 35, 1/25.89*100],
  ],

}

emblem_uni = {
  NAME: "emblem",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [ATT, 9, 1/8.7*100],
    [IED, 30, 1/21.74*100],
  ],

  LEGENDARY: [
    [ATT, 12, 1/3.45*100],
    [IED, 40, 1/17.27*100],
    [IED, 35, 1/27.63*100],
  ],

}

# pendants, rings, face, eye, earrings
accessory_violet_equality = {
  NAME: "accessory",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/9.8*100],
    [HP, 9, 1/11.76*100],
    [ALLSTAT, 6, 1/7.84*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/7.84*100],
    [ALLSTAT, 9, 1/5.88*100],
    [HP, 12, 1/7.84*100],
    [MESO, 20, 1/5.88*100],
    [DROP, 20, 1/5.88*100],
  ],

}

accessory_uni = {
  NAME: "accessory",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/11.63*100],
    [HP, 9, 1/11.63*100],
    [ALLSTAT, 6, 1/2.33*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/6.06*100],
    [ALLSTAT, 9, 1/1.52*100],
    [HP, 12, 1/6.06*100],
    [MESO, 20, 1/9.09*100],
    [DROP, 20, 1/9.09*100],
  ],

}

cape_belt_shoulder_violet_equality = {
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/8.47*100],
    [HP, 9, 1/10.17*100],
    [ALLSTAT, 6, 1/6.78*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/8.89*100],
    [HP, 12, 1/8.89*100],
    [ALLSTAT, 9, 1/6.67*100],
  ],

}

cape_belt_shoulder_uni = {
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/7.69*100],
    [HP, 9, 1/7.69*100],
    [ALLSTAT, 6, 1/1.54*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/8.89*100],
    [HP, 12, 1/8.89*100],
    [ALLSTAT, 9, 1/6.67*100],
  ],

}

shoe_violet_equality = {
  NAME: "shoe",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/7.94*100],
    [HP, 9, 1/9.52*100],
    [ALLSTAT, 6, 1/6.35*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/8.33*100],
    [HP, 12, 1/8.33*100],
    [ALLSTAT, 9, 1/6.25*100],
  ],

}

shoe_uni = {
  NAME: "shoe",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/6.33*100],
    [HP, 9, 1/6.33*100],
    [ALLSTAT, 6, 1/1.27*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/7.27*100],
    [HP, 12, 1/7.27*100],
    [ALLSTAT, 9, 1/1.82*100],
  ],

}

glove_violet_equality = {
  NAME: "glove",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/7.46*100],
    [HP, 9, 1/8.96*100],
    [ALLSTAT, 6, 1/5.97*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/7.69*100],
    [HP, 12, 1/7.69*100],
    [ALLSTAT, 9, 1/5.77*100],
    [CRITDMG, 8, 1/7.69*100],
  ],

}

glove_uni = {
  NAME: "glove",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/5.26*100],
    [HP, 9, 1/5.26*100],
    [ALLSTAT, 6, 1/1.05*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/5.8*100],
    [HP, 12, 1/5.8*100],
    [ALLSTAT, 9, 1/1.45*100],
    [CRITDMG, 8, 1/2.9*100],
  ],

}

bottom_violet_equality = {
  NAME: "bottom",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/7.94*100],
    [HP, 9, 1/9.52*100],
    [ALLSTAT, 6, 1/6.35*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/8.89*100],
    [HP, 12, 1/8.89*100],
    [ALLSTAT, 9, 1/6.67*100],
  ],

}

bottom_uni = {
  NAME: "bottom",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/6.35*100],
    [HP, 9, 1/6.35*100],
    [ALLSTAT, 6, 1/1.59*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/8.89*100],
    [HP, 12, 1/8.89*100],
    [ALLSTAT, 9, 1/2.22*100],
  ],

}

top_overall_violet_equality = {
  NAME: "top/overall",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/6.85*100],
    [HP, 9, 1/8.22*100],
    [ALLSTAT, 6, 1/5.48*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/7.84*100],
    [HP, 12, 1/7.84*100],
    [ALLSTAT, 9, 1/5.88*100],
  ],

}

top_overall_uni = {
  NAME: "top/overall",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/4.08*100],
    [HP, 9, 1/4.08*100],
    [ALLSTAT, 6, 1/1.02*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/6.15*100],
    [HP, 12, 1/6.15*100],
    [ALLSTAT, 9, 1/1.54*100],
  ],

}

hat_violet_equality = {
  NAME: "hat",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    [MAINSTAT, 9, 1/7.94*100],
    [HP, 9, 1/9.52*100],
    [ALLSTAT, 6, 1/6.35*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/7.55*100],
    [HP, 12, 1/7.55*100],
    [ALLSTAT, 9, 1/5.66*100],
    [COOLDOWN, 2, 1/3.77*100],
    [COOLDOWN, 1, 1/5.66*100],
  ],

}

hat_uni = {
  NAME: "hat",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    [MAINSTAT, 9, 1/5.8*100],
    [HP, 9, 1/5.8*100],
    [ALLSTAT, 6, 1/1.45*100],
  ],

  LEGENDARY: [
    [MAINSTAT, 12, 1/5.0*100],
    [HP, 12, 1/5.0*100],
    [ALLSTAT, 9, 1/1.25*100],
    [COOLDOWN, 2, 1/10.0*100],
    [COOLDOWN, 1, 1/10.0*100],
  ],

}

# ---------------------------------------------------------------------------------------------------------

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
      return x + [[ANY, 0, 0]] # chance is calculated later

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

      # arrays of line indices to generate combinations
      p = np.arange(num_prime)
      n = np.arange(len(lines))
      is_prime_pn = np.concatenate((np.repeat(True, len(p)), np.repeat(False, len(n))))
      c = LineCache((col(LINE_TYPE), col(LINE_VALUE), col(LINE_ONEIN, 'float64'), is_prime_pn))

      # calculate ANY line chance
      any_p = sum(1/c.onein[:num_prime-1])
      any_n = sum(1/c.onein[num_prime:-1])
      c.onein[num_prime - 1] = 1/(1 - any_p)
      c.onein[-1] = 1/(1 - any_n)

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
      forbidden = [BOSS, IED]
      if reduce(or_, [np.any(c.types == x) for x in forbidden]):
        mask = reduce(or_, [np.count_nonzero(c.types == x, axis=1) > 2 for x in forbidden])
        c.filt(np.logical_not(mask))

      cache[tier] = c
    else:
      c = cache[tier]

    return c

  # cache combos for each set of lines
  combos_i = COMBOS_VIOLET if type == VIOLET else COMBOS
  if combos_i not in lines:
    lines[combos_i] = {}
  c = cache_combos(lines[combos_i])

  # unicubes are 1/3rd the line chances because you roll 3 cubes on average to select
  chance_multiplier = 3 if type == UNI else 1

  prime_chance = prime_chances[type]
  if not isinstance(prime_chance, list):
      prime_chance = prime_chance[tier]

  # prime_chance = [prime_chance]
  prime_chance =         np.array(prime_chance, dtype='float64') .reshape(1, -1)
  nonprime_chance = (1 - np.array(prime_chance, dtype='float64')).reshape(1, -1)

  def combo_chance(want):
    types, values, _, _ = c.lines
    if LINES in want:
      # all combinations that contains at least n lines of any of the stats specified
      # TODO: allow specifying minimum amount for the lines
      mask = sum([np.count_nonzero(types == x, axis=1)
                  for x in want.keys() if x != LINES]) >= want[LINES]
    else:
      # all combinations that contain all of the stats and with at least the requested amt.
      # note: we AND with the line type because some lines match multiple lines. for example
      #       when we look for stat we also want to match allstat, so we set up the lines enum
      #       to be a bitmask so we can match multiple things such as MAINSTAT | ALLSTAT
      mask = reduce(and_, [np.sum(values * (types & x != 0).astype(int), axis=1) >= want[x]
                           for x in want.keys()])

    good = c.copy().filt(mask)

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

print(f" ! DISCLAIMER ! ".center(80, "="))
print(disclaimer)

cube_calcs()
unicube_calcs()
