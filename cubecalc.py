#!/usr/bin/env python

from itertools import product
from functools import reduce
from functools import partial
from operator import mul

BOSS = "boss"
IED = "ied"
ATT = "att"
ANY = "any"
STAT = "stat"
ALLSTAT = "allstat"
HP = "hp"
COOLDOWN = "cooldown"
CRITDMG = "critdmg"
LINES = "match by number of lines and what lines are allowed"

COMMON = 0
RARE = 1
EPIC = 2
UNIQUE = 3
LEGENDARY = 4

DEFAULT_TIER = LEGENDARY

RED = "red"
MEISTER = "meister"
BLACK = "black"
VIOLET = "violet"
EQUALITY = "equality"
BONUS = "bonus"
OCCULT = "occult"
UNI = "uni"

COMBOS = "combos"
COMBOS_VIOLET = "combos (violet)"
NAME = "name"
DEFAULT_CUBE = "default cube"

lines_base = { COMBOS: None }

prime_chances = {
  RED: [1, 0.1, 0.01],
  MEISTER: [1, 0.001996, 0.001996],
  BLACK: [1, 0.2, 0.05],
  VIOLET: [1, 0.1, 0.01, 0.01, 0.1, 0.01],
  EQUALITY: [1, 1, 1],
  BONUS: [1, 0.004975, 0.004975],
  OCCULT: [1] + [1.0/101]*2,
  UNI: 0.15,
}

weapon = {
  NAME: "weapon",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    (BOSS, 30, 14.3333),
    (IED,  30, 14.3333),
    (ATT,   9, 14.3333),
  ],
  
  LEGENDARY: [
    (BOSS, 40, 20.5),
    (BOSS, 35, 20.5),
    (BOSS, 30, 20.5),
    (IED,  40, 20.5),
    (IED,  35, 20.5),
    (ATT,  12, 20.5),
  ],

}

weapon_noncash = {
  NAME: "weapon",
  DEFAULT_CUBE: MEISTER,

  UNIQUE: [
    (BOSS, 30, 15),
    (IED,  30, 15),
    (ATT,   9, 15),
  ],

  LEGENDARY: [
    (BOSS, 40, 36),
    (BOSS, 35, 18),
    (BOSS, 30, 18),
    (IED,  40, 36),
    (IED,  35, 18),
    (ATT,  12, 18),
  ],
  
}

secondary = {
  NAME: "secondary",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    (BOSS, 30, 17.0),
    (IED,  30, 17.0),
    (ATT,   9, 17.0),
  ],

  LEGENDARY: [
    (BOSS, 40, 23.5),
    (BOSS, 35, 23.5),
    (BOSS, 30, 23.5),
    (IED,  40, 23.5),
    (IED,  35, 23.5),
    (ATT,  12, 23.5),
  ],

}

secondary_noncash = {
  NAME: "secondary",
  DEFAULT_CUBE: MEISTER,

  UNIQUE: [
    (BOSS, 30, 21),
    (IED,  30, 21),
    (ATT,   9, 21),
  ],

  LEGENDARY: [
    (BOSS, 40, 24),
    (BOSS, 35, 24),
    (BOSS, 30, 48),
    (IED,  40, 48),
    (IED,  35, 24),
    (ATT,  12, 24),
  ],
  
}

emblem = {
  NAME: "emblem",
  DEFAULT_CUBE: [RED, BLACK],

  LEGENDARY: [
    (IED,  40, 17.5),
    (IED,  35, 17.5),
    (ATT,  12, 17.5),
  ],

  UNIQUE: [
    (IED,  30, 13.3333),
    (ATT,   9, 13.3333),
  ],

}

emblem_noncash = {
  NAME: "emblem",
  DEFAULT_CUBE: MEISTER,

  UNIQUE: [
    (IED,  30, 14),
    (ATT,   9, 14),
  ],

  LEGENDARY: [
    (IED,  40, 15.5),
    (IED,  35, 31),
    (ATT,  12, 15.5),
  ],
  
}

weapon_bonus = {
  NAME: "weapon",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    (ATT, 9, 21.5),
  ],

  LEGENDARY: [
    (ATT, 12, 19.5),
  ],
  
}

secondary_bonus = {
  NAME: "secondary",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    (ATT, 9, 21.5),
  ],

  LEGENDARY: [
    (ATT, 12, 20.5),
  ],
  
}

emblem_bonus = {
  NAME: "emblem",
  DEFAULT_CUBE: BONUS,

  UNIQUE: [
    (ATT, 9, 21),
  ],

  LEGENDARY: [
    (ATT, 12, 19),
  ],

}

top_overall = {
  NAME: "top/overall",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    (STAT, 9, 13.2),
    (HP, 9, 11),
    (ALLSTAT, 6, 16.5),
  ],

  LEGENDARY: [
    (STAT, 12, 10.75),
    (ALLSTAT, 9, 10.75),
    (HP, 12, 10.75),
  ],

}

top_overall_noncash = {
  NAME: "top/overall",
  DEFAULT_CUBE: MEISTER,

  UNIQUE: [
    (STAT, 9, 16.5),
    (HP, 9, 11),
    (ALLSTAT, 6, 33),
  ],

  LEGENDARY: [
    (STAT, 12, 17),
    (ALLSTAT, 9, 17),
    (HP, 12, 11.3333),
  ],
  
}

hat = {
  NAME: "hat",
  DEFAULT_CUBE: [RED, BLACK],

  UNIQUE: [
    (STAT, 9, 11.2),
    (HP, 9, 9.3333),
    (ALLSTAT, 6, 14),
  ],

  LEGENDARY: [
    (STAT, 12, 11.25),
    (HP, 12, 11.25),
    (ALLSTAT, 9, 15),
    (COOLDOWN, 1, 15),
    (COOLDOWN, 2, 22.5),
  ],
  
}

hat_noncash = {
  NAME: "hat",
  DEFAULT_CUBE: MEISTER,

  UNIQUE: [
    (STAT, 9, 14.5),
    (HP, 9, 9.6666),
    (ALLSTAT, 6, 29),
  ],

  LEGENDARY: [
    (STAT, 12, 18),
    (HP, 12, 12),
    (ALLSTAT, 9, 18),
    (COOLDOWN, 1, 12),
    (COOLDOWN, 2, 18),
  ],
  
}

accessory_noncash = {
  NAME: "accessory",
  DEFAULT_CUBE: MEISTER,

  RARE: [
    (STAT, 3, 21),
    (HP, 3, 14),
  ],

  EPIC: [
    (STAT, 6, 9),
    (HP, 6, 6),
    (ALLSTAT, 3, 18),
  ],
}

# TMS cubes
# https://tw.beanfun.com/beanfuncommon/EventAD_Mobile/EventAD.aspx?EventADID=8421

weapon_secondary_violet_equality = {
  NAME: "weapon",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (BOSS, 30, 1/6.52*100),
    (ATT, 9, 1/6.52*100),
    (IED, 30, 1/8.7*100),
  ],

  LEGENDARY: [
    (BOSS, 40, 1/4.44*100),
    (BOSS, 35, 1/4.44*100),
    (BOSS, 30, 1/4.44*100),
    (ATT, 12, 1/4.44*100),
    (IED, 40, 1/6.67*100),
    (IED, 35, 1/6.67*100),
  ],
  
}

emblem_violet_equality = {
  NAME: "emblem",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (ATT, 9, 1/6.98*100),
    (IED, 30, 1/9.3*100),
  ],

  LEGENDARY: [
    (ATT, 12, 1/5.13*100),
    (IED, 40, 1/7.69*100),
    (IED, 35, 1/7.69*100),
  ],

}

weapon_secondary_uni = {
  NAME: "weapon/secondary",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (BOSS, 30, 1/5.48*100),
    (ATT, 9, 1/8.22*100),
    (IED, 30, 1/20.55*100),
  ],

  LEGENDARY: [
    (BOSS, 40, 1/1.13*100),
    (BOSS, 35, 1/2.10*100),
    (BOSS, 30, 1/3.07*100),
    (ATT, 12, 1/3.24*100),
    (IED, 40, 1/16.18*100),
    (IED, 35, 1/25.89*100),
  ],

}

emblem_uni = {
  NAME: "emblem",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (ATT, 9, 1/8.7*100),
    (IED, 30, 1/21.74*100),
  ],

  LEGENDARY: [
    (ATT, 12, 1/3.45*100),
    (IED, 40, 1/17.27*100),
    (IED, 35, 1/27.63*100),
  ],

}

# pendants, rings, face, eye, earrings
accessory_violet_equality = {
  NAME: "accessory",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/9.8*100),
    (HP, 9, 1/11.76*100),
    (ALLSTAT, 6, 1/7.84*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/7.84*100),
    (ALLSTAT, 9, 1/5.88*100),
    (HP, 12, 1/7.84*100),
  ],
  
}

accessory_uni = {
  NAME: "accessory",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/11.63*100),
    (HP, 9, 1/11.63*100),
    (ALLSTAT, 6, 1/2.33*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/6.06*100),
    (ALLSTAT, 9, 1/1.52*100),
    (HP, 12, 1/6.06*100),
  ],
  
}

cape_belt_shoulder_violet_equality = {
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/8.47*100),
    (HP, 9, 1/10.17*100),
    (ALLSTAT, 6, 1/6.78*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/8.89*100),
    (HP, 12, 1/8.89*100),
    (ALLSTAT, 9, 1/6.67*100),
  ],
  
}

cape_belt_shoulder_uni = {
  NAME: "cape/belt/shoulder",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/7.69*100),
    (HP, 9, 1/7.69*100),
    (ALLSTAT, 6, 1/1.54*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/8.89*100),
    (HP, 12, 1/8.89*100),
    (ALLSTAT, 9, 1/6.67*100),
  ],
  
}

shoe_violet_equality = {
  NAME: "shoe",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/7.94*100),
    (HP, 9, 1/9.52*100),
    (ALLSTAT, 6, 1/6.35*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/8.33*100),
    (HP, 12, 1/8.33*100),
    (ALLSTAT, 9, 1/6.25*100),
  ],

}

shoe_uni = {
  NAME: "shoe",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/6.33*100),
    (HP, 9, 1/6.33*100),
    (ALLSTAT, 6, 1/1.27*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/7.27*100),
    (HP, 12, 1/7.27*100),
    (ALLSTAT, 9, 1/1.82*100),
  ],
  
}

glove_violet_equality = {
  NAME: "glove",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/7.46*100),
    (HP, 9, 1/8.96*100),
    (ALLSTAT, 6, 1/5.97*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/7.69*100),
    (HP, 12, 1/7.69*100),
    (ALLSTAT, 9, 1/5.77*100),
    (CRITDMG, 8, 1/7.69*100),
  ],
  
}

glove_uni = {
  NAME: "glove",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/5.26*100),
    (HP, 9, 1/5.26*100),
    (ALLSTAT, 6, 1/1.05*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/5.8*100),
    (HP, 12, 1/5.8*100),
    (ALLSTAT, 9, 1/1.45*100),
    (CRITDMG, 8, 1/2.9*100),
  ],
  
}

bottom_violet_equality = {
  NAME: "bottom",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/7.94*100),
    (HP, 9, 1/9.52*100),
    (ALLSTAT, 6, 1/6.35*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/8.89*100),
    (HP, 12, 1/8.89*100),
    (ALLSTAT, 9, 1/6.67*100),
  ],
  
}

bottom_uni = {
  NAME: "bottom",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/6.35*100),
    (HP, 9, 1/6.35*100),
    (ALLSTAT, 6, 1/1.59*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/8.89*100),
    (HP, 12, 1/8.89*100),
    (ALLSTAT, 9, 1/2.22*100),
  ],
  
}

top_overall_violet_equality = {
  NAME: "top/overall",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/6.85*100),
    (HP, 9, 1/8.22*100),
    (ALLSTAT, 6, 1/5.48*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/7.84*100),
    (HP, 12, 1/7.84*100),
    (ALLSTAT, 9, 1/5.88*100),
  ],
  
}

top_overall_uni = {
  NAME: "top/overall",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/4.08*100),
    (HP, 9, 1/4.08*100),
    (ALLSTAT, 6, 1/1.02*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/6.15*100),
    (HP, 12, 1/6.15*100),
    (ALLSTAT, 9, 1/1.54*100),
  ],
  
}

hat_violet_equality = {
  NAME: "hat",
  DEFAULT_CUBE: [VIOLET, EQUALITY],

  UNIQUE: [
    (STAT, 9, 1/7.94*100),
    (HP, 9, 1/9.52*100),
    (ALLSTAT, 6, 1/6.35*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/7.55*100),
    (HP, 12, 1/7.55*100),
    (ALLSTAT, 9, 1/5.66*100),
    (COOLDOWN, 2, 1/3.77*100),
    (COOLDOWN, 1, 1/5.66*100),
  ],
  
}

hat_uni = {
  NAME: "hat",
  DEFAULT_CUBE: UNI,

  UNIQUE: [
    (STAT, 9, 1/5.8*100),
    (HP, 9, 1/5.8*100),
    (ALLSTAT, 6, 1/1.45*100),
  ],

  LEGENDARY: [
    (STAT, 12, 1/5.0*100),
    (HP, 12, 1/5.0*100),
    (ALLSTAT, 9, 1/1.25*100),
    (COOLDOWN, 2, 1/10.0*100),
    (COOLDOWN, 1, 1/10.0*100),
  ],
  
}

# ---------------------------------------------------------------------------------------------------------

def filter_impossible_lines(combos):
  for combo in combos:
    counts = {BOSS: 0, IED: 0}
    for (_, t, _, _) in combo:
      if t in counts:
        counts[t] += 1
    for x in counts.values():
      if x > 2:
        break
    else:
      yield combo


def tabulate(rows):
  max_len = max((len(text) for (text, _) in rows))
  for (text, result) in rows:
    print(f"{text.rjust(max_len)} {result}")


def mklines(prime, lines):
  return [(prime, typ, amt, onein) for (typ, amt, onein) in lines]


def fmt_chance(text, wants, combos, combo_chance):
  chance = sum([combo_chance(want, combos) for want in wants])
  return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")


def unicube_calc(print_combos, lines, tier=DEFAULT_TIER):
  print(f" {lines[NAME]}: 2l->3l by rerolling 2nd or 3rd line (unicube) ".center(80, "="))

  prime_chance = prime_chances[UNI]
  lines = mklines(False, lines[tier - 1]) + mklines(True, lines[tier])

  def combo_chance(want, _combos):
    # _combos is unused arg, I need to refactor fmt_chance
    want_stat = list(want.keys())[0]
    want_value = want[want_stat]
    eligible_lines = [(prime, stat, value, onein) for (prime, stat, value, onein) in lines
                      if (stat == want_stat or (stat == ALLSTAT and want_stat == STAT)) and value >= want_value]
    return sum([1/onein * (prime_chance if prime else (1 - prime_chance))
                for (prime, _, _, onein) in eligible_lines]) / 3
    # divide by 3 because 3 cubes avg to select line, and then you reroll the line without spending an extra cube

  tabulate([fmt_chance(text, want, [], combo_chance) for (text, want) in print_combos])


def __cube_calc(print_combos, lines, type, tier):
  if type == UNI:
    unicube_calc(print_combos, lines, tier)
    return

  print(f" {lines[NAME]} ({type}) ".center(80, "="))

  prime_chance = prime_chances[type]

  if type == OCCULT:
    tier = min(EPIC, tier)

  def make_any_line(prime, lines):
    lines = mklines(prime, lines)
    return lines + [(prime, ANY, 0, 1.0/(1.0 - sum((1.0/onein for (_, _, _, onein) in lines))))]

  # to represent all the lines we don't care about I generate an ANY line that
  # has 1-(sum of the chances of all lines we care about) chance
  p = make_any_line(True, lines[tier])
  n = make_any_line(False, lines[tier - 1]) + p

  combos_i = COMBOS_VIOLET if type == VIOLET else COMBOS

  # cache combos for each set of lines
  if combos_i not in lines:
    if type == VIOLET:
      lines[combos_i] = product(p, n, n, n, n, n)
    else:
      lines[combos_i] = product(p, n, n)

    lines[combos_i] = list(filter_impossible_lines(lines[combos_i]))

  combos = lines[combos_i]

  def combo_chance(want, combos):
    good=set()
    if LINES in want:
      # we are looking for all combinations that contains at least n lines of any of the stats specified
      for combo in combos:
        lines = 0
        for (prime, typ, amount, onein) in combo:
          if typ == ALLSTAT and typ not in want:
            typ = STAT
          if typ in want and amount >= want[typ]:
            lines += 1
        if lines >= want[LINES]:
          good.add(combo)
    else:
      for combo in combos:
        amounts = {}
        for (prime, typ, amount, onein) in combo:
          if typ not in amounts: amounts[typ] = 0
          amounts[typ] += amount
        if ALLSTAT in amounts and STAT in amounts:
          amounts[STAT] += amounts[ALLSTAT]
        for k in want.keys():
          if k not in amounts or amounts[k] < want[k]:
            break
        else:
          good.add(combo)

    # for any lines that can be both prime and non-prime, we need to adjust the probability of prime lines
    # by their prime chance, and the probability of non-prime lines by the inverse of the prime chance.
    # this way, the sum of all proababilities of prime and non-prime lines will add up to 1

    return sum([reduce(mul, [(1.0/onein) * (prime_chance[i] if prime else (1 - prime_chance[i]))
      for i, (prime, typ, amount, onein) in enumerate(combo)]) for combo in good])

  def fmt_chance(text, wants, combos):
    chance = sum([combo_chance(want, combos) for want in wants])
    return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

  tabulate([fmt_chance(text, want, combos) for (text, want) in print_combos])


def single_or_list(x):
  return x if isinstance(x, list) else [x]


def cube_calc(print_combos, lines, types=[], tier=DEFAULT_TIER):
  if not types:
    types = lines[DEFAULT_CUBE]
  for type in single_or_list(types):
    __cube_calc(print_combos, lines, type, tier)


class Combos:
  def __init__(self, combos):
    self.calc = partial(cube_calc, combos)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    pass


def cube_calcs():
  combos_ws = [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
    ("21+ att and boss", [{ATT: 21, BOSS: 1}]),
    ("21+ att and ied", [{ATT: 21, IED: 1}]),
    ("18+ att and boss", [{ATT: 18, BOSS: 1}]),
    ("18+ att and ied", [{ATT: 18, IED: 1}]),
    ("any 2l combo of att+boss", [{ATT: 1, BOSS: 1, LINES: 2}]),
    ("any 2l combo of att+boss+ied", [{ATT: 1, BOSS: 1, IED: 1, LINES: 2}]),
    ("any 3l combo of att+boss", [{ATT: 1, BOSS: 1, LINES: 3}]),
    ("any 3l combo of att+boss+ied", [{ATT: 1, BOSS: 1, IED: 1, LINES: 3}]),
    ("60+ied", [{IED: 60}]),
    ("70+ied", [{IED: 70}]),
    ("60+ied and att", [{IED: 60, ATT: 1}]),
    ("60+ied and boss", [{IED: 60, BOSS: 1}]),
  ]

  combos_e = [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
    ("21+ att and ied", [{ATT: 21, IED: 1}]),
    ("any 2l combo of att+ied", [{ATT: 1, IED: 1, LINES: 2}]),
    ("any 3l combo of att+ied", [{ATT: 1, IED: 1, LINES: 3}]),
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

  with Combos(combos_ws) as c:
    c.calc(weapon)
    c.calc(weapon_noncash)
    c.calc(secondary)
    c.calc(secondary_noncash)
    c.calc(weapon_secondary_violet_equality)

  with Combos(combos_e) as c:
    c.calc(emblem)
    c.calc(emblem_noncash)
    c.calc(emblem_violet_equality)

  with Combos(combos_wse_b) as c:
    c.calc(weapon_bonus)
    c.calc(secondary_bonus)
    c.calc(emblem_bonus)

  with Combos(combos_stat) as c:
    c.calc(top_overall)
    c.calc(top_overall_noncash)
    c.calc(top_overall_violet_equality)
    c.calc(accessory_violet_equality)
    c.calc(cape_belt_shoulder_violet_equality)
    c.calc(shoe_violet_equality)
    c.calc(bottom_violet_equality)

  with Combos(combos_hat) as c:
    c.calc(hat)
    c.calc(hat_noncash)
    c.calc(hat_violet_equality)

  with Combos(combos_occult_stat) as c:
    c.calc(accessory_noncash, OCCULT)

  with Combos(combos_glove) as c:
    c.calc(glove_violet_equality)


def unicube_calcs():
  combos_uni_e_prime = [
    ("12 att", [{ATT: 12}]),
    ("40 ied", [{IED: 40}]),
    ("35+ ied", [{IED: 35}]),
  ]

  combos_uni_e_nonprime = [
    ("9+ att or 30+ ied", [{ATT: 9}, {IED: 30}]),
    ("9+ att", [{ATT: 9}]),
    ("30+ ied", [{IED: 30}]),
  ]

  combos_uni_ws_prime = [
    ("35+ boss", [{BOSS: 35}]),
    ("40 boss", [{BOSS: 40}]),
  ] + combos_uni_e_prime

  combos_uni_ws_nonprime = [
    ("9+ att or 30+ boss or 30+ ied", [{ATT: 9}, {BOSS: 30}, {IED: 30}]),
    ("9+ att or 30+ boss", [{ATT: 9}, {BOSS: 30}]),
    ("30+ boss", [{BOSS: 30}]),
  ] + combos_uni_e_nonprime

  combos_uni_e = combos_uni_e_nonprime + combos_uni_e_prime
  combos_uni_ws = combos_uni_ws_nonprime + combos_uni_ws_prime

  combos_uni_stat_prime = [
    ("12 stat", [{STAT: 12}]),
    ("12 hp", [{HP: 12}]),
    ("9 allstat", [{ALLSTAT: 9}]),
  ]

  combos_uni_stat_nonprime = [
    ("6+ stat", [{STAT: 6}]),
    ("9+ stat", [{STAT: 9}]),
    ("9+ hp", [{HP: 9}]),
    ("6 allstat", [{ALLSTAT: 6}]),
  ]

  combos_uni_hat_prime = combos_uni_stat_prime + [
    ("1+s cooldown", [{COOLDOWN: 1}]),
    ("2s cooldown", [{COOLDOWN: 2}]),
  ]

  combos_uni_stat = combos_uni_stat_nonprime + combos_uni_stat_prime
  combos_uni_glove_prime = combos_uni_stat_prime + [ ("8 crit damage", [{CRITDMG: 8}]) ]
  combos_uni_glove = combos_uni_stat_nonprime + combos_uni_glove_prime
  combos_uni_hat = combos_uni_stat_nonprime + combos_uni_hat_prime

  with Combos(combos_uni_ws) as c:
    c.calc(weapon_secondary_uni)

  with Combos(combos_uni_e) as c:
    c.calc(emblem_uni)

  with Combos(combos_uni_stat) as c:
    c.calc(accessory_uni)
    c.calc(cape_belt_shoulder_uni)
    c.calc(shoe_uni)
    c.calc(bottom_uni)
    c.calc(top_overall_uni)

  with Combos(combos_uni_glove) as c:
    c.calc(glove_uni)

  with Combos(combos_uni_hat) as c:
    c.calc(hat_uni)

cube_calcs()
unicube_calcs()
