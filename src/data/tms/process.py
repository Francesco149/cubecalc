#!/usr/bin/env python3

import sys

sys.path.append("../../")
from common import *
from datautils import nonempty, skip, merge_duplicate_lines

broad_categories = {
  "防具",
  "飾品",
  "武器",
}

category_conversion = {
  "帽子": HAT,
  "上衣": TOP_OVERALL,
  "套服": TOP_OVERALL,
  "下衣": BOTTOM,
  "手套": GLOVE,
  "披風": CAPE_BELT_SHOULDER,
  "腰帶": CAPE_BELT_SHOULDER,
  "肩膀": CAPE_BELT_SHOULDER,
  "鞋子": SHOE,
  "墜飾": FACE_EYE_RING_EARRING_PENDANT,
  "戒指": FACE_EYE_RING_EARRING_PENDANT,
  "臉部裝飾": FACE_EYE_RING_EARRING_PENDANT,
  "眼睛裝飾": FACE_EYE_RING_EARRING_PENDANT,
  "耳環": FACE_EYE_RING_EARRING_PENDANT,
  "武器": WEAPON,
  "徽章": EMBLEM,
  "輔助武器(力量之盾, 靈魂戒指除外)": SECONDARY,
  "輔助武器(力量之盾, 靈魂戒指)": FORCE_SHIELD_SOUL_RING,
  "輔助武器(包含力量之盾, 靈魂戒指)": SECONDARY | FORCE_SHIELD_SOUL_RING,
}

tier_conversion = {
  "特殊等級": RARE,
  "稀有等級": EPIC,
  "罕見等級": UNIQUE,
  "傳說等級": LEGENDARY,
}

ied_text = lambda x: f"無視怪物防禦率+{x}%"
decent_text = lambda x: f"可以使用<{x}> 技能"
boss_text = lambda x: f"攻擊BOSS怪物時傷害增加+{x}%"

line_conversion = {
  "STR": FLAT_MAINSTAT_A,
  "最大HP": FLAT_HP_A,
  "全屬性": FLAT_ALLSTAT_A,
  "物理攻擊力": FLAT_ATT_A,
  "STR%": MAINSTAT_A,
  "最大HP%": HP_A,
  "全屬性%": ALLSTAT_A,
  "物理攻擊力%": ATT_A,
  ied_text(15): IED_C,
  ied_text(30): IED_C,
  ied_text(35): IED_B,
  ied_text(40): IED_A,
  boss_text(30): BOSS_C,
  boss_text(35): BOSS_B,
  boss_text(40): BOSS_A,
  decent_text("實用的會心之眼"): DECENT_SHARP_EYES,
  decent_text("實用的最終極速"): DECENT_SPEED_INFUSION,
  decent_text("實用的戰鬥命令"): DECENT_COMBAT_ORDERS,
  "爆擊傷害%": CRITDMG_A,
  "總傷害%": DAMAGE_A,

  # NOTE: the page has the same text for 1s and 2s so we have to guess that the one with lower
  #       chance is the 2s line. this is done later
  "減少所有技能冷卻時間(10秒以下會減少5%，不會減少到未滿5秒)": COOLDOWN_1,
  "被擊中後無敵時間增加": INVIN,
  "楓幣獲得量%": MESO_A,
  "道具掉落率%": DROP_A,
  "以角色等級為準每10級增加力量": MAINSTAT_PER_10_LVLS,
  "以角色等級為準每10級增加物理攻擊力": ATT_PER_10_LVLS,
}

irrelevant_lines = [
  "DEX", "INT", "LUK", "最大MP", "防禦率", "魔法攻擊力",
  "DEX%", "INT%", "LUK%", "最大MP%", "防禦率%", "魔法攻擊力%",
  "爆擊機率%",
  "攻擊時有一定的機率恢復MP",
  "攻擊時有一定的機率發動中毒效果",
  "攻擊時有一定的機率發動昏迷效果",
  "攻擊時有一定的機率發動緩慢效果",
  "攻擊時有一定的機率發動闇黑效果",
  "攻擊時有一定的機率發動冰結效果",
  "攻擊時有一定的機率發動封印效果",
  decent_text("實用的時空門"),
  decent_text("實用的神聖之火"),
  decent_text("實用的進階祝福"),
  decent_text("實用的速度激發"),
  "移動速度", "跳躍力",
  "被擊中時有一定機率無視傷害",
  "擊殺怪物有一定機率恢復HP",
  "HP恢復道具及恢復技能效果增加",
  "被擊中時有一定機率在時間內無敵", # chance to be invincibile
  "擊殺怪物有一定機率恢復MP",
  "有一定機率反射所受的傷害",
  "所有技能的MP消耗%",
  "攻擊時有一定的機率恢復HP",
  "以角色等級為準每10級增加敏捷",
  "以角色等級為準每10級增加智力",
  "以角色等級為準每10級增加幸運",
  "以角色等級為準每10級增加魔法攻擊力",
]


def find_tier(f):
  for x in nonempty(f):
    s = x.strip()
    if s in tier_conversion:
      return tier_conversion[s]
  return None


def split_categories(s):
  level = 0
  start = 0
  kw = { "(": 1, ")": -1 }
  for i, x in enumerate(s):
    if x in kw:
      level += kw[x]
    if level == 0 and x == ",":
      yield s[start:i]
      start = i + 1
  yield s[start:]


def parse_category(s):
  res = None
  for x in split_categories(s):
    s = x.strip()
    if s not in category_conversion:
      break
    c = category_conversion[s]
    res = res | c if res is not None else c
  return res


def parse_line(f):
  pos = f.tell()
  line = skip(f)
  is_relevant = line in line_conversion
  if not is_relevant and line not in irrelevant_lines:
    f.seek(pos)
    return None
  if is_relevant:
    line = line_conversion[line]

  skip(f) # skip category
  skip(f) # skip animus
  skip(f) # skip reflect
  chances = {
    VIOLET: skip(f),
    EQUALITY: skip(f),
    UNI: skip(f),
  }
  if not is_relevant:
    return line, {}
  if chances[VIOLET] != chances[EQUALITY]:
    sys.stderr.write(f"{line} {chances}: expected violet == equality\n")
    sys.exit(1)
  return line, {k | EQUALITY if k == VIOLET else k: v.split('%')[0]
                for k, v in chances.items() if k in {VIOLET, UNI}}


def parse_lines(f):
  while True:
    s = parse_line(f)
    if s is None:
      break
    if s[1]:
      yield s


def parse_broad(f):
  pos = f.tell()
  s = skip(f)
  if s not in broad_categories:
    f.seek(pos)
    return None
  return s


d = {}

with open("cache/line_chances.txt") as f:
  while True:
    tier = find_tier(f)
    if tier is None:
      break

    while True:
      parse_broad(f)

      pos = f.tell()
      s = skip(f)
      if s is None:
        break
      category = parse_category(s)
      if category is None:
        f.seek(pos)
        sys.stderr.write(f"DEBUG: tier ended at '{s}'\n")
        break

      lines = list(parse_lines(f))
      if lines:
        for cube in lines[0][1].keys():
          if cube not in d:
            d[cube] = {}
          if category not in d[cube]:
            d[cube][category] = {}
          d[cube][category][tier] = [[line, chances[cube]] for line, chances in lines]


# janky way to adjust the lower chance cd line to be 2s
def fix_cd_lines():
  category = HAT
  tierdata = d[VIOLET | EQUALITY][category][LEGENDARY]
  cd_idxs = [i for i, (line, chance) in enumerate(tierdata) if line & COOLDOWN != 0]
  if len(cd_idxs) > 2:
    l = [tierdata[x] for x in cd_idxs]
    sys.stderr.write(f"too many cooldown lines: {l}")
    sys.exit(1)
  if len(cd_idxs) == 2:
    cd2_idx = cd_idxs[1] if tierdata[cd_idxs[0]] > tierdata[cd_idxs[1]] else cd_idxs[0]
    for cube in d.keys():
      tierdata = d[cube][category][LEGENDARY]
      tierdata[cd2_idx][0] = COOLDOWN_2

fix_cd_lines()

bitmask_str = lambda i, e: " | ".join([x.name for x in e if i & x])

from functools import reduce
from operator import or_

for cube, cubedata in d.items():
  cubes = bitmask_str(cube, Cube)
  print(f"{cubes}: {{")
  for category, categorydata in cubedata.items():
    merge_duplicate_lines(categorydata)
    categories = bitmask_str(category, Category)
    print(f"  {categories}: percent({{")
    for tier, tierdata in categorydata.items():
      print(f"    {tier.name}: [")
      for (line, chance) in tierdata:
        print(f"      [{line.name}, {chance}],")
      print(f"    ],")
    print("  }),")
  print("},")
