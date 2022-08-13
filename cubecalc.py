#!/usr/bin/env python3

from functools import reduce, partial
from operator import mul, or_, and_, add
import numpy as np
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

from common import *
from data.utils import percent

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

LINE_TYPE = 0
LINE_ONEIN = 1

# data pre-processing. lots of unnecessary redundancy here that I should fix
# this is all glue that replaces the previously hardcoded probability tables
import data.kms as kms
import data.tms as tms

for k, v in kms.cash.items():
  v[DEFAULT_CUBE] = [RED, BLACK]

for k, v in kms.noncash.items():
  v[DEFAULT_CUBE] = MEISTER

for k, v in kms.bonus.items():
  v[DEFAULT_CUBE] = BONUS

for x in [kms.cash, kms.noncash, kms.bonus]:
  for k, v in x.items():
    v[NAME] = category_name(k)

empty_tiers = {x: [] for x in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]}

def find_probabilities(data, cubes_mask, categories_mask):
  # find all the dicts that match both the desired cubes and categories and merge them
  cubedatas = [v for k, v in data.items() if k & cubes_mask]
  probabilities = reduce(add, [[v for k, v in x.items() if k & categories_mask] for x in cubedatas])
  info = {
    NAME: category_name(categories_mask),
    DEFAULT_CUBE: [x for x in Cube if x & cubes_mask],
  }
  return empty_tiers | info | reduce(or_, probabilities, {})

weapon = kms.cash[WEAPON]
secondary = kms.cash[SECONDARY]
emblem = kms.cash[EMBLEM]
top_overall = kms.cash[TOP_OVERALL]
bottom = kms.cash[BOTTOM]
hat = kms.cash[HAT]
accessory = kms.cash[FACE_EYE_RING_EARRING_PENDANT]

weapon_noncash = kms.noncash[WEAPON]
secondary_noncash = kms.noncash[SECONDARY]
emblem_noncash = kms.noncash[EMBLEM]
top_overall_noncash = kms.noncash[TOP_OVERALL]
bottom_noncash = kms.noncash[BOTTOM]
hat_noncash = kms.noncash[HAT]
accessory_noncash = kms.noncash[FACE_EYE_RING_EARRING_PENDANT]

weapon_bonus = kms.bonus[WEAPON]
secondary_bonus = kms.bonus[SECONDARY]
emblem_bonus = kms.bonus[EMBLEM]

# note: w/s and force shield/soul ring should not be together if we're gonna go below uniq

prob_ve = partial(find_probabilities, tms.event, VIOLET | EQUALITY)
weapon_secondary_violet_equality = prob_ve(WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING)
emblem_violet_equality = prob_ve(EMBLEM)
accessory_violet_equality = prob_ve(FACE_EYE_RING_EARRING_PENDANT)
cape_belt_shoulder_violet_equality = prob_ve(CAPE_BELT_SHOULDER)
shoe_violet_equality = prob_ve(SHOE)
glove_violet_equality = prob_ve(GLOVE)
bottom_violet_equality = prob_ve(BOTTOM)
top_overall_violet_equality = prob_ve(TOP_OVERALL)
hat_violet_equality = prob_ve(HAT)

prob_uni = partial(find_probabilities, tms.event, UNI)
weapon_secondary_uni = prob_uni(WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING)
emblem_uni = prob_uni(EMBLEM)
accessory_uni = prob_uni(FACE_EYE_RING_EARRING_PENDANT)
cape_belt_shoulder_uni = prob_uni(CAPE_BELT_SHOULDER)
shoe_uni = prob_uni(SHOE)
glove_uni = prob_uni(GLOVE)
bottom_uni = prob_uni(BOTTOM)
top_overall_uni = prob_uni(TOP_OVERALL)
hat_uni = prob_uni(HAT)

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
    INVIN: 1,
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
