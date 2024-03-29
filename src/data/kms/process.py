#!/usr/bin/env python3

import sys

sys.path.append("../../")
from common import *

from itertools import zip_longest
import sys

lines = {stat.strip(): float(percent.strip().split('%')[0])
         for stat, percent in zip_longest(*[sys.stdin]*2)}

KW_MATT = "마력"
KW_ATT = "공격력"
KW_STAT = "STR"
KW_HP = "최대 HP"
KW_ALLSTAT = "올스탯"
stat_keywords = {KW_STAT, "INT", "DEX", "LUK"}

def stat_name(s):
  return s.split(':')[0].strip()

convert_s = {
  KW_STAT: MAINSTAT_A,
  KW_ATT: ATT_A,
  "메소 획득량": MESO_A,
  "아이템 드롭률": DROP_A,
  KW_HP: HP_A,
  KW_ALLSTAT: ALLSTAT_A,
  "크리티컬 데미지": CRITDMG_A,
  "데미지": DAMAGE_A,
  "캐릭터 기준 10레벨 당 STR": MAINSTAT_PER_10_LVLS,
  "캐릭터 기준 10레벨 당 공격력": ATT_PER_10_LVLS,
  "몬스터 방어율 무시": IED_C,
  "보스 몬스터 공격 시 데미지": BOSS_C,
  "HP 회복 아이템 및 회복 스킬 효율": HP_ITEMS_AND_SKILLS_A,
}

ied_text = lambda x: f"몬스터 방어율 무시 : +{x}%"
boss_text = lambda x: f"보스 몬스터 공격 시 데미지 : +{x}%"
cd_text = lambda x: f"모든 스킬의 재사용 대기시간 : -{x}초(10초 이하는 {5*x}%감소 5초 미만으로 감소 불가)"
invin_text = lambda x: f"피격 후 무적시간 : +{x}초"
flat_text = lambda k, x=12: f"{k} : +{x}"
steal_text = lambda x=7: f"공격 시 {x}% 확률로 오토스틸"

convert = {
  flat_text(KW_STAT, 10): FLAT_MAINSTAT_A,
  flat_text(KW_STAT, 6): FLAT_MAINSTAT_A,
  flat_text(KW_STAT): FLAT_MAINSTAT_A,
  flat_text(KW_STAT, 14): FLAT_MAINSTAT_A,
  flat_text(KW_STAT, 16): FLAT_MAINSTAT_A,
  flat_text(KW_STAT, 18): FLAT_MAINSTAT_A,
  flat_text(KW_ALLSTAT, 3): FLAT_ALLSTAT_A,
  flat_text(KW_ALLSTAT, 5): FLAT_ALLSTAT_A,
  flat_text(KW_HP, 50): FLAT_HP_A,
  flat_text(KW_HP, 60): FLAT_HP_A,
  flat_text(KW_HP, 100): FLAT_HP_A,
  flat_text(KW_HP, 120): FLAT_HP_A,
  flat_text(KW_HP, 180): FLAT_HP_A,
  flat_text(KW_HP, 240): FLAT_HP_A,
  flat_text(KW_HP, 300): FLAT_HP_A,
  flat_text(KW_ATT, 3): FLAT_ATT_A,
  flat_text(KW_ATT, 6): FLAT_ATT_A,
  flat_text(KW_ATT, 10): FLAT_ATT_A,
  flat_text(KW_ATT, 11): FLAT_ATT_A,
  flat_text(KW_ATT): FLAT_ATT_A,
  flat_text(KW_ATT, 14): FLAT_ATT_A,
  ied_text(35): IED_B,
  ied_text(40): IED_A,
  boss_text(35): BOSS_B,
  boss_text(40): BOSS_A,
  cd_text(1): COOLDOWN_1,
  cd_text(2): COOLDOWN_2,
  invin_text(1): INVIN,
  invin_text(2): INVIN,
  invin_text(3): INVIN,
  "<쓸만한 윈드 부스터> 스킬 사용 가능": DECENT_SPEED_INFUSION,
  "<쓸만한 샤프 아이즈> 스킬 사용 가능": DECENT_SHARP_EYES,
  "<쓸만한 컴뱃 오더스> 스킬 사용 가능": DECENT_COMBAT_ORDERS,
  steal_text(7): AUTOSTEAL_A,
  steal_text(5): AUTOSTEAL_B,
  steal_text(3): AUTOSTEAL_C,
}

# we only take 1 stat and 1 type of att since they're all the same
duplicates = {*{x for x in stat_keywords if x != KW_STAT}, KW_MATT}
lines = {k: v for k, v in lines.items() if k.split(' ')[0] not in duplicates}

def convert_stat(stat):
  stat = stat.strip()
  if stat in convert:
    return convert[stat]
  n = stat_name(stat)
  if n in convert_s:
    return convert_s[n]
  return None

def converted_lines():
  for k, v in lines.items():
    c = convert_stat(k)
    if c:
      yield c, v

lines = {k: v for k, v in converted_lines()}

print("[")
for stat, percent in lines.items():
  print(f"  [{stat.name}, {percent}],")
print("],")
