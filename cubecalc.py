#!/usr/bin/env python

from itertools import product
from functools import reduce
from operator import mul

BOSS = "boss"
IED = "ied"
ATT = "att"
ANY = "any"
STAT = "stat"
ALLSTAT = "allstat"
HP = "hp"
COOLDOWN = "cooldown"
P = True
N = False

prime_chance_red = [1, 0.1, 0.01]
prime_chance_meister = [1, 0.001996, 0.001996]
prime_chance_black = [1, 0.2, 0.05]
prime_chance_violet = [1, 0.1, 0.01, 0.01, 0.1, 0.01]
prime_chance_equality = [1, 1, 1]
prime_chance_bonus = [1, 0.004975, 0.004975]
prime_chance_occult = [1] + [1.0/101]*2

prime_lines_weapon = [
  (P, BOSS, 40, 20.5),
  (P, BOSS, 35, 20.5),
  (P, BOSS, 30, 20.5),
  (P, IED,  40, 20.5),
  (P, IED,  35, 20.5),
  (P, ATT,  12, 20.5),
]

prime_lines_weapon_meister = [
  (P, BOSS, 40, 36),
  (P, BOSS, 35, 18),
  (P, BOSS, 30, 18),
  (P, IED,  40, 36),
  (P, IED,  35, 18),
  (P, ATT,  12, 18),
]

lines_weapon = [
  (N, BOSS, 30, 14.3333),
  (N, IED,  30, 14.3333),
  (N, ATT,   9, 14.3333),
]

lines_weapon_meister = [
  (N, BOSS, 30, 15),
  (N, IED,  30, 15),
  (N, ATT,   9, 15),
]

prime_lines_secondary = [
  (P, BOSS, 40, 23.5),
  (P, BOSS, 35, 23.5),
  (P, BOSS, 30, 23.5),
  (P, IED,  40, 23.5),
  (P, IED,  35, 23.5),
  (P, ATT,  12, 23.5),
]

prime_lines_secondary_meister = [
  (P, BOSS, 40, 24),
  (P, BOSS, 35, 24),
  (P, BOSS, 30, 48),
  (P, IED,  40, 48),
  (P, IED,  35, 24),
  (P, ATT,  12, 24),
]

lines_secondary = [
  (N, BOSS, 30, 17.0),
  (N, IED,  30, 17.0),
  (N, ATT,   9, 17.0),
]

lines_secondary_meister = [
  (N, BOSS, 30, 21),
  (N, IED,  30, 21),
  (N, ATT,   9, 21),
]

prime_lines_emblem = [
  (P, IED,  40, 17.5),
  (P, IED,  35, 17.5),
  (P, ATT,  12, 17.5),
]

prime_lines_emblem_meister = [
  (P, IED,  40, 15.5),
  (P, IED,  35, 31),
  (P, ATT,  12, 15.5),
]

lines_emblem = [
  (N, IED,  30, 13.3333),
  (N, ATT,   9, 13.3333),
]

lines_emblem_meister = [
  (N, IED,  30, 14),
  (N, ATT,   9, 14),
]

prime_lines_weapon_b = [
  (P, ATT, 12, 19.5),
]

lines_weapon_b = [
  (N, ATT, 9, 21.5),
]

prime_lines_secondary_b = [
  (P, ATT, 12, 20.5),
]

lines_secondary_b = [
  (N, ATT, 9, 21.5),
]

prime_lines_emblem_b = [
  (P, ATT, 12, 19),
]

lines_emblem_b = [
  (N, ATT, 9, 21),
]

prime_lines_top = [
  (P, STAT, 12, 10.75),
  (P, ALLSTAT, 9, 10.75),
  (P, HP, 12, 10.75),
]

prime_lines_top_meister = [
  (P, STAT, 12, 17),
  (P, ALLSTAT, 9, 17),
  (P, HP, 12, 11.3333),
]

lines_top = [
  (N, STAT, 9, 13.2),
  (N, HP, 9, 11),
  (N, ALLSTAT, 6, 16.5),
]

lines_top_meister = [
  (N, STAT, 9, 16.5),
  (N, HP, 9, 11),
  (N, ALLSTAT, 6, 33),
]

prime_lines_hat = [
  (P, STAT, 12, 11.25),
  (P, HP, 12, 11.25),
  (P, ALLSTAT, 9, 15),
  (P, COOLDOWN, 1, 15),
  (P, COOLDOWN, 2, 22.5),
]

prime_lines_hat_meister = [
  (P, STAT, 12, 18),
  (P, HP, 12, 12),
  (P, ALLSTAT, 9, 18),
  (P, COOLDOWN, 1, 12),
  (P, COOLDOWN, 2, 18),
]

lines_hat = [
  (N, STAT, 9, 11.2),
  (N, HP, 9, 9.3333),
  (N, ALLSTAT, 6, 14),
]

lines_hat_meister = [
  (N, STAT, 9, 14.5),
  (N, HP, 9, 9.6666),
  (N, ALLSTAT, 6, 29),
]

prime_lines_occult_accessory = [
  (P, STAT, 6, 9),
  (P, HP, 6, 6),
  (P, ALLSTAT, 3, 18),
]

lines_occult_accessory = [
  (N, STAT, 3, 21),
  (N, HP, 3, 14),
]

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

def cube_calc(
  text, prime_lines, lines, print_combos, singular_cube=False, prime_chance_singular=[]
):
  print(f" {text} ".center(80, "="))
  lines = lines + prime_lines
  def make_any_line(prime, lines):
    return lines + [(prime, ANY, 0, 1.0/(1.0 - sum((1.0/onein for (_, _, _, onein) in lines))))]

  # to represent all the lines we don't care about I generate an ANY line that
  # has 1-(sum of the chances of all lines we care about) chance
  p = make_any_line(P, prime_lines)
  n = make_any_line(N, lines)
  if not singular_cube:
    combos_red = list(filter_impossible_lines(product(p, n, n)))
    combos_violet = list(filter_impossible_lines(product(p, n, n, n, n, n)))
    combos_equality = list(filter_impossible_lines(product(p, p, p)))
  else:
    combos_singular_cube = list(product(p, n, n))

  def combo_chance(want, prime_chance, combos):
    good=set()
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

  def fmt_chance(text, wants, prime_chance, combos):
    chance = sum([combo_chance(want, prime_chance, combos) for want in wants])
    return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

  def tabulate(rows):
    max_len = max((len(text) for (text, _) in rows))
    for (text, result) in rows:
      print(f"{text.rjust(max_len)} {result}")

  if singular_cube:
    tabulate([fmt_chance(text, want, prime_chance_singular, combos_singular_cube)
      for (text, want) in print_combos])
    return
  print("red")
  tabulate([fmt_chance(text, want, prime_chance_red, combos_red)
    for (text, want) in print_combos])
  print()
  print("violet")
  tabulate([fmt_chance(text, want, prime_chance_violet, combos_violet)
    for (text, want) in print_combos])
  print()
  print("equality")
  tabulate([fmt_chance(text, want, prime_chance_equality, combos_equality)
    for (text, want) in print_combos])
  print()
  print("black")
  tabulate([fmt_chance(text, want, prime_chance_black, combos_red)
    for (text, want) in print_combos])
  print()


def cube_calc_b(text, prime_lines, lines, print_combos):
  return cube_calc(text, prime_lines, lines, print_combos, True, prime_chance_bonus)


def cube_calc_m(text, prime_lines, lines, print_combos):
  return cube_calc(text, prime_lines, lines, print_combos, True, prime_chance_meister)


def cube_calc_o(text, prime_lines, lines, print_combos):
  return cube_calc(text, prime_lines, lines, print_combos, True, prime_chance_occult)


combos_ws = [
  ("21+ att", [{ATT: 21}]),
  ("30+ att", [{ATT: 30}]),
  ("33+ att", [{ATT: 33}]),
  ("21+ att and boss", [{ATT: 21, BOSS: 1}]),
  ("21+ att and ied", [{ATT: 21, IED: 1}]),
  ("18+ att and 30+boss", [{ATT: 18, BOSS: 30}]),
  ("18+ att and 30+ied", [{ATT: 18, IED: 30}]),
  ("60+ied", [{IED: 60}]),
  ("70+ied", [{IED: 70}]),
  ("60+ied and att", [{IED: 60, ATT: 1}]),
  ("60+ied and boss", [{IED: 60, BOSS: 1}]),
  ("21+ att and boss or 18+att and 30+boss", [{ATT: 21, BOSS: 1}, {ATT: 18, BOSS: 30}]),
]

combos_e = [
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

cube_calc("weapon", prime_lines_weapon, lines_weapon, combos_ws)
cube_calc_m("weapon (meisters)", prime_lines_weapon_meister, lines_weapon_meister, combos_ws)
cube_calc("secondary", prime_lines_secondary, lines_secondary, combos_ws)
cube_calc_m("secondary (meisters)", prime_lines_secondary_meister, lines_secondary_meister, combos_ws)
cube_calc("emblem", prime_lines_emblem, lines_emblem, combos_e)
cube_calc_m("emblem (meisters)", prime_lines_emblem_meister, lines_emblem_meister, combos_e)

cube_calc_b("weapon bpot", prime_lines_weapon_b, lines_weapon_b, combos_wse_b)
cube_calc_b("secondary bpot", prime_lines_secondary_b, lines_secondary_b, combos_wse_b)
cube_calc_b("emblem bpot", prime_lines_emblem_b, lines_emblem_b, combos_wse_b)

cube_calc("top/overall", prime_lines_top, lines_top, combos_stat)
cube_calc_m("top/overall (meisters)", prime_lines_top_meister, lines_top_meister, combos_stat)

cube_calc("hat", prime_lines_hat, lines_hat, combos_hat)

cube_calc_o("accessory (occult cubes)",
  prime_lines_occult_accessory, lines_occult_accessory, combos_occult_stat)
