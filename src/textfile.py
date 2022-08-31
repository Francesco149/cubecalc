#!/usr/bin/env python3

# this script generates cubechances.txt
# there is a lot of leftover janky glue code here from back when all the probabilities were
# hardcoded. once I have a proper UI, this will mainly just be a benchmark and a way to check
# that changes in the code didn't affect any result unexpectedly

from cubecalc import disclaimer, cube_calc
from common import *
from functools import partial

from datautils import percent
from datautils import find_validate_probabilities as find_probabilities
import kms
import tms

TIER_DEFAULT = LEGENDARY

prob_cash = partial(find_probabilities, kms.cubes, CASH_MAIN)
weapon = prob_cash(WEAPON)
secondary = prob_cash(SECONDARY)
emblem = prob_cash(EMBLEM)
top_overall = prob_cash(TOP_OVERALL)
bottom = prob_cash(BOTTOM)
hat = prob_cash(HAT)
accessory = prob_cash(FACE_EYE_RING_EARRING_PENDANT)
cape_belt_shoulder = prob_cash(CAPE_BELT_SHOULDER)
glove = prob_cash(GLOVE)

prob_noncash = partial(find_probabilities, kms.cubes, NONCASH_MAIN)
weapon_noncash = prob_noncash(WEAPON)
secondary_noncash = prob_noncash(SECONDARY)
emblem_noncash = prob_noncash(EMBLEM)
top_overall_noncash = prob_noncash(TOP_OVERALL)
bottom_noncash = prob_noncash(BOTTOM)
hat_noncash = prob_noncash(HAT)
accessory_noncash = prob_noncash(FACE_EYE_RING_EARRING_PENDANT)
cape_belt_shoulder_noncash = prob_noncash(CAPE_BELT_SHOULDER)
glove_noncash = prob_noncash(GLOVE)

prob_bonus = partial(find_probabilities, kms.cubes, BONUS)
weapon_bonus = prob_bonus(WEAPON)
secondary_bonus = prob_bonus(SECONDARY)
emblem_bonus = prob_bonus(EMBLEM)
hat_bonus = prob_bonus(HAT)

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

from familiars import familiars as familiars_data
from familiars import red_card_estimate
familiars = find_probabilities(familiars_data, FAMILIAR, FAMILIAR_STATS)
familiars_red_card = find_probabilities(red_card_estimate, RED_FAM_CARD, FAMILIAR_STATS)


def tabulate(rows):
  max_len = max((len(text) for (text, _) in rows))
  for (text, result) in rows:
    print(f"{text.rjust(max_len)} {result}")


def __cube_calc_print(print_combos, category, type, tier, level, region, lines):
  def fmt_chance(text, wants):
    nonlocal tier
    chance, tier = cube_calc(wants, category, type, tier, level, region, lines)
    return (text, f"1 in {round(1.0/chance)} cubes, {chance*100:.4f}%")

  # janky but we run this first to get the actual tier that's being computed
  formatted = [fmt_chance(text, want) for (text, want) in print_combos]
  print(f" {lines[NAME]} ({type.name.lower()} on lv{level} {tier.name.lower()}) ".center(80, "="))
  tabulate(formatted)


def single_or_list(x):
  return x if isinstance(x, list) else [x]


def cube_calc_print(print_combos, category, types, tier, level, region, *args):
  for l in args:
    lt = types
    if not lt:
      lt = l[DEFAULT_CUBE]
    for t in single_or_list(lt):
      __cube_calc_print(print_combos, category, t, tier, level, region, l)


def Combos(combos, category, types=[], tier=TIER_DEFAULT, level=150, region=GMS):
  return partial(cube_calc_print, combos, category, types, tier, level, region)


def cube_calcs():
  combos_wse_occult = [
    ("6+ att", [{ATT: 6}]),
    ("9+ att", [{ATT: 9}]),
    ("12+ att", [{ATT: 12}]),
  ]

  combos_any_ws = [
    ("any 2l combo of att+boss", [{ATT: 1, BOSS_ONLY: 1, LINES: 2}]),
    ("any 2l combo of att+boss+ied", [{ATT: 1, BOSS_ONLY: 1, IED: 1, LINES: 2}]),
    ("any 3l combo of att+boss", [{ATT: 1, BOSS_ONLY: 1, LINES: 3}]),
    ("any 3l combo of att+boss+ied", [{ATT: 1, BOSS_ONLY: 1, IED: 1, LINES: 3}]),
  ]

  combos_wse_master = [
    ("9+ att", [{ATT: 9}]),
    ("12+ att", [{ATT: 12}]),
    ("15+ att", [{ATT: 15}]),
    ("21+ att", [{ATT: 21}]),
  ]

  combos_ws_master = combos_any_ws + combos_wse_master + [
    ("any boss", [{BOSS_ONLY: 1}]),
  ]

  combos_ws = combos_any_ws + [
    ("18+ att", [{ATT: 18}]),
    ("21+ att", [{ATT: 21}]),
    ("30+ att", [{ATT: 30}]),
    ("33+ att", [{ATT: 33}]),
    ("21+ att and boss", [{ATT: 21, BOSS_ONLY: 1}]),
    ("21+ att and ied", [{ATT: 21, IED: 1}]),
    ("18+ att and boss", [{ATT: 18, BOSS_ONLY: 1}]),
    ("18+ att and ied", [{ATT: 18, IED: 1}]),
    ("60+ied", [{IED: 60}]),
    ("70+ied", [{IED: 70}]),
    ("60+ied and att", [{IED: 60, ATT: 1}]),
    ("60+ied and boss", [{IED: 60, BOSS_ONLY: 1}]),
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

  combos_rare_b = [
    ("10+ flat att", [{FLAT_ATT: 10}]),
    ("13+ flat att", [{FLAT_ATT: 13}]),
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

  combos_glove_steal = [
    ("3+ auto steal", [{AUTOSTEAL: 3}]),
    ("5+ auto steal", [{AUTOSTEAL: 5}]),
    ("7+ auto steal", [{AUTOSTEAL: 7}]),
    ("10+ auto steal", [{AUTOSTEAL: 10}]),
    ("12+ auto steal", [{AUTOSTEAL: 12}]),
    ("13+ auto steal", [{AUTOSTEAL: 13}]),
    ("14+ auto steal", [{AUTOSTEAL: 14}]),
    ("15+ auto steal", [{AUTOSTEAL: 15}]),
    ("17+ auto steal", [{AUTOSTEAL: 17}]),
    ("19+ auto steal", [{AUTOSTEAL: 19}]),
    ("21 auto steal", [{AUTOSTEAL: 21}]),
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

  ws = WEAPON | SECONDARY
  wse = ws | EMBLEM

  Combos(combos_ws, ws)(
    weapon,
    weapon_noncash,
    secondary,
    secondary_noncash,
    weapon_secondary_violet_equality,
  )

  Combos(combos_ws_master, ws, MASTER)(
    weapon_noncash,
    secondary_noncash,
  )

  Combos(combos_e, EMBLEM)(
    emblem,
    emblem_noncash,
    emblem_violet_equality,
  )

  Combos(combos_e_master, EMBLEM, MASTER)(
    emblem_noncash,
  )

  Combos(combos_wse_occult, wse, OCCULT)(
    weapon_noncash,
    secondary_noncash,
    emblem_noncash,
  )

  Combos(combos_wse_b, wse)(
    weapon_bonus,
    secondary_bonus,
    emblem_bonus,
  )

  Combos(combos_rare_b, HAT, BONUS, RARE)(
    hat_bonus,
  )

  Combos(combos_stat, TOP_OVERALL | CAPE_BELT_SHOULDER | SHOE | BOTTOM)(
    top_overall,
    top_overall_noncash,
    top_overall_violet_equality,
    cape_belt_shoulder,
    cape_belt_shoulder_noncash,
    cape_belt_shoulder_violet_equality,
    shoe_violet_equality,
    bottom,
    bottom_noncash,
    bottom_violet_equality,
  )

  Combos(combos_stat + combos_mesodrop, FACE_EYE_RING_EARRING_PENDANT)(
    accessory,
    accessory_noncash,
    accessory_violet_equality,
  )

  Combos(combos_hat, HAT)(
    hat,
    hat_noncash,
    hat_violet_equality,
  )

  stat = FACE_EYE_RING_EARRING_PENDANT | TOP_OVERALL | HAT

  Combos(combos_occult_stat, stat, OCCULT)(
    accessory_noncash,
    top_overall_noncash,
    hat_noncash,
  )

  Combos(combos_master_stat, stat, [MASTER, MEISTER], UNIQUE)(
    accessory_noncash,
    top_overall_noncash,
    hat_noncash,
  )

  Combos(combos_master_stat, stat, RED, UNIQUE)(
    accessory,
    top_overall,
    hat,
  )

  Combos(combos_glove, GLOVE)(
    glove,
    glove_noncash,
    glove_violet_equality,
  )

  Combos(combos_glove_steal, GLOVE)(
    glove_noncash,
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
    ("35+ boss", [{BOSS_ONLY: 35}]),
    ("40 boss", [{BOSS_ONLY: 40}]),
  ] + combos_e_prime

  combos_ws_nonprime = [
    ("9+ att or 30+ boss or 30+ ied", [{ATT: 9}, {BOSS_ONLY: 30}, {IED: 30}]),
    ("9+ att or 30+ boss", [{ATT: 9}, {BOSS_ONLY: 30}]),
    ("30+ boss", [{BOSS_ONLY: 30}]),
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

  Combos(combos_ws, WEAPON | SECONDARY)(
    weapon_secondary_uni,
  )

  Combos(combos_e, EMBLEM)(
    emblem_uni,
  )

  Combos(combos_stat, CAPE_BELT_SHOULDER | SHOE | BOTTOM | TOP_OVERALL)(
    cape_belt_shoulder_uni,
    shoe_uni,
    bottom_uni,
    top_overall_uni,
  )

  Combos(combos_stat + combos_mesodrop, FACE_EYE_RING_EARRING_PENDANT)(
    accessory_uni,
  )

  Combos(combos_glove, GLOVE)(
    glove_uni,
  )

  Combos(combos_hat, HAT)(
    hat_uni,
  )


def familiar_calcs():
  combos_fam_common = [
    ("15+ ied", [{IED: 15}]),
    ("30+ meso", [{MESO: 30}]),
    ("30+ drop", [{DROP: 30}]),
    ("1+ damage", [{DAMAGE: 1}]),
  ]

  combos_fam_rare = combos_fam_common + [
    ("30+ ied", [{IED: 30}]),
    ("2+ damage", [{DAMAGE: 2}]),
    ("3+ damage", [{DAMAGE: 3}]),
    ("20+ meso", [{MESO: 20}]),
    ("20+ drop", [{DROP: 20}]),
    ("20+ meso and drop", [{MESO: 20, DROP: 20}]),
    ("50+ meso", [{MESO: 50}]),
    ("50+ drop", [{DROP: 50}]),
    ("70+ drop", [{DROP: 70}]),
    ("70+ meso", [{DROP: 70}]),
    ("5+ hp healing", [{HEAL_HP: 5}]),
    ("5+ mp healing", [{HEAL_MP: 5}]),
  ]

  combos_fam_epic = [
    ("20+ boss", [{BOSS: 20}]),
    ("30+ boss", [{BOSS: 30}]),
    ("any 2l combo of boss and hp healing", [{BOSS: 1, HEAL_HP: 1, LINES: 2}]),
    ("20+ ied", [{IED: 20}]),
    ("30+ ied", [{IED: 30}]),
    ("25+ drop", [{DROP: 25}]),
    ("50+ drop", [{DROP: 50}]),
    ("100+ drop", [{DROP: 100}]),
    ("25+ meso", [{MESO: 25}]),
    ("25+ meso and drop", [{MESO: 25, DROP: 25}]),
    ("40+ meso and drop", [{MESO: 40, DROP: 40}]),
    ("1+ auto steal", [{AUTOSTEAL: 1}]),
    ("2+ auto steal", [{AUTOSTEAL: 2}]),
    ("any 2l combo of drop and auto steal", [{AUTOSTEAL: 1, DROP: 1, LINES: 2}]),
    ("10+ hp healing", [{HEAL_HP: 10}]),
    ("10+ mp healing", [{HEAL_MP: 10}]),
    ("15+ hp healing", [{HEAL_HP: 15}]),
    ("15+ mp healing", [{HEAL_MP: 15}]),
  ]

  combos_fam_unique = combos_fam_epic + [
    ("35+ boss", [{BOSS: 35}]),
    ("40+ boss", [{BOSS: 40}]),
    ("35+ boss and any hp healing", [{BOSS: 35, HEAL_HP: 1}]),
    ("40+ boss and any hp healing", [{BOSS: 40, HEAL_HP: 1}]),
    ("35+ ied", [{IED: 35}]),
    ("40+ ied", [{IED: 40}]),
    ("any 2l combo of boss and ied", [{BOSS: 1, IED: 1, LINES: 2}]),
    ("any 2l combo of boss", [{BOSS: 1, LINES: 2}]),
    ("50+ boss ", [{BOSS: 50}]),
    ("50+ meso and drop", [{MESO: 50, DROP: 50}]),
    ("25+ meso and 90+ drop", [{MESO: 25, DROP: 90}]),
    ("any 2l combo of meso and drop", [{MESO: 1, DROP: 1, LINES: 2}]),
    ("any 2l combo of drop and auto steal", [{AUTOSTEAL: 1, DROP: 1, LINES: 2}]),

    ("3+ auto steal", [{AUTOSTEAL: 3}]),
    ("4+ auto steal", [{AUTOSTEAL: 4}]),
    ("5+ auto steal", [{AUTOSTEAL: 5}]),
    ("6+ auto steal", [{AUTOSTEAL: 6}]),
    ("7+ auto steal", [{AUTOSTEAL: 7}]),
    ("8+ auto steal", [{AUTOSTEAL: 8}]),
    ("9+ auto steal", [{AUTOSTEAL: 9}]),

    ("20+ hp healing", [{HEAL_HP: 20}]),
    ("20+ mp healing", [{HEAL_MP: 20}]),
  ]

  combos_fam_legendary = [
    ("40+ boss", [{BOSS: 40}]),
    ("45+ boss", [{BOSS: 45}]),
    ("50+ boss", [{BOSS: 50}]),
    ("60+ boss", [{BOSS: 60}]),
    ("any 2l combo of boss and hp healing", [{BOSS: 1, HEAL_HP: 1, LINES: 2}]),
    ("45+ boss and any hp healing", [{BOSS: 45, HEAL_HP: 1}]),
    ("50+ boss and any hp healing", [{BOSS: 50, HEAL_HP: 1}]),

    ("40+ ied", [{IED: 40}]),
    ("45+ ied", [{IED: 45}]),
    ("50+ ied", [{IED: 50}]),
    ("60+ ied", [{IED: 60}]),

    ("any 2l combo of drop and auto steal", [{AUTOSTEAL: 1, DROP: 1, LINES: 2}]),
    ("4+ auto steal", [{AUTOSTEAL: 4}]),
    ("6+ auto steal", [{AUTOSTEAL: 6}]),
    ("8+ auto steal", [{AUTOSTEAL: 8}]),
    ("12+ auto steal", [{AUTOSTEAL: 12}]),
    ("13+ auto steal", [{AUTOSTEAL: 13}]),
    ("14+ auto steal", [{AUTOSTEAL: 14}]),
  ]

  Combos(combos_fam_common, FAMILIAR_STATS, FAMILIAR, COMMON)(familiars)
  Combos(combos_fam_rare, FAMILIAR_STATS, FAMILIAR, RARE)(familiars)
  Combos(combos_fam_epic, FAMILIAR_STATS, FAMILIAR, EPIC)(familiars)
  Combos(combos_fam_unique, FAMILIAR_STATS, FAMILIAR, UNIQUE)(familiars)
  Combos(combos_fam_legendary, FAMILIAR_STATS)(
    familiars,
    familiars_red_card,
  )


if __name__ == "__main__":
  print(f" ! DISCLAIMER ! ".center(80, "="))
  print(disclaimer)

  cube_calcs()
  unicube_calcs()
  familiar_calcs()
