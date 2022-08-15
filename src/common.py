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

  # special internal values used for caching
  COMBOS = auto()
  NAME = auto()
  DEFAULT_CUBE = auto()

category_names = {
  SECONDARY: "2ndary excl. force shield/soul ring",
  FORCE_SHIELD_SOUL_RING: "force shield/soul ring",
  TOP_OVERALL: "top/overall",
  CAPE_BELT_SHOULDER: "cape/belt/shoulder",
  FACE_EYE_RING_EARRING_PENDANT: "accessory (face/eye/ring/ear/pend)",
  HEART_BADGE: "heart/badge",
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
  BOSS_30 = 1
  BOSS_35 = auto()
  BOSS_40 = auto()
  IED_15 = auto()
  IED_30 = auto()
  IED_35 = auto()
  IED_40 = auto()
  ATT = auto()
  ANY = auto()
  MAINSTAT = auto()
  ALLSTAT = auto()
  HP = auto()
  COOLDOWN_1 = auto()
  COOLDOWN_2 = auto()
  CRITDMG = auto()
  MESO = auto()
  DROP = auto()
  INVIN = auto()
  DECENT_SPEED_INFUSION = auto()
  DECENT_SHARP_EYES = auto()
  DECENT_COMBAT_ORDERS = auto()
  FLAT_ATT = auto()
  FLAT_MAINSTAT = auto()
  FLAT_ALLSTAT = auto()
  FLAT_HP = auto()

  # special keys for matching lines
  LINES = auto() # match by number of lines and what lines are allowed


BOSS = BOSS_30 | BOSS_35 | BOSS_40
STAT = MAINSTAT | ALLSTAT
IED = IED_15 | IED_30 | IED_35 | IED_40
COOLDOWN = COOLDOWN_1 | COOLDOWN_2
DECENTS = DECENT_SPEED_INFUSION | DECENT_SHARP_EYES | DECENT_COMBAT_ORDERS

@global_enum
class Tier(IntEnum):
  COMMON = 1
  RARE = auto()
  EPIC = auto()
  UNIQUE = auto()
  LEGENDARY = auto()

TIER_DEFAULT = LEGENDARY

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

NONCASH_MAIN = OCCULT | MASTER | MEISTER
CASH_MAIN = RED | BLACK
