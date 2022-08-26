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
  KW_STAT: MAINSTAT,
  KW_ATT: ATT,
  "메소 획득량": MESO,
  "아이템 드롭률": DROP,
  KW_HP: HP,
  KW_ALLSTAT: ALLSTAT,
  "크리티컬 데미지": CRITDMG,
  "데미지": DAMAGE,
  "캐릭터 기준 10레벨 당 STR": MAINSTAT_PER_10_LVLS,
  "캐릭터 기준 10레벨 당 공격력": ATT_PER_10_LVLS,
  "몬스터 방어율 무시": IED_OTHER,
  "보스 몬스터 공격 시 데미지": BOSS_OTHER,
}

ied_text = lambda x: f"몬스터 방어율 무시 : +{x}%"
boss_text = lambda x: f"보스 몬스터 공격 시 데미지 : +{x}%"
cd_text = lambda x: f"모든 스킬의 재사용 대기시간 : -{x}초(10초 이하는 {5*x}%감소 5초 미만으로 감소 불가)"
invin_text = lambda x: f"피격 후 무적시간 : +{x}초"
flat_text = lambda k, x=12: f"{k} : +{x}"

convert = {
  flat_text(KW_STAT, 10): FLAT_MAINSTAT,
  flat_text(KW_STAT, 6): FLAT_MAINSTAT,
  flat_text(KW_STAT): FLAT_MAINSTAT,
  flat_text(KW_STAT, 14): FLAT_MAINSTAT,
  flat_text(KW_STAT, 16): FLAT_MAINSTAT,
  flat_text(KW_STAT, 18): FLAT_MAINSTAT,
  flat_text(KW_ALLSTAT, 3): FLAT_ALLSTAT,
  flat_text(KW_ALLSTAT, 5): FLAT_ALLSTAT,
  flat_text(KW_HP, 60): FLAT_HP,
  flat_text(KW_HP, 100): FLAT_HP,
  flat_text(KW_HP, 120): FLAT_HP,
  flat_text(KW_HP, 180): FLAT_HP,
  flat_text(KW_HP, 240): FLAT_HP,
  flat_text(KW_HP, 300): FLAT_HP,
  flat_text(KW_ATT, 3): FLAT_ATT,
  flat_text(KW_ATT, 6): FLAT_ATT,
  flat_text(KW_ATT, 10): FLAT_ATT,
  flat_text(KW_ATT, 11): FLAT_ATT,
  flat_text(KW_ATT): FLAT_ATT,
  flat_text(KW_ATT, 14): FLAT_ATT,
  ied_text(35): IED_35,
  ied_text(40): IED_40,
  boss_text(35): BOSS_35,
  boss_text(40): BOSS_40,
  cd_text(1): COOLDOWN_1,
  cd_text(2): COOLDOWN_2,
  invin_text(1): INVIN,
  invin_text(2): INVIN,
  invin_text(3): INVIN,
  "<쓸만한 윈드 부스터> 스킬 사용 가능": DECENT_SPEED_INFUSION,
  "<쓸만한 샤프 아이즈> 스킬 사용 가능": DECENT_SHARP_EYES,
  "<쓸만한 컴뱃 오더스> 스킬 사용 가능": DECENT_COMBAT_ORDERS,
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
