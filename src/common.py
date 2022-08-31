from enum import IntEnum, IntFlag, auto

def global_enum(enum):
  globals().update(enum.__members__)
  return enum

@global_enum
class Category(IntFlag):
  WEAPON = 1
  EMBLEM = auto()
  SECONDARY = auto()
  FORCE_SHIELD_SOUL_RING = auto()
  HAT = auto()
  TOP_OVERALL = auto()
  BOTTOM = auto()
  SHOE = auto()
  GLOVE = auto()
  CAPE_BELT_SHOULDER = auto()
  FACE_EYE_RING_EARRING_PENDANT = auto()
  HEART_BADGE = auto()
  FAMILIAR_STATS = auto()

  # special internal values used for caching
  LINE_CACHE = auto()
  NAME = auto()
  DEFAULT_CUBE = auto()

category_names = {
  SECONDARY: "2ndary excl. force shield/soul ring",
  FORCE_SHIELD_SOUL_RING: "force shield/soul ring",
  TOP_OVERALL: "top/overall",
  CAPE_BELT_SHOULDER: "cape/belt/shoulder",
  FACE_EYE_RING_EARRING_PENDANT: "accessory (face/eye/ring/ear/pend)",
  HEART_BADGE: "heart/badge",
  FAMILIAR_STATS: "familiar",
}

combined_category_names = {
  SECONDARY | FORCE_SHIELD_SOUL_RING: "2ndary/force shield/soul ring",
}

enumbits = lambda v, e: [x for x in e if v & x]

def category_name(c):
  combined = []
  for x in combined_category_names.keys():
    if c & x == x:
      combined += [combined_category_names[x]]
      c &= ~x
  return ", ".join([category_names[x] if x in category_names else x.name.lower()
                    for x in enumbits(c, Category)] + combined)

@global_enum
class Line(IntFlag):

  # lines are bitmasks of the line type and variant
  # the line type is self explanatory: just ied, boss, etc
  # the line variant are special bits (A, B, C, D, ...) that determine the amount for lines that
  #   appear multiple times with different amounts in the same tier, for example:
  #   IED | LINE_A = 40% ied
  #   IED | LINE_B = 35% ied
  # this way we compress the line bitmask in as little bits as possible while still enabling
  #   quick scanning of line types through bitmasks

  LINE_A = auto()
  LINE_B = auto()
  LINE_C = auto()
  LINE_D = auto()

  ANY = auto()
  BOSS_ONLY = auto()
  DAMAGE = auto()
  IED = auto()
  ATT = auto()
  MAINSTAT = auto()
  ALLSTAT = auto()
  HP = auto()
  COOLDOWN = auto()
  CRITDMG = auto()
  DROP_MESO = auto()
  MESO_ONLY = auto()
  DROP_ONLY = auto()
  INVIN = auto()
  DECENT_SPEED_INFUSION = auto()
  DECENT_SHARP_EYES = auto()
  DECENT_COMBAT_ORDERS = auto()
  FLAT_ATT = auto()
  FLAT_MAINSTAT = auto()
  FLAT_ALLSTAT = auto()
  FLAT_HP = auto()
  MAINSTAT_PER_10_LVLS = auto()
  ATT_PER_10_LVLS = auto()
  FLAT_MESO = auto()

  # special keys for matching lines
  LINES = auto() # match by number of lines and what lines are allowed

@global_enum
class LineVariants(IntFlag):
  BOSS_A = BOSS_ONLY | LINE_A
  BOSS_B = BOSS_ONLY | LINE_B
  BOSS_C = BOSS_ONLY | LINE_C
  DAMAGE_A = DAMAGE | LINE_A
  DAMAGE_B = DAMAGE | LINE_B
  IED_A = IED | LINE_A
  IED_B = IED | LINE_B
  IED_C = IED | LINE_C
  COOLDOWN_1 = COOLDOWN | LINE_A
  COOLDOWN_2 = COOLDOWN | LINE_B
  CRITDMG_A = CRITDMG | LINE_A
  CRITDMG_B = CRITDMG | LINE_B
  SMALL_DROP_MESO = DROP_MESO | LINE_A
  NORMAL_DROP_MESO = DROP_MESO | LINE_B
  LARGE_DROP_MESO = DROP_MESO | LINE_C
  SMALL_MESO = MESO_ONLY | LINE_A
  MESO_A = MESO_ONLY | LINE_B
  LARGE_MESO = MESO_ONLY | LINE_C
  SMALL_DROP = DROP_ONLY | LINE_A
  DROP_A = DROP_ONLY | LINE_B
  LARGE_DROP = DROP_ONLY | LINE_C
  FLAT_MAINSTAT_A = FLAT_MAINSTAT | LINE_A
  FLAT_MAINSTAT_B = FLAT_MAINSTAT | LINE_B
  FLAT_ALLSTAT_A = FLAT_ALLSTAT | LINE_A
  FLAT_ALLSTAT_B = FLAT_ALLSTAT | LINE_B
  FLAT_ALLSTAT_C = FLAT_ALLSTAT | LINE_C
  FLAT_ALLSTAT_D = FLAT_ALLSTAT | LINE_D

@global_enum
class LineMasks(IntFlag):
  BOSS = BOSS_ONLY | DAMAGE
  STAT = MAINSTAT | ALLSTAT
  FLAT_STAT = FLAT_MAINSTAT | FLAT_ALLSTAT
  DECENTS = DECENT_SPEED_INFUSION | DECENT_SHARP_EYES | DECENT_COMBAT_ORDERS
  MESO = MESO_ONLY | DROP_MESO
  DROP = DROP_ONLY | DROP_MESO

@global_enum
class Tier(IntEnum):
  BASE = 1
  COMMON = auto()
  RARE = auto()
  EPIC = auto()
  UNIQUE = auto()
  LEGENDARY = auto()

@global_enum
class Cube(IntFlag):
  RED = 1
  MEISTER = auto()
  MASTER = auto()
  OCCULT = auto()
  BLACK = auto()
  VIOLET = auto()
  EQUALITY = auto()
  BONUS = auto()
  UNI = auto()
  FAMILIAR = auto()
  RED_FAM_CARD = auto()

@global_enum
class CubeMasks(IntFlag):
  NONCASH_MAIN = OCCULT | MASTER | MEISTER
  CASH_MAIN = RED | BLACK

@global_enum
class Region(IntFlag):
  KMS = 1
  MSEA = auto()
  GMS = auto()
  JMS = auto()
  TMS = auto()
  CMS = auto()

@global_enum
class RegionMasks(IntFlag):
  HAS_GMS_LINES = GMS | TMS
  NO_FLAME_ADVANTAGE = CMS | TMS # unused, just a reminder for myself

tier_limits = {
  OCCULT: EPIC,
  MASTER: UNIQUE,
}
