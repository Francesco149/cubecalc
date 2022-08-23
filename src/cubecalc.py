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

NOTE: for simplicity, all the values use lvl<160 lines, so for example
      30% att means 12 9 9 and it's the same as 33% on a lvl 160+ item
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


line_values = {
  COMMON: {
    ANY: 0,
    FLAT_MAINSTAT: 6,
    FLAT_HP: 60,
    FLAT_ATT: 6,
  },

  RARE: {
    ANY: 0,
    FLAT_MAINSTAT: 12,
    FLAT_HP: 120,
    FLAT_ATT: 12,
    MAINSTAT: 3,
    HP: 3,
    FLAT_ALLSTAT: 5,
    ATT: 3,
    DAMAGE: 3,
    IED_15: 15,
  },

  EPIC: {
    ANY: 0,
    MAINSTAT: 6,
    ALLSTAT: 3,
    HP: 6,
    INVIN: 1,
    ATT: 6,
    DAMAGE: 6,
    IED_15: 15,
  },

  UNIQUE: {
    BOSS_30: 30,
    IED_30: 30,
    ATT: 9,
    DAMAGE: 9,
    ANY: 0,
    MAINSTAT: 9,
    ALLSTAT: 6,
    HP: 9,
    INVIN: 2,
    DECENT_SHARP_EYES: 1,
  },

  LEGENDARY: {
    BOSS_30: 30,
    BOSS_35: 35,
    BOSS_40: 40,
    IED_30: 30,
    IED_35: 35,
    IED_40: 40,
    ATT: 12,
    DAMAGE: 12,
    ANY: 0,
    MAINSTAT: 12,
    ALLSTAT: 9,
    HP: 12,
    COOLDOWN_2: 2,
    COOLDOWN_1: 1,
    CRITDMG: 8,
    MESO: 20,
    DROP: 20,
    INVIN: 3,
    DECENT_SPEED_INFUSION: 1,
    DECENT_COMBAT_ORDERS: 1,
  },
}


line_values_bonus = {
  COMMON: {
    ANY: 0,
    FLAT_MAINSTAT: 6,
    FLAT_ATT: 3,
    FLAT_HP: 60,
  },

  RARE: {
    ANY: 0,
    FLAT_MAINSTAT: 11,
    FLAT_ATT: 10,
    FLAT_HP: 100,
    MAINSTAT: 3,
    HP: 2,
    FLAT_ALLSTAT: 3,
  },

  EPIC: {
    ANY: 0,
    FLAT_MAINSTAT: 14,
    FLAT_ATT: 11,
    FLAT_HP: 180,
    MAINSTAT: 4,
    HP: 5,
    ALLSTAT: 3,
  },

  UNIQUE: {
    ANY: 0,
    FLAT_MAINSTAT: 16,
    FLAT_ATT: 12,
    FLAT_HP: 240,
    MAINSTAT: 5,
    HP: 7,
    ALLSTAT: 4,
    #MAINSTAT_PER_10_LVLS: 1,
  },

  LEGENDARY: {
    ANY: 0,
    FLAT_MAINSTAT: 18,
    FLAT_ATT: 14,
    FLAT_HP: 300,
    MAINSTAT: 7,
    HP: 10,
    CRITDMG: 1,
    ALLSTAT: 5,
    #MAINSTAT_PER_10_LVLS: 2,
    COOLDOWN_1: 1,
    MESO: 5,
    DROP: 5,
  },
}

line_values_bonus_wse = {
  COMMON: {
    ANY: 0,
    FLAT_MAINSTAT: 6,
    FLAT_ATT: 6,
    FLAT_HP: 60,
  },

  RARE: {
    ANY: 0,
    FLAT_MAINSTAT: 12,
    FLAT_ATT: 12,
    FLAT_HP: 100,
    MAINSTAT: 3,
    ATT: 3,
    DAMAGE: 3,
    HP: 2,
    FLAT_ALLSTAT: 5,
  },

  EPIC: {
    ANY: 0,
    MAINSTAT: 6,
    ATT: 6,
    DAMAGE: 6,
    HP: 5,
    ALLSTAT: 3,
    IED_3: 3,
  },

  UNIQUE: {
    ANY: 0,
    MAINSTAT: 9,
    ATT: 9,
    DAMAGE: 9,
    HP: 7,
    ALLSTAT: 6,
    BOSS_12: 12,
    IED_4: 4,
    #MAINSTAT_PER_10_LVLS: 1,
  },

  LEGENDARY: {
    ANY: 0,
    MAINSTAT: 12,
    ATT: 12,
    DAMAGE: 12,
    HP: 10,
    ALLSTAT: 9,
    CRITDMG: 1,
    BOSS_18: 18,
    IED_5: 5,
    #MAINSTAT_PER_10_LVLS: 2,
    #ATT_PER_10_LVLS: 1,
  },
}


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


def cube_calc(wants, category, type, tier, lines):
  """
  calculate probability of rolling a combination of stats

  Parameters
  ----------
  wants : dict
    maps stats to the desired minimum amount.
    for example, {STAT: 6, CRITDMG: 8} means "8%+ crit dmg and 6+stat together"

    if the special key LINES is included, the probability of rolling any combination
    that contains wants[LINES] or more of any of the lines specified, and the amount is ignored.
    for example, {ATT: 1, BOSS: 1, LINES: 3} means
      "any combination of 3 lines of either att or boss"

  category : Category enum
    equip category. see the enum

  type : Cube enum
    cube type. see the enum

  tier : Tier enum
    the tier of the item. if the cube's tier limit is lower than this, it will be adjusted to the
    highest allowed

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
        [ATT, 1/7.5*100],
        [IED_30, 1/7.5*100],
      ],
      LEGENDARY: [
        [ATT, 1/5.7143*100],
        [IED_35, 1/5.7143*100],
        [IED_40, 1/5.7143*100],
      ],
    }
  """
  if type in tier_limits:
    tier = min(tier_limits[type], tier)

  lvals = line_values
  if type == BONUS:
    if category & (WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING | EMBLEM):
      lvals = line_values_bonus_wse
    else:
      lvals = line_values_bonus


  def make_lines():
    # to represent all the lines we don't care about I generate an ANY line that
    # has 1-(sum of the chances of all lines we care about) chance
    def make_any_line(x):
      return x + [[ANY, 0]] # chance is calculated later

    lines_prime = make_any_line(lines[tier])
    return lines_prime + make_any_line(lines[tier - 1]), len(lines_prime)


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

      types_col = col(LINE_TYPE)
      types_l = [Line(x) for x in types_col]
      values_col = np.array(
        [lvals[tier][x] for x in types_l[:num_prime]] +
        [lvals[tier - 1][x] for x in types_l[num_prime:]]
      )
      is_prime_pn = np.concatenate((np.repeat(True, num_prime),
                                    np.repeat(False, len(types_col) - num_prime)))
      c = LineCache((types_col, values_col, col(LINE_ONEIN, 'float64'), is_prime_pn))
      cache[tier] = c
    else:
      c = cache[tier]

    return c


  # cache combos for each cube category called for these lines.
  # the category is mainly how many lines we're rolling and the prime/nonprime logic
  if LINE_CACHE not in lines:
    lines[LINE_CACHE] = {}
  category = type if type in {VIOLET, UNI, EQUALITY} else RED
  if category not in lines[LINE_CACHE]:
    lines[LINE_CACHE][category] = {}
  line_cache = cache_lines(lines[LINE_CACHE][category])

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

    if category == VIOLET:
      combo_idxs = np.array(np.meshgrid(p, n, n, n, n, n)).T.reshape(-1, 6)
    elif category == UNI:
      combo_idxs = np.array(np.meshgrid(n)).T.reshape(-1, 1)
    elif category == EQUALITY:
      combo_idxs = np.array(np.meshgrid(p, p, p)).T.reshape(-1, 3)
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
    #       line_type & (MAINSTAT | ALLSTAT) != 0

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
