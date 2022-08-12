import sys
sys.path.append("../../")
from data.utils import percent
from common import *

event = {
  VIOLET | EQUALITY: {
    HAT | TOP_OVERALL | BOTTOM | GLOVE | CAPE_BELT_SHOULDER: percent({
      RARE: [
        [MAINSTAT, 6.00],
        [HP, 6.00],
      ],
    }),
    SHOE: percent({
      RARE: [
        [MAINSTAT, 5.56],
        [HP, 5.56],
      ],
      EPIC: [
        [MAINSTAT, 11.90],
        [HP, 16.67],
        [ALLSTAT, 4.76],
      ],
      UNIQUE: [
        [MAINSTAT, 7.94],
        [HP, 9.52],
        [ALLSTAT, 6.35],
      ],
      LEGENDARY: [
        [MAINSTAT, 8.33],
        [HP, 8.33],
        [ALLSTAT, 6.25],
      ],
    }),
    FACE_EYE_RING_EARRING_PENDANT: percent({
      RARE: [
        [MAINSTAT, 6.00],
        [HP, 6.00],
      ],
      EPIC: [
        [MAINSTAT, 11.90],
        [HP, 16.67],
        [ALLSTAT, 4.76],
      ],
      UNIQUE: [
        [MAINSTAT, 9.80],
        [HP, 11.76],
        [ALLSTAT, 7.84],
      ],
      LEGENDARY: [
        [MAINSTAT, 7.84],
        [HP, 7.84],
        [ALLSTAT, 5.88],
        [MESO, 5.88],
        [DROP, 5.88],
      ],
    }),
    WEAPON | EMBLEM | SECONDARY: percent({
      RARE: [
        [ATT, 1.85],
        [IED_15, 1.85],
      ],
      EPIC: [
        [ATT, 4.00],
        [IED_15, 4.00],
      ],
    }),
    FORCE_SHIELD_SOUL_RING: percent({
      RARE: [
        [ATT, 2.08],
        [IED_15, 2.08],
      ],
      EPIC: [
        [ATT, 4.65],
        [IED_15, 4.65],
      ],
    }),
    HAT | BOTTOM | CAPE_BELT_SHOULDER: percent({
      EPIC: [
        [MAINSTAT, 11.90],
        [HP, 16.67],
        [ALLSTAT, 4.76],
      ],
    }),
    TOP_OVERALL: percent({
      EPIC: [
        [INVIN, 6.25],
        [INVIN, 6.25],
        [MAINSTAT, 10.42],
        [HP, 14.58],
        [ALLSTAT, 4.17],
      ],
      UNIQUE: [
        [INVIN, 5.48],
        [MAINSTAT, 6.85],
        [HP, 8.22],
        [ALLSTAT, 5.48],
      ],
      LEGENDARY: [
        [INVIN, 5.88],
        [MAINSTAT, 7.84],
        [HP, 7.84],
        [ALLSTAT, 5.88],
      ],
    }),
    GLOVE: percent({
      EPIC: [
        [MAINSTAT, 10.42],
        [HP, 14.58],
        [ALLSTAT, 4.17],
      ],
      UNIQUE: [
        [DECENT_SHARP_EYES, 5.97],
        [MAINSTAT, 7.46],
        [HP, 8.96],
        [ALLSTAT, 5.97],
      ],
      LEGENDARY: [
        [CRITDMG, 7.69],
        [DECENT_SPEED_INFUSION, 5.77],
        [MAINSTAT, 7.69],
        [HP, 7.69],
        [ALLSTAT, 5.77],
      ],
    }),
    HAT: percent({
      UNIQUE: [
        [MAINSTAT, 7.94],
        [HP, 9.52],
        [ALLSTAT, 6.35],
      ],
      LEGENDARY: [
        [COOLDOWN_1, 5.66],
        [COOLDOWN_2, 3.77],
        [MAINSTAT, 7.55],
        [HP, 7.55],
        [ALLSTAT, 5.66],
      ],
    }),
    BOTTOM: percent({
      UNIQUE: [
        [MAINSTAT, 7.94],
        [HP, 9.52],
        [ALLSTAT, 6.35],
      ],
      LEGENDARY: [
        [MAINSTAT, 8.89],
        [HP, 8.89],
        [ALLSTAT, 6.67],
      ],
    }),
    CAPE_BELT_SHOULDER: percent({
      UNIQUE: [
        [MAINSTAT, 8.47],
        [HP, 10.17],
        [ALLSTAT, 6.78],
      ],
      LEGENDARY: [
        [MAINSTAT, 8.89],
        [HP, 8.89],
        [ALLSTAT, 6.67],
      ],
    }),
    WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING: percent({
      UNIQUE: [
        [ATT, 6.52],
        [IED_30, 8.70],
        [BOSS_30, 6.52],
      ],
      LEGENDARY: [
        [ATT, 4.44],
        [IED_35, 6.67],
        [IED_40, 6.67],
        [BOSS_30, 4.44],
        [BOSS_35, 4.44],
        [BOSS_40, 4.44],
      ],
    }),
    EMBLEM: percent({
      UNIQUE: [
        [ATT, 6.98],
        [IED_30, 9.30],
      ],
      LEGENDARY: [
        [ATT, 5.13],
        [IED_35, 7.69],
        [IED_40, 7.69],
      ],
    }),
  },
  UNI: {
    HAT | TOP_OVERALL | BOTTOM | GLOVE | CAPE_BELT_SHOULDER: percent({
      RARE: [
        [MAINSTAT, 2.78],
        [HP, 2.78],
      ],
    }),
    SHOE: percent({
      RARE: [
        [MAINSTAT, 2.19],
        [HP, 2.19],
      ],
      EPIC: [
        [MAINSTAT, 13.70],
        [HP, 13.70],
        [ALLSTAT, 1.37],
      ],
      UNIQUE: [
        [MAINSTAT, 6.33],
        [HP, 6.33],
        [ALLSTAT, 1.27],
      ],
      LEGENDARY: [
        [MAINSTAT, 7.27],
        [HP, 7.27],
        [ALLSTAT, 1.82],
      ],
    }),
    FACE_EYE_RING_EARRING_PENDANT: percent({
      RARE: [
        [MAINSTAT, 2.78],
        [HP, 2.78],
      ],
      EPIC: [
        [MAINSTAT, 13.70],
        [HP, 13.70],
        [ALLSTAT, 1.37],
      ],
      UNIQUE: [
        [MAINSTAT, 11.63],
        [HP, 11.63],
        [ALLSTAT, 2.33],
      ],
      LEGENDARY: [
        [MAINSTAT, 6.06],
        [HP, 6.06],
        [ALLSTAT, 1.52],
        [MESO, 9.09],
        [DROP, 9.09],
      ],
    }),
    WEAPON | EMBLEM | SECONDARY: percent({
      RARE: [
        [ATT, 1.85],
        [IED_15, 1.85],
      ],
      EPIC: [
        [ATT, 4.11],
        [IED_15, 6.85],
      ],
    }),
    FORCE_SHIELD_SOUL_RING: percent({
      RARE: [
        [ATT, 2.00],
        [IED_15, 2.00],
      ],
      EPIC: [
        [ATT, 4.55],
        [IED_15, 7.58],
      ],
    }),
    HAT | BOTTOM | CAPE_BELT_SHOULDER: percent({
      EPIC: [
        [MAINSTAT, 14.08],
        [HP, 14.08],
        [ALLSTAT, 1.41],
      ],
    }),
    TOP_OVERALL: percent({
      EPIC: [
        [INVIN, 2.80],
        [INVIN, 2.80],
        [MAINSTAT, 13.08],
        [HP, 13.08],
        [ALLSTAT, 0.93],
      ],
      UNIQUE: [
        [INVIN, 8.16],
        [MAINSTAT, 4.08],
        [HP, 4.08],
        [ALLSTAT, 1.02],
      ],
      LEGENDARY: [
        [INVIN, 12.31],
        [MAINSTAT, 6.15],
        [HP, 6.15],
        [ALLSTAT, 1.54],
      ],
    }),
    GLOVE: percent({
      EPIC: [
        [MAINSTAT, 13.08],
        [HP, 13.08],
        [ALLSTAT, 0.93],
      ],
      UNIQUE: [
        [DECENT_SHARP_EYES, 8.42],
        [MAINSTAT, 5.26],
        [HP, 5.26],
        [ALLSTAT, 1.05],
      ],
      LEGENDARY: [
        [CRITDMG, 2.90],
        [DECENT_SPEED_INFUSION, 11.59],
        [MAINSTAT, 5.80],
        [HP, 5.80],
        [ALLSTAT, 1.45],
      ],
    }),
    HAT: percent({
      UNIQUE: [
        [MAINSTAT, 5.80],
        [HP, 5.80],
        [ALLSTAT, 1.45],
      ],
      LEGENDARY: [
        [COOLDOWN_1, 10.00],
        [COOLDOWN_2, 10.00],
        [MAINSTAT, 5.00],
        [HP, 5.00],
        [ALLSTAT, 1.25],
      ],
    }),
    BOTTOM: percent({
      UNIQUE: [
        [MAINSTAT, 6.35],
        [HP, 6.35],
        [ALLSTAT, 1.59],
      ],
      LEGENDARY: [
        [MAINSTAT, 8.89],
        [HP, 8.89],
        [ALLSTAT, 2.22],
      ],
    }),
    CAPE_BELT_SHOULDER: percent({
      UNIQUE: [
        [MAINSTAT, 7.69],
        [HP, 7.69],
        [ALLSTAT, 1.54],
      ],
      LEGENDARY: [
        [MAINSTAT, 8.89],
        [HP, 8.89],
        [ALLSTAT, 6.67],
      ],
    }),
    WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING: percent({
      UNIQUE: [
        [ATT, 8.22],
        [IED_30, 20.55],
        [BOSS_30, 5.48],
      ],
      LEGENDARY: [
        [ATT, 3.24],
        [IED_35, 25.89],
        [IED_40, 16.18],
        [BOSS_30, 3.07],
        [BOSS_35, 2.10],
        [BOSS_40, 1.13],
      ],
    }),
    EMBLEM: percent({
      UNIQUE: [
        [ATT, 8.70],
        [IED_30, 21.74],
      ],
      LEGENDARY: [
        [ATT, 3.45],
        [IED_35, 27.63],
        [IED_40, 17.27],
      ],
    }),
  },
}
