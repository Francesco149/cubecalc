from common import *
from functools import reduce
from operator import or_, add

def relevant_lines(cube):
  stat = STAT | HP

  if cube & (RED | BLACK | OCCULT | MASTER | MEISTER | VIOLET | EQUALITY | UNI):
    e = IED | ATT
    ws = e | BOSS
    lines = {
      WEAPON: ws,
      EMBLEM: e,
      SECONDARY: ws,
      FORCE_SHIELD_SOUL_RING: ws,
      HAT: stat | COOLDOWN,
      TOP_OVERALL: stat | INVIN,
      BOTTOM: stat,
      SHOE: stat | DECENTS,
      GLOVE: stat | CRITDMG | DECENTS,
      CAPE_BELT_SHOULDER: stat,
      FACE_EYE_RING_EARRING_PENDANT: stat | MESO | DROP,
      HEART_BADGE: stat,
    }

  elif cube & BONUS:
    e = IED | ATT
    ws = e | BOSS
    stat = STAT | HP | DROP | MESO | CRITDMG | FLAT_ATT

    lines = {
      WEAPON: ATT,
      EMBLEM: ATT,
      SECONDARY: ATT,
      FORCE_SHIELD_SOUL_RING: ATT,
      HAT: stat | COOLDOWN,
      TOP_OVERALL: stat,
      BOTTOM: stat,
      SHOE: stat,
      GLOVE: stat,
      CAPE_BELT_SHOULDER: stat,
      FACE_EYE_RING_EARRING_PENDANT: stat,
      HEART_BADGE: stat,
    }

  return lines


def percent(lines):
  for k in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]:
    if k in lines:
      lines[k] = [[x[0], 1/x[1]*100] for x in lines[k]]
  return lines


empty_tiers = {x: [] for x in [COMMON, RARE, EPIC, UNIQUE, LEGENDARY]}

def find_probabilities(data, cubes_mask, categories_mask):
  """
  find all the dicts that match both the desired cubes and categories and merge them
  data format is assumed to be the same as data/tms/__init__.py
  """
  cubedatas = [v for k, v in data.items() if k & cubes_mask]
  probabilities = reduce(add, [[v for k, v in x.items() if k & categories_mask] for x in cubedatas])
  info = {
    NAME: category_name(categories_mask),
    DEFAULT_CUBE: MEISTER if cubes_mask & NONCASH_MAIN else [x for x in Cube if x & cubes_mask],
  }
  return empty_tiers | info | reduce(or_, probabilities, {})
