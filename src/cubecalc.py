from functools import reduce
from operator import or_, and_
import numpy as np

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

familiar calculations are very speculative and might not be accurate at all:
  - for familiars we use the data mined rates from southperry. we don't know
    whether these refer to reveal or familiard cards or both. we don't even
    know the prime rates so it's hardcoded to never get double prime
  - for red cards we use the data I collected from 2.9k rolls to estimate
    line rates. this is probably not a big enough sample size to be
    truly representative of the averages.

NOTE: for cases where the tier is lower than the max tier of the cube
      (such as red cubes on unique) it's assumed that you won't tier up
"""

from common import *

# prime chances can be calculated from the official KMS probabilities:
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/red
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/black
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/strange
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/master
#   https://maplestory.nexon.com/Guide/OtherProbability/cube/artisan

# TMS violet prime chance from: https://strategywiki.org/wiki/MapleStory/Potential_System

prime_chances = {
  RED: [1, 0.1, 0.01],
  BLACK: [1, 0.2, 0.05],
  VIOLET: [1, 0.1, 0.01, 0.01, 0.1, 0.01],
  EQUALITY: [1, 1, 1],
  BONUS: {
    BASE: [1] * 3,
    COMMON: [1] * 3,
    RARE: [1] + [1.0/51]*2,
    EPIC: [1] + [1.0/21]*2,
    UNIQUE: [1] + [1.0/51]*2,
    LEGENDARY: [1] + [0.004975]*2,
  },
  OCCULT: {
    BASE: [1] * 3,
    COMMON: [1] * 3,
    RARE: [1] + [1.0/1001]*2,
    EPIC: [1] + [1.0/101]*2,
  },
  MASTER: {
    BASE: [1] * 3,
    COMMON: [1] * 3,
    RARE: [1] + [1.0/6]*2,
    EPIC: [1] + [1.0/21]*2,
    UNIQUE: [1] + [1.0/84.3333]*2,
  },
  MEISTER: {
    BASE: [1] * 3,
    COMMON: [1] * 3,
    RARE: [1] + [1.0/6]*2,
    EPIC: [1] + [1.0/12.5008]*2,
    UNIQUE: [1] + [1.0/58.9666]*2,
    LEGENDARY: [1] + [0.001996]*2,
  },
  UNI: [0.15],
  FAMILIAR: [1, 0],
  RED_FAM_CARD: [1, 13/2903],
}

# amounts are either just the amount of all lvl ranges or a lists of tuples of (max lvl, amount)
# line values from https://strategywiki.org/wiki/MapleStory/Potential_System#Bonus_Potential
# TODO: consider scraping this data or at least moving it out of this file

MAXLVL = 300
HIGHLVL_KMS = 250

def find_line_values(cube, category, region):
  has_gms_lines = (region & HAS_GMS_LINES) != 0
  highlvl = 151 if has_gms_lines else HIGHLVL_KMS
  lowlvlmax = highlvl - 1

  minlvl = lambda minlvl, amt: [ (minlvl - 1, 0), (MAXLVL, amt) ]

  def addtier(values, amount, minlv=highlvl):
    _, lastamt = values[-1]
    return values[:-1] + [(minlv - 1, lastamt), (MAXLVL, amount)]

  mpot_4 = [
    (30, 1),
    (70, 2),
    (lowlvlmax, 3),
    (MAXLVL, 4),
  ]

  mpot_7 = [
    (30, 2),
    (70, 4),
    (lowlvlmax, 6),
    (MAXLVL, 7),
  ]

  mpot_8 = [
    (49, 0),
    (60, 5),
    (80, 6),
    (MAXLVL, 8),
  ]

  mpot_9 = [
    (30, 3),
    (70, 6),
    (MAXLVL, 9),
  ]

  mpot_10_kms = addtier(mpot_9, 10, HIGHLVL_KMS)
  mpot_10 = addtier(mpot_9, 10) if has_gms_lines else mpot_10_kms

  mpot_12 = [
    (30, 6),
    (70, 9),
    (150, 12),
  ]

  mpot_13_kms = addtier(mpot_12, 13, HIGHLVL_KMS)
  mpot_13 = addtier(mpot_12, 13) if has_gms_lines else mpot_13_kms

  mpot_20 = [
    (30, 10),
    (70, 15),
    (MAXLVL, 20),
  ]

  flat_mainstat_13 = [
    (20, 2),
    (40, 4),
    (50, 6),
    (70, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_hp_125 = [(x, x) for x in range(10, 120, 10)] + [
    (lowlvlmax, 120),
    (MAXLVL, 125),
  ]

  flat_att_13 = [
    (20, 2),
    (40, 4),
    (60, 6),
    (80, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_allstat_6 = [(x, x//20) for x in range(20, 100, 20)] + [
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  flat_mainstat_6 = [
    (20, 1),
    (40, 2),
    (50, 3),
    (70, 4),
    (90, 5),
    (MAXLVL, 6),
  ]

  flat_hp_60 = [(x, x//2) for x in range(10, 120, 10)] + [(MAXLVL, 60)]

  flat_att_6 = [
    (20, 1),
    (40, 2),
    (60, 3),
    (80, 4),
    (90, 5),
    (MAXLVL, 6),
  ]

  hp_recovery_30 = [
    (30, 10),
    (70, 20),
    (MAXLVL, 30),
  ]

  hp_recovery_40 = [
    (30, 20),
    (70, 30),
    (MAXLVL, 40),
  ]

  values = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_HP_A: flat_hp_60,
      FLAT_ATT_A: flat_att_6,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_13,
      FLAT_HP_A: flat_hp_125,
      FLAT_ATT_A: flat_att_13,
      MAINSTAT_A: mpot_4,
      HP_A: mpot_4,
      FLAT_ALLSTAT_A: flat_allstat_6,
      ATT_A: mpot_4,
      DAMAGE_A: mpot_4,
      IED_C: minlvl(30, 15),
    },

    EPIC: {
      ANY: 1,
      MAINSTAT_A: mpot_7,
      ALLSTAT_A: mpot_4,
      HP_A: mpot_7,
      INVIN: 1,
      ATT_A: mpot_7,
      DAMAGE_A: mpot_7,
      IED_C: minlvl(50, 15),
    },

    UNIQUE: {
      ANY: 1,
      BOSS_C: minlvl(100, 30),
      IED_C: minlvl(50, 30),
      ATT_A: mpot_10,
      DAMAGE_A: mpot_10,
      MAINSTAT_A: mpot_10,
      ALLSTAT_A: mpot_7,
      HP_A: mpot_10_kms,
      INVIN: 2,
      DECENT_SHARP_EYES: minlvl(120, 1),
      MAINSTAT_PER_10_LVLS: minlvl(30, 1),
      HP_ITEMS_AND_SKILLS_A: hp_recovery_30,
    },

    LEGENDARY: {
      ANY: 1,
      BOSS_C: minlvl(50, 30),
      BOSS_B: minlvl(100, 35),
      BOSS_A: minlvl(100, 40),
      IED_B: minlvl(50, 35),
      IED_A: minlvl(100, 40),
      ATT_A: mpot_13,
      DAMAGE_A: mpot_13,
      MAINSTAT_A: mpot_13,
      ALLSTAT_A: mpot_10,
      HP_A: mpot_13_kms,
      COOLDOWN_2: minlvl(120, 2),
      COOLDOWN_1: minlvl(70, 1),
      CRITDMG_A: mpot_8,
      MESO_A: mpot_20,
      DROP_A: mpot_20,
      INVIN: 3,
      DECENT_SPEED_INFUSION: minlvl(120, 1),
      DECENT_COMBAT_ORDERS: minlvl(70, 1),
      ATT_PER_10_LVLS: minlvl(30, 1),
      AUTOSTEAL_A: 7,
      AUTOSTEAL_B: 5,
      AUTOSTEAL_C: 3,
      HP_ITEMS_AND_SKILLS_A: hp_recovery_40,
    },
  }

  flat_att_3 = [
    (50, 1),
    (100, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_11 = [
    (20, 2),
    (50, 4),
    (70, 6),
    (90, 8),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  flat_att_11 = [
    (20, 1),
    (40, 2),
    (60, 4),
    (80, 6),
    (90, 8),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  flat_hp_125 = [
    (20, 10),
    (50, 15),
    (90, 50),
    (lowlvlmax, 100),
    (MAXLVL, 125),
  ]

  mainstat_3 = [
    (90, 1),
    (lowlvlmax, 2),
    (MAXLVL, 3),
  ]

  flat_allstat_3 = [
    (50, 1),
    (90, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_15 = [
    (20, 4),
    (40, 5),
    (50, 8),
    (70, 10),
    (90, 12),
    (lowlvlmax, 14),
    (MAXLVL, 15),
  ]

  flat_att_12 = [
    (20, 4),
    (50, 6),
    (90, 8),
    (lowlvlmax, 11),
    (MAXLVL, 12),
  ]

  flat_hp_195 = [(x, int(x*1.5)) for x in range(10, 120, 10)] + [
    (lowlvlmax, 180),
  ]

  if has_gms_lines:
    flat_hp_195 += (HIGHLVL_KMS - 1, 185)

  flat_hp_195 += [(MAXLVL, 195)]

  mainstat_5 = [
    (20, 1),
    (50, 2),
    (90, 3),
    (lowlvlmax, 4),
    (MAXLVL, 4),
  ]

  hp_6 = mainstat_5[:3] + [
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  allstat_3 = [
    (90, 1),
    (lowlvlmax, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_17 = [
    (20, 8),
    (50, 10),
    (70, 12),
    (90, 14),
    (lowlvlmax, 16),
    (MAXLVL, 17),
  ]

  flat_att_13 = [
    (20, 6),
    (50, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_hp_250 = [(x, x*2) for x in range(10, 120, 10)] + [
    (lowlvlmax, 240),
    (MAXLVL, 250),
  ]

  mainstat_6 = [
    (20, 2),
    (50, 3),
    (90, 4),
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  hp_8 = mainstat_6[:2] + [
    (90, 5),
    (lowlvlmax, 7),
    (MAXLVL, 8),
  ]

  allstat_5 = [
    (20, 1),
    (50, 2),
    (90, 3),
    (lowlvlmax, 4),
    (MAXLVL, 5),
  ]

  flat_mainstat_19 = [
    (20, 8),
    (40, 10),
    (50, 12),
    (70, 14),
    (90, 16),
    (lowlvlmax, 18),
    (MAXLVL, 19),
  ]

  flat_att_15 = [
    (20, 8),
    (50, 10),
    (90, 12),
    (lowlvlmax, 14),
    (MAXLVL, 15),
  ]

  flat_hp_310 = [(x, int(x*2.5)) for x in range(10, 120, 10)] + [
    (lowlvlmax, 300),
    (MAXLVL, 310),
  ]

  mainstat_8 = [
    (20, 3),
    (50, 4),
    (90, 5),
    (lowlvlmax, 7),
    (MAXLVL, 8),
  ]

  hp_11 = [
    (20, 3),
    (50, 5),
    (90, 7),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  allstat_6 = [
    (20, 2),
    (50, 3),
    (90, 4),
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  values_bonus = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_ATT_A: flat_att_3,
      FLAT_HP_A: flat_hp_60,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_11,
      FLAT_ATT_A: flat_att_11,
      FLAT_HP_A: flat_hp_125,
      MAINSTAT_A: mainstat_3,
      HP_A: mainstat_3,
      FLAT_ALLSTAT_A: flat_allstat_3,
    },

    EPIC: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_15,
      FLAT_ATT_A: flat_att_12,
      FLAT_HP_A: flat_hp_195,
      MAINSTAT_A: mainstat_5,
      HP_A: hp_6,
      ALLSTAT_A: allstat_3,
    },

    UNIQUE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_17,
      FLAT_ATT_A: flat_att_13,
      FLAT_HP_A: flat_hp_250,
      MAINSTAT_A: mainstat_6,
      HP_A: hp_8,
      ALLSTAT_A: allstat_5,
      MAINSTAT_PER_10_LVLS: 1,
    },

    LEGENDARY: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_19,
      FLAT_ATT_A: flat_att_15,
      FLAT_HP_A: flat_hp_310,
      MAINSTAT_A: mainstat_8,
      HP_A: hp_11,
      CRITDMG_A: 1,
      ALLSTAT_A: allstat_6,
      MAINSTAT_PER_10_LVLS: 2,
      COOLDOWN_1: 1,
      MESO_A: 5,
      DROP_A: 5,
    },
  }

  flat_hp_125_wse = [
    (20, 10),
    (50, 15),
    (90, 50),
    (lowlvlmax, 100),
    (MAXLVL, 125),
  ]

  values_bonus_wse = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_ATT_A: flat_att_6,
      FLAT_HP_A: flat_hp_60,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_13,
      FLAT_ATT_A: flat_att_13,
      FLAT_HP_A: flat_hp_125_wse,
      MAINSTAT_A: mpot_4,
      ATT_A: mpot_4,
      DAMAGE_A: mpot_4,
      HP_A: mainstat_3,
      FLAT_ALLSTAT_A: flat_allstat_6,
    },

    EPIC: {
      ANY: 1,
      MAINSTAT_A: mpot_7,
      ATT_A: mpot_7,
      DAMAGE_A: mpot_7,
      HP_A: hp_6,
      ALLSTAT_A: mpot_4,
      IED_C: 3,
    },

    UNIQUE: {
      ANY: 1,
      MAINSTAT_A: mpot_10,
      ATT_A: mpot_10,
      DAMAGE_A: mpot_10,
      HP_A: hp_8,
      ALLSTAT_A: mpot_7,
      BOSS_C: 12,
      IED_C: 4,
      MAINSTAT_PER_10_LVLS: 1,
    },

    LEGENDARY: {
      ANY: 1,
      MAINSTAT_A: mpot_13,
      ATT_A: mpot_13,
      DAMAGE_A: mpot_13,
      HP_A: hp_11,
      ALLSTAT_A: mpot_10,
      CRITDMG_A: 1,
      BOSS_C: 18,
      IED_C: 5,
      MAINSTAT_PER_10_LVLS: 2,
      ATT_PER_10_LVLS: 1,
    },
  }

  if cube == BONUS:
    if category & (WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING | EMBLEM):
      return values_bonus_wse
    else:
      return values_bonus
  elif cube == FAMILIAR or cube == RED_FAM_CARD:
    from familiars import values as values_familiar
    return values_familiar
  return values


forbidden_combos = [
  (1, [DECENTS, INVIN]),
  (2, [BOSS, IED, DROP]),
]


LINE_TYPE = 0
LINE_ONEIN = 1


# unused, only for debugging
def debug_print_combos(good, exit=True):
  a = np.dstack((good.types, good.values, good.onein, good.is_prime)).tolist()
  a = [[[Line(c[0]), c[1], c[2], c[3]] for c in x] for x in a]
  from pprint import pprint
  pprint(a)
  if exit:
    import sys
    sys.exit(0)


def cube_calc(wants, category, type, tier, level, region, lines):
  """
  calculate probability of rolling a combination of stats

  Parameters
  ----------
  wants : dict
    maps stats to the desired minimum amount.
    for example, {STAT: 6, CRITDMG: 8} means "8%+ crit dmg and 6+stat together"

    if the special key LINES is included, the probability of rolling any combination
    that contains wants[LINES] or more of any of the lines specified, and the amount is ignored.
    for example, {ATT_A: 1, BOSS: 1, LINES: 3} means
      "any combination of 3 lines of either att or boss"

  category : Category enum
    equip category. see the enum

  type : Cube enum
    cube type. see the enum

  tier : Tier enum
    the tier of the item. if the cube's tier limit is lower than this, it will be adjusted to the
    highest allowed

  level : int
    level of the item

  region : Region enum
    the game region. see the enum

  lines : dict
    maps tiers to lists of lists that contain the line type and probability. probability should be
    in the format of "one in x", meaning that 20 means 1/20 (5%).
    the line type is a Line enum.
    NOTE: this dict will be modified during the calculation for caching purposes and more keys
          will be added to it. if you need to reuse the data for other things, make a copy before
          passing it. the caching makes subsequent calls for the same data and cubes faster.
    example that also shows how to convert % probability to "one in"
    {
      UNIQUE: [
        [ATT_A, 1/7.5*100],
        [IED_C, 1/7.5*100],
      ],
      LEGENDARY: [
        [ATT_A, 1/5.7143*100],
        [IED_B, 1/5.7143*100],
        [IED_A, 1/5.7143*100],
      ],
    }
  """
  if type in tier_limits:
    tier = min(tier_limits[type], tier)

  lvals = find_line_values(type, category, region)

  def make_lines():
    # to represent all the lines we don't care about I generate an ANY line that
    # has 1-(sum of the chances of all lines we care about) chance
    def make_any_line(x):
      return x + [[ANY, 0]] # chance is calculated later

    res = make_any_line(lines[tier])
    num_primes = len(res)
    if (tier - 1) in lines:
      res += make_any_line(lines[tier - 1])
    return res, num_primes


  # the first time we are called for a certains set of lines, we convert the lines into numpy
  # arrays for each column (all types, all values, all probabilities, etc...). this is for
  # performance, since we want to filter based on certain columns and it's a lot faster if
  # we have the values packed together and we use numpy (which most likely uses vectorized
  # instructions).

  # the LineCache class holds these arrays and allows us to filter and reshape all of them at once.

  # the filt() method filters all the arrays through numpy fancy indexing on by passing either:
  # - an array of bools to filter out some elements. used to quickly filter out irrelevant lines
  # - an array of indices to replace with the elements, which could also be in a different shape
  #   than a flat array. used to go from a list of all the possible lines to a 2D array of all
  #   possible relevant line combinations

  # the copy() method creates a copy of the line cache so that we can store a LineCache of just
  # all the possible lines for subsequent calls, then copy it and filter every time without
  # affecting the cache object

  # because of how we store a line cache for each tier we're called with that also contains
  # lines for the lower tier, there will be some duplication. this is fine, it's nice to do it this
  # way for simplicity


  def cache_lines(cache):
    if tier not in cache:
      lines, num_prime = make_lines()

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


      def get_lval(tier, line):
        v = lvals[tier][line]
        if isinstance(v, list):
          for maxlvl, amt in v:
            if level <= maxlvl:
              return amt
          raise RuntimeError(f"failed to find {Tier(tier).name} {Line(line).name} "+
              f"for level {level}: {v}")
        return v


      types_col = col(LINE_TYPE)
      types_l = [Line(x) for x in types_col]
      values_list = [get_lval(tier, x) for x in types_l[:num_prime]]
      if (tier - 1) in lvals:
        values_list += [get_lval(tier - 1, x) for x in types_l[num_prime:]]
      values_col = np.array(values_list)
      is_prime_pn = np.concatenate((np.repeat(True, num_prime),
                                    np.repeat(False, len(types_col) - num_prime)))
      c = LineCache((types_col, values_col, col(LINE_ONEIN, 'float64'), is_prime_pn))
      c.filt(c.values != 0) # zero value means it's impossible at this lvl
      if tier not in cache:
        cache[tier] = {}
      cache[tier][level] = c
    else:
      c = cache[tier][level]

    return c


  # cache combos for each cube category called for these lines.
  # the category is mainly how many lines we're rolling and the prime/nonprime logic
  if LINE_CACHE not in lines:
    lines[LINE_CACHE] = {}
  if type in {FAMILIAR, RED_FAM_CARD}:
    cube_category = FAMILIAR
  else:
    cube_category = type if type in {VIOLET, UNI, EQUALITY} else RED
  if cube_category not in lines[LINE_CACHE]:
    lines[LINE_CACHE][cube_category] = {}
  line_cache = cache_lines(lines[LINE_CACHE][cube_category])

  # unicubes are 1/3rd the line chances because you roll 3 cubes on average to select
  chance_multiplier = 3 if type == UNI else 1

  prime_chance = prime_chances[type]
  if not isinstance(prime_chance, list):
    prime_chance = prime_chance[tier]

  # prime_chance = [prime_chance]
  prime_chance =         np.array(prime_chance, dtype='float64') .reshape(1, -1)
  nonprime_chance = (1 - np.array(prime_chance, dtype='float64')).reshape(1, -1)

  def combo_chance(want):
    for x in want.keys():
      if x not in LineMasks and x not in Line:
        raise RuntimeError(f"desired stat {x} not in LineMasks or Line")

    c = line_cache.copy()

    # filter out lines that are not in our want dict to exponentially reduce combinations
    relevant_line_bits = reduce(or_, want.keys()) | ANY
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

    if cube_category == VIOLET:
      combo_idxs = np.array(np.meshgrid(p, n, n, n, n, n)).T.reshape(-1, 6)
    elif cube_category == UNI:
      combo_idxs = np.array(np.meshgrid(n)).T.reshape(-1, 1)
    elif cube_category == EQUALITY:
      combo_idxs = np.array(np.meshgrid(p, p, p)).T.reshape(-1, 3)
    elif cube_category == FAMILIAR:
      if type == FAMILIAR:
        n = n[len(p):] # prevent division by 0
      combo_idxs = np.array(np.meshgrid(p, n)).T.reshape(-1, 2)
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

    # note: line types are a bitmask so that we can check for multiple line types in one operation
    #       by just ANDing by a bit mask of all the types we want.

    #       this is also useful to match multiple lines later. for example
    #       when we look for stat we also want to match allstat so we can check that
    #       line_type & (MAINSTAT_A | ALLSTAT_A) != 0

    for n, forbidden in forbidden_combos:
      if np.any(c.types & reduce(or_, forbidden) != 0):
        mask = reduce(or_, [np.count_nonzero(c.types & x != 0, axis=1) > n for x in forbidden])
        c.filt(np.logical_not(mask))

    if LINES in want:
      # all combinations that contains at least n lines of any of the stats specified
      # TODO: allow specifying minimum amount for the lines
      mask = np.count_nonzero(c.types & (relevant_line_bits & ~ANY) != 0, axis=1) >= want[LINES]
    else:
      # all combinations that contain all of the stats and with at least the requested amt.
      mask = reduce(and_, [np.sum(c.values * (c.types & x != 0).astype(int), axis=1) >= want[x]
                           for x in want.keys()])

    good = c.filt(mask)

    # adjust the probability of prime lines by their prime chance,
    # and the probability of non-prime lines by the inverse of the prime chance.
    # this way, the sum of all proababilities of prime and non-prime lines will add up to 1
    good.onein /= np.where(good.is_prime, np.repeat(prime_chance, len(good.onein), axis=0),
                           np.repeat(nonprime_chance, len(good.onein), axis=0))

    return sum(np.prod(1/(good.onein * chance_multiplier), axis=1))

  return sum([combo_chance(want) for want in wants]), tier
