#!/usr/bin/env python3

import sys
import re

sys.path.append("../../")
from common import *
from datautils import nonempty, skip

tiers = {
  "Base": BASE,
  "Common": COMMON,
  "Rare": RARE,
  "Epic": EPIC,
  "Unique": UNIQUE,
  "Legendary": LEGENDARY,
}

known_lines = {
  "DEF: +#incPDD",
  "Jump: +#incJump",
  "Max MP: +#incMMP",
  "Movement Speed: +#incSpeed",
  "When hit, #prop% chance to be happy for #time sec",
  "When hit, #prop% chance to be moved for #time sec",
  "When hit, #prop% chance to become furious for #time sec",
  "When hit, #prop% chance to become outraged for #time sec",
  "When hit, #prop% chance to fall in love for #time sec",
  "Attacks have a #prop% chance to inflict Lv. #level Blind",
  "Attacks have a #prop% chance to inflict Lv. #level Freeze",
  "Attacks have a #prop% chance to inflict Lv. #level Poison",
  "Attacks have a #prop% chance to inflict Lv. #level Seal",
  "Attacks have a #prop% chance to inflict Lv. #level Slow",
  "Attacks have a #prop% chance to inflict Lv. #level Stun",
  "Attacks have a #prop% chance to restore #HP HP",
  "Attacks have a #prop% chance to restore #MP MP",
  "Continually restores a small amount of MP",
  "DEF: +#incPDDr%",
  "Increases Defense by a small amount",
  "Increases Speed and Jump slightly",
  "Max MP: +#incMMPr%",
  "Prevents HP loss due to the cold in El Nath",
  "Prevents HP loss from drowning at the Aquarium",
  "Prevents slipping in El Nath",
  "Restores #RecoveryMP MP every 4 sec",
  "Attacks have a #prop% chance to ignore #ignoreDAM damage",
  "Continually restores MP",
  "Continually restores a small amount of MP to nearby allies",
  "Continually restores the party's MP by a small amount",
  "Hitting an enemy has a #prop% chance to restore #MP MP",
  "Increases Defense",
  "Increases Speed and Jump",
  "Increases party members' Defense by a small amount",
  "Increases party members' Jump by a small amount",
  "Increases party members' Speed by a small amount",
  "Increases the Defense of nearby allies by a small amount",
  "Increases the Jump of nearby allies by a small amount",
  "Increases the Speed of nearby allies by a small amount",
  "When hit, #prop% chance to ignore #ignoreDAM damage",
  "Increases Defense by a large amount",
  "Increases Speed and Jump by a large amount",
  "Increases party members' Defense"
  "Attacks have a #prop% chance to ignore #ignoreDAMr% damage",
  "Continually restores MP to nearby allies",
  "Continually restores MP to party members",
  "Continually restores a large amount of MP",
  "Attacks have a #prop% chance to ignore #ignoreDAMr% damage",
  "Increases party members' Defense",
  "Increases party members' Jump",
  "Increases party members' Speed",
  "Increases the Defense of nearby allies",
  "Increases the Jump of nearby allies",
  "Increases the Speed of nearby allies",
  "All Elemental Resistances: +#incTerR",
  "All Skill MP Costs: -#mpconReduce%",
  "Continually restores a large amount of MP to nearby allies",
  "Continually restores a large amount of MP to party members",
  "Increases party members' Defense by a large amount",
  "Increases the Defense of nearby allies by a large amount",
  "Increases the Jump of nearby allies by a large amount",
  "Increases the Speed of nearby allies by a large amount",
  "Increases your party's Defense",
  "Increases your party's Speed",
  "Increases your party's Speed and Jump",
  "All Skills Cost: -#mpconReduce%",

  # duplicate lines
  "Magic ATT: +#incMAD",
  "Magic ATT: +#incMADr%",
  "DEX: +#incDEX",
  "INT: +#incINT",
  "LUK: +#incLUK",
  "DEX: +#incDEXr%",
  "INT: +#incINTr%",
  "LUK: +#incLUKr%",
  "Increases DEX",
  "Increases LUK",
  "Increases INT",
  "Increases DEX by a small amount",
  "Increases LUK by a small amount",
  "Increases INT by a small amount",
  "Increases DEX by a large amount",
  "Increases LUK by a large amount",
  "Increases INT by a large amount",
  "Increases the DEX of nearby allies by a small amount",
  "Increases the INT of nearby allies by a small amount",
  "Increases the LUK of nearby allies by a small amount",
  "Increases party members' INT by a small amount",
  "Increases party members' DEX by a small amount",
  "Increases party members' LUK by a small amount",
  "Increases nearby allies' DEX by a percentage",
  "Increases nearby allies' INT by a percentage",
  "Increases nearby allies' LUK by a percentage",
  "Increases nearby allies' DEX by a small percentage",
  "Increases nearby allies' INT by a small percentage",
  "Increases nearby allies' LUK by a small percentage",
  "Increases party members' DEX",
  "Increases party members' INT",
  "Increases party members' LUK",
  "Increases party members' DEX by a small percentage",
  "Increases party members' INT by a small percentage",
  "Increases party members' LUK by a small percentage",
  "Increases the DEX of nearby allies",
  "Increases the INT of nearby allies",
  "Increases the LUK of nearby allies",
  "Increases nearby allies' DEX by a large percentage",
  "Increases nearby allies' INT by a large percentage",
  "Increases nearby allies' LUK by a large percentage",
  "Increases party members' DEX by a large amount",
  "Increases party members' INT by a large amount",
  "Increases party members' LUK by a large amount",
  "Increases party members' DEX by a large percentage",
  "Increases party members' INT by a large percentage",
  "Increases party members' LUK by a large percentage",
  "Increases the DEX of nearby allies by a large amount",
  "Increases the INT of nearby allies by a large amount",
  "Increases the LUK of nearby allies by a large amount",
  "Increases your party's DEX",
  "Increases your party's INT",
  "Increases your party's LUK",

  # TODO: add these as useful lines
  "#prop% chance to become invincible for #time seconds when attacked.",

  "Critical Rate: +#incCr%",
  "#prop% chance to Auto Steal",
  "All Skill Levels: +#incAllskill",

  "Continually restores a small amount of HP",
  "Continually restores HP",
  "Continually restores HP and MP",
  "Continually restores a large amount of HP",
  "Continually restores a large amount of HP & MP",

  "Continually restores a small amount of HP & MP to nearby allies",
  "Continually restores a small amount of HP to nearby allies",
  "Continually restores HP to nearby allies",
  "Continually restores HP & MP to nearby allies",
  "Continually restores a large amount of HP to nearby allies",
  "Continually restores a large amount of HP & MP to nearby allies",

  "Continually restores HP to party members",
  "Continually restores HP & MP to party members",
  "Continually restores a large amount of HP to party members",
  "Continually restores a large amount of HP & MP to party members",

  "Continually restores the party's HP & MP by a small amount",
  "Continually restores the party's HP by a small amount",

  "Hitting an enemy has a #prop% chance to restore #HP HP",
  "HP Recovery Items and Skills: +#RecoveryUP%",
  "Restores #RecoveryHP HP every 4 sec",

  "Increases party members' STR by a small amount",
  "Increases your party's STR",
  "Increases your party's STR, INT, DEX, and LUK",
  "Increases the STR of nearby allies by a small amount",
  "Increases STR by a small amount",
  "Increases STR",
  "Increases STR by a large amount",

  "Increases STR, INT, DEX, and LUK of players on the same map",
  "Increases Speed, Jump, DEX, and Defense by a small amount",

  "ATT: +#incPAD",
  "Max HP: +#incMHP",
  "STR: +#incSTR",
  "All Stats: +#incSTR",
  "Increases party members' STR",
  "Increases party members' STR by a large amount",
  "Increases the STR of nearby allies",
  "Increases the STR of nearby allies by a large amount",

  "ATT: +#incPADr%",
  "STR: +#incSTRr%",
  "Max HP: +#incMHPr%",
  "All Stats: +#incSTRr%",
  "Increases party members' STR by a small percentage",
  "Increases party members' STR by a large percentage",
  "Increases nearby allies' STR by a percentage",
  "Increases nearby allies' STR by a large percentage",

  "Outlines your character in black",
  "Outlines your character in red",
  "Shrouds your character in darkness",
  "Shrouds your character in red shadow",
  "Turns your character red",

  "#prop% chance to reflect #DAMreflect% damage",
  "Abnormal Status Resistance: +#incAsrR%",
}

convert_lines = {
  "Attacks ignore #ignoreTargetDEF% Monster DEF": IED_C,

  "Increases Item Drop Rate by a small amount": SMALL_DROP,
  "Increases Item Drop Rate": DROP_A,
  "Increases Item Drop Rate by a large amount": LARGE_DROP,

  "Increases Meso Drop Rate": MESO_A,
  "Increases Meso Drop Rate by a small amount": SMALL_MESO,
  "Increases Meso Drop Rate by a large amount": LARGE_MESO,

  "Increases Item and Meso Drop Rate by a small amount": SMALL_DROP_MESO,
  "Increases Item and Meso Drop Rate": DROP_MESO,
  "Increases Item and Meso Drop Rate by a large amount": LARGE_DROP_MESO,

  "Item Acquisition Rate: +#incRewardProp%": SMALL_DROP,
  "Mesos Obtained: +#incMesoProp": FLAT_MESO,

  "Total Damage: +#incDAMr%": DAMAGE_A,
  "When hit, get +#time sec of invincibility": INVIN,
  "When hit, gain +#time sec of invincibility": INVIN,
  "Damage to Bosses: +#incDAMr%": BOSS_C,
  "Boss Damage: +#incDAMr%": BOSS_C,
  "Critical Damage: +#incCriticaldamage%": CRITDMG_A,
}

def parse_stat(f):
  s = skip(f)
  if s in known_lines:
    return ANY
  if s not in convert_lines:
    sys.stderr.write(f"stopped on non-stat: {s}\n")
    return None
  return convert_lines[s]


def parse_tier(f):
  l = skip(f)
  s = l.split(" ")[0]
  if s not in tiers:
    sys.stderr.write(f"stopped on non-tier: {l}\n")
    return None
  return tiers[s]

boss_ied_conversion = {
  IED_C: [IED_A, IED_B, IED_C],
  BOSS_C: [BOSS_A, BOSS_B, BOSS_C],
}

lines = {}
with open("cache/familiars.txt") as f:
  percent = -1
  while True:
    tier = parse_tier(f)
    if tier is None:
      break
    lines[tier] = []
    counts = {}

    while True:
      pos = f.tell()
      stat = parse_stat(f)
      if stat is None:
        f.seek(pos)
        break
      s = re.split("[(:%)]", skip(f))
      if s[0] != "Weight":
        raise RuntimeError(f"expected Weight, got {s}")
      percent = float(s[2])
      line = skip(f)
      if not line:
        break

      if stat != ANY:
        linetext = re.split(r"[0-9]", line)[1]
        linetext = line.split(f"2{linetext}")[0][1:]
        amount = int(re.findall(r"[0-9]+", linetext)[-1])
        i = 2
        if stat & (IED_C | BOSS_C):
          if amount == 50 or (amount == 40 and tier == UNIQUE):
            i = 0
          elif amount == 35 or amount == 45:
            i = 1
          elif amount == 30 and tier == EPIC:
            i = 0
          stat = boss_ied_conversion[stat][i]

        if stat == CRITDMG_A:
          if amount == 2:
            stat = CRITDMG_B

        if stat == DAMAGE_A:
          if amount == 5:
            stat = DAMAGE_B

        if stat == LARGE_DROP_MESO:
          if amount == 60:
            # this line doesn't seem to be used
            # it's the big spider line i think
            continue

        line = (stat, percent, amount)
        if line not in counts:
          counts[line] = 1
          lines[tier] += [line]
        else:
          counts[line] += 1

    # TODO: use merge_duplicate_lines in datautils
    for i, l in enumerate(lines[tier]):
      stat, percent, amount = l
      if counts[l] > 1:
        new_percent = percent * counts[l]
        sys.stderr.write(f"{tier.name}: merging duplicate line " +
            f"{amount} {stat.name} from {percent}% to {new_percent}%\n")
        lines[tier][i] = (stat, new_percent, amount)


print("familiars = {")
print("  FAMILIAR: {")
print("    FAMILIAR_STATS: percent({")
for k, v in lines.items():
  print(f"      {k.name}: [")
  for (stat, percent, amount) in v:
    print(f"        [{stat.name}, {percent}], # {amount}")
  print("      ],")
print("    }),")
print("  },")
print("}")
print()
print("values = {")
for k, v in lines.items():
  print(f"  {k.name}: {{")
  print("    ANY: 1,")
  for (stat, percent, amount) in v:
    print(f"    {stat.name}: {amount},")
  print("  },")
print("}")