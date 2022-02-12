#!/usr/bin/env python

from itertools import product
from functools import reduce
from operator import mul

BOSS = "boss"
IED = "ied"
ATT = "att"
ANY = "any"
P = True
N = False

prime_chance_red = [1, 0.1, 0.01]
prime_chance_black = [1, 0.2, 0.05]
prime_chance_violet = [1, 0.1, 0.01, 0.01, 0.1, 0.01]
prime_chance_equality = [1, 1, 1]

prime_lines_weapon = [
  (P, BOSS, 40, 20.5),
  (P, BOSS, 35, 20.5),
  (P, BOSS, 30, 20.5),
  (P, IED,  40, 20.5),
  (P, IED,  35, 20.5),
  (P, ATT,  12, 20.5),
]

lines_weapon = [
  (N, BOSS, 30, 14.3333),
  (N, IED,  30, 14.3333),
  (N, ATT,   9, 14.3333),
]

prime_lines_secondary = [
  (P, BOSS, 40, 23.5),
  (P, BOSS, 35, 23.5),
  (P, BOSS, 30, 23.5),
  (P, IED,  40, 23.5),
  (P, IED,  35, 23.5),
  (P, ATT,  12, 23.5),
]

lines_secondary = [
  (N, BOSS, 30, 17.0),
  (N, IED,  30, 17.0),
  (N, ATT,   9, 17.0),
]

prime_lines_emblem = [
  (P, IED,  40, 17.5),
  (P, IED,  35, 17.5),
  (P, ATT,  12, 17.5),
]

lines_emblem = [
  (N, IED,  30, 13.3333),
  (N, ATT,   9, 13.3333),
]

def cube_calc(text, prime_lines, lines, print_combos):
  print(f" {text} ".center(80, "="))
  lines = lines + prime_lines
  def make_any_line(lines):
    return lines + [(N, ANY, 0, 1.0/(1.0 - sum((1.0/onein for (_, _, _, onein) in lines))))]

  # to represent all the lines we don't care about I generate an ANY line that
  # has 1-(sum of the chances of all lines we care about) chance
  p = make_any_line(prime_lines)
  n = make_any_line(lines)
  combos_red = [x for x in product(p, n, n)]
  combos_violet = [x for x in product(p, n, n, n, n, n)]
  combos_equality = [x for x in product(p, p, p)]

  def combo_chance(want, prime_chance, combos):
    good=set()
    for combo in combos:
      amounts = {}
      for (prime, typ, amount, onein) in combo:
        if typ not in amounts: amounts[typ] = 0
        amounts[typ] += amount
      for k in want.keys():
        if k not in amounts or amounts[k] < want[k]:
          break
      else:
        good.add(combo)
    return sum([reduce(mul, [1.0/onein * (prime_chance[i] if prime else 1)
      for i, (prime, typ, amount, onein) in enumerate(combo)]) for combo in good])

  def fmt_chance(text, wants, prime_chance, combos):
    chance = sum([combo_chance(want, prime_chance, combos) for want in wants])
    return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

  def tabulate(rows):
    max_len = max((len(text) for (text, _) in rows))
    for (text, result) in rows:
      print(f"{text.rjust(max_len)} {result}")

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


combos_ws = [
  ("21+ att", [{ATT: 21}]),
  ("30+ att", [{ATT: 30}]),
  ("33+ att", [{ATT: 33}]),
  ("21+ att and boss", [{ATT: 21, BOSS: 1}]),
  ("21+ att and ied", [{ATT: 21, IED: 1}]),
  ("18+ att and 30+boss", [{ATT: 18, BOSS: 30}]),
  ("18+ att and 30+ied", [{ATT: 18, IED: 30}]),
  ("21+ att and boss or 18+att and 30+boss", [{ATT: 21, BOSS: 1}, {ATT: 18, BOSS: 30}]),
]

combos_e = [
  ("21+ att", [{ATT: 21}]),
  ("30+ att", [{ATT: 30}]),
  ("33+ att", [{ATT: 33}]),
  ("21+ att and ied", [{ATT: 21, IED: 1}]),
]

cube_calc("weapon", prime_lines_weapon, lines_weapon, combos_ws)
cube_calc("secondary", prime_lines_secondary, lines_secondary, combos_ws)
cube_calc("emblem", prime_lines_emblem, lines_emblem, combos_e)
