from common import *

def relevant_lines(cube):
  stat = STAT | HP

  if cube & (RED | BLACK | OCCULT | MASTER | MEISTER | VIOLET | EQUALITY | UNI) != 0:
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
      SHOE: stat,
      GLOVE: stat | CRITDMG | DECENTS,
      CAPE_BELT_SHOULDER: stat,
      FACE_EYE_RING_EARRING_PENDANT: stat | MESO | DROP,
      HEART_BADGE: stat,
    }

  elif cube & BONUS != 0:
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
