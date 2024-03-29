#!/usr/bin/env python3

import sys
import pandas as pd
sys.path.append("../../")
from common import *

known = {
  LEGENDARY: {
    "6% chance to become invincible for 5 seconds when attacked.",
    "10% chance to reflect 40% damage",
    "All Skill MP Costs: -12%",
    "Outlines your character in red",
    "Outlines your character in black",
    "Shrouds your character in red shadow",
    "Shrouds your character in darkness",
    "Attacks have a 12% chance to ignore 25% damage",
    "DEF: +9%",
    "10% chance to reflect 30% damage",
    "Max MP: +9%",
    "Attacks have a 12% chance to ignore 45% damage",
    "All Skills Cost: -6%",
    "All Elemental Resistances: +7",
    "LUK: +9%",
    "DEX: +9%",
    "INT: +9%",
    "Magic ATT: +9%",

    "Abnormal Status Resistance: +7%",
    "All Skill Levels: +1",
    "Critical Rate: +9%",
  },
  UNIQUE: {
    "All Skill MP Costs: -5%",
    "Increases the Speed of nearby allies by a large amount",
    "DEF: +5%",
    "DEF: +6%",
    "Attacks have a 10% chance to ignore 30% damage",
    "Increases party members' Speed",
    "DEF: +25",
    "Hitting an enemy has a 15% chance to restore 45 MP",
    "Increases party members' Defense by a large amount",
    "Attacks have a 10% chance to ignore 25% damage",
    "Increases the Defense of nearby allies by a large amount",
    "10% chance to reflect 20% damage",
    "Increases the Jump of nearby allies by a large amount",
    "All Skill MP Costs: -10%",
    "All Elemental Resistances: +5",
    "DEF: +22",
    "Turns your character red",
    "Max MP: +6%",
    "Max MP: +5%",
    "Max MP: +25",
    "Attacks have a 10% chance to ignore 20% damage",
    "Increases your party's Speed and Jump",
    "Attacks have a 10% chance to ignore 40% damage",
    "Movement Speed: +8",
    "Movement Speed: +7",
    "Jump: +7",
    "Max MP: +22",
    "Jump: +8",
    "Increases party members' Jump",

    # these lines are both unique and leg, not prime
    "Outlines your character in black",
    "10% chance to reflect 30% damage",
    "Shrouds your character in darkness",
    "All Skill Levels: +1",
    "Outlines your character in red",

    "DEX: +7",
    "INT: +7",
    "LUK: +7",
    "DEX: +8",
    "INT: +8",
    "LUK: +8",
    "DEX: +5%",
    "INT: +5%",
    "LUK: +5%",
    "DEX: +6%",
    "INT: +6%",
    "LUK: +6%",
    "Magic ATT: +5%",
    "Magic ATT: +6%",
    "Magic ATT: +7",
    "Magic ATT: +8",

    # TODO: add these lines
    "Abnormal Status Resistance: +5%",
    "Hitting an enemy has a 15% chance to restore 45 HP",
    "3% chance to become invincible for 5 seconds when attacked.",
    "4% chance to become invincible for 5 seconds when attacked.",
    "Critical Rate: +5%",
    "Critical Rate: +6%",
  }
}

conversion = {
  LEGENDARY: {
    "Attacks ignore 50% Monster DEF": IED_A,
    "Attacks ignore 45% Monster DEF": IED_B,
    "Boss Damage: +50%": BOSS_A,
    "Boss Damage: +45%": BOSS_B,
    "Boss Damage: +40%": BOSS_C,
    "Total Damage: +9%": DAMAGE_A,
    "Mesos Obtained: +12": FLAT_MESO,
    "Critical Damage: +6%": CRITDMG_A,
    "When hit, gain +4 sec of invincibility": INVIN,
    "Item Acquisition Rate: +12%": SMALL_DROP,
    "STR: +9%": MAINSTAT_A,
    "ATT: +9%": ATT_A,
    "Max HP: +9%": HP_A,
    "All Stats: +5%": ALLSTAT_A,
    "8% chance to Auto Steal": AUTOSTEAL_A,
    "6% chance to Auto Steal": AUTOSTEAL_B,
    "4% chance to Auto Steal": AUTOSTEAL_C,
    "HP Recovery Items and Skills: +30%": HP_ITEMS_AND_SKILLS_A,
  },
  UNIQUE: {
    "Item Acquisition Rate: +10%": SMALL_DROP,
    "Increases Item and Meso Drop Rate by a large amount": LARGE_DROP_MESO,
    "Attacks ignore 30% Monster DEF": IED_C,
    "Attacks ignore 35% Monster DEF": IED_B,
    "Attacks ignore 40% Monster DEF": IED_A,
    "Boss Damage: +40%": BOSS_A,
    "Boss Damage: +35%": BOSS_B,
    "Boss Damage: +30%": BOSS_C,
    "Total Damage: +6%": DAMAGE_A,
    "Total Damage: +5%": DAMAGE_B,
    "Critical Damage: +2%": CRITDMG_B,
    "Critical Damage: +3%": CRITDMG_A,
    "When hit, gain +3 sec of invincibility": INVIN,
    "Mesos Obtained: +10": FLAT_MESO,
    "STR: +7": FLAT_MAINSTAT_B,
    "STR: +8": FLAT_MAINSTAT_A,
    "All Stats: +4": FLAT_ALLSTAT_A,
    "Increases your party's STR, INT, DEX, and LUK": FLAT_ALLSTAT_B,
    "Increases STR, INT, DEX, and LUK of players on the same map": FLAT_ALLSTAT_C,
    "ATT: +7": FLAT_ATT_A,
    "ATT: +8": FLAT_ATT_B,
    "Increases Speed, Jump, DEX, and Defense by a small amount": FLAT_DEX_ONLY,
    "Max HP: +22": FLAT_HP_B,
    "Max HP: +25": FLAT_HP_A,
    "STR: +5%": MAINSTAT_B,
    "STR: +6%": MAINSTAT_A,
    "ATT: +5%": ATT_B,
    "ATT: +6%": ATT_A,
    "Max HP: +5%": HP_B,
    "Max HP: +6%": HP_A,
    "All Stats: +2%": ALLSTAT_B,
    "All Stats: +3%": ALLSTAT_A,
    "3% chance to Auto Steal": AUTOSTEAL_E,
    "4% chance to Auto Steal": AUTOSTEAL_D,
    "5% chance to Auto Steal": AUTOSTEAL_C,
    "6% chance to Auto Steal": AUTOSTEAL_B,
    "7% chance to Auto Steal": AUTOSTEAL_A,
    "Continually restores a large amount of HP to nearby allies": HEAL_HP_ONLY_NEAR_A,
    "Continually restores a large amount of HP to party members": HEAL_HP_ONLY_PARTY_A,
    "Continually restores a large amount of HP & MP": HEAL_HP_MP_A,
    "Continually restores a large amount of HP & MP to party members": HEAL_HP_MP_PARTY_A,
    "Continually restores a large amount of HP & MP to nearby allies": HEAL_HP_MP_NEAR_A,
    "Continually restores a large amount of MP to party members": HEAL_MP_ONLY_PARTY_A,
    "Continually restores a large amount of MP to nearby allies": HEAL_MP_ONLY_NEAR_A,
    "HP Recovery Items and Skills: +15%": HP_ITEMS_AND_SKILLS_B,
    "HP Recovery Items and Skills: +20%": HP_ITEMS_AND_SKILLS_A,
  },
}

df = pd.read_excel("red-card-data.ods", engine="odf", header=None, usecols=[0, 1])
datapoints = len(df[0])
primes = 0

def process(tier, line, count, pr=True):
  if line in known[tier]:
    return 0

  if line not in conversion[tier]:
    # double prime
    if (tier + 1) in known and line in known[tier + 1]:
      return count

    if (tier + 1) in conversion and line in conversion[tier + 1]:
      return count

    raise RuntimeError(f"unknown line: {line}")

  if pr:
    conv = conversion[tier][line]
    nonprime = f" / ({nonprimes} / {datapoints})" if tier == UNIQUE else ""
    print(f"        [{conv.name}, {count} / {datapoints} * 100{nonprime}],")

  return 0

primes = sum([process(UNIQUE, *x, False) for x in df[1].value_counts().items()])
nonprimes = datapoints - primes

print("red_card_estimate = {")
print("  RED_FAM_CARD: {")
print("    FAMILIAR_STATS: percent({")
print("      BASE: [],")
print("      COMMON: [],")
print("      RARE: [],")
print("      EPIC: [],")
print("      UNIQUE: [")
[process(UNIQUE, *x) for x in df[1].value_counts().items()]
print("      ],")
print("      LEGENDARY: [")
[process(LEGENDARY, *x) for x in df[0].value_counts().items()]
print("      ],")
print("    }),")
print("  },")
print("}")
