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

tier_limits = {
  OCCULT: EPIC,
  MASTER: UNIQUE,
}

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
  COMMON: { ANY: 0 },

  RARE: {
    ATT: 3,
    ANY: 0,
    MAINSTAT: 3,
    HP: 3,
    IED_15: 15,
  },

  EPIC: {
    ATT: 6,
    ANY: 0,
    MAINSTAT: 6,
    ALLSTAT: 3,
    HP: 6,
    INVIN: 1,
    IED_15: 15,
  },

  UNIQUE: {
    BOSS_30: 30,
    IED_30: 30,
    ATT: 9,
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


def cube_calc(wants, type, tier, lines):
  if type in tier_limits:
    tier = min(tier_limits[type], tier)


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

    forbidden = [DECENTS, INVIN]
    if np.any(c.types & reduce(or_, forbidden) != 0):
      mask = reduce(or_, [np.count_nonzero(c.types & x != 0, axis=1) > 1 for x in forbidden])
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
