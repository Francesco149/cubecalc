# this file was automatically generated by /data/kms/run.sh
# do not edit, edit the scraper
import sys
from datautils import percent
from common import *

cubes = {
  CASH_MAIN: {
    WEAPON: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.2727],
        [FLAT_HP_A, 12.2727],
        [FLAT_ATT_A, 8.1818],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.1224],
        [FLAT_HP_A, 6.1224],
        [FLAT_ATT_A, 4.0816],
        [MAINSTAT_A, 6.1224],
        [ATT_A, 2.0408],
        [DAMAGE_A, 2.0408],
        [FLAT_ALLSTAT_A, 4.0816],
        [IED_C, 2.0408],
      ],
      EPIC: [
        [MAINSTAT_A, 10.8696],
        [HP_A, 10.8696],
        [ATT_A, 4.3478],
        [DAMAGE_A, 4.3478],
        [ALLSTAT_A, 4.3478],
        [IED_C, 4.3478],
      ],
      UNIQUE: [
        [MAINSTAT_A, 11.6279],
        [ATT_A, 6.9767],
        [DAMAGE_A, 6.9767],
        [ALLSTAT_A, 9.3023],
        [IED_C, 6.9767],
        [BOSS_C, 6.9767],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 9.7561],
        [ATT_A, 4.878],
        [DAMAGE_A, 4.878],
        [ALLSTAT_A, 7.3171],
        [ATT_PER_10_LVLS, 4.878],
        [IED_B, 4.878],
        [IED_A, 4.878],
        [BOSS_B, 9.7561],
        [BOSS_A, 4.878],
      ],
    }),
    EMBLEM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.2727],
        [FLAT_HP_A, 12.2727],
        [FLAT_ATT_A, 8.1818],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.1224],
        [FLAT_HP_A, 6.1224],
        [FLAT_ATT_A, 4.0816],
        [MAINSTAT_A, 6.1224],
        [ATT_A, 2.0408],
        [DAMAGE_A, 2.0408],
        [FLAT_ALLSTAT_A, 4.0816],
        [IED_C, 2.0408],
      ],
      EPIC: [
        [MAINSTAT_A, 10.8696],
        [HP_A, 10.8696],
        [ATT_A, 4.3478],
        [DAMAGE_A, 4.3478],
        [ALLSTAT_A, 4.3478],
        [IED_C, 4.3478],
      ],
      UNIQUE: [
        [MAINSTAT_A, 12.5],
        [ATT_A, 7.5],
        [DAMAGE_A, 7.5],
        [ALLSTAT_A, 10.0],
        [IED_C, 7.5],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 11.4286],
        [ATT_A, 5.7143],
        [DAMAGE_A, 5.7143],
        [ALLSTAT_A, 8.5714],
        [ATT_PER_10_LVLS, 5.7143],
        [IED_B, 5.7143],
        [IED_A, 5.7143],
      ],
    }),
    SECONDARY: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.2727],
        [FLAT_HP_A, 12.2727],
        [FLAT_ATT_A, 8.1818],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.1224],
        [FLAT_HP_A, 6.1224],
        [FLAT_ATT_A, 4.0816],
        [MAINSTAT_A, 6.1224],
        [ATT_A, 2.0408],
        [DAMAGE_A, 2.0408],
        [FLAT_ALLSTAT_A, 4.0816],
        [IED_C, 2.0408],
      ],
      EPIC: [
        [MAINSTAT_A, 10.8696],
        [HP_A, 10.8696],
        [ATT_A, 4.3478],
        [DAMAGE_A, 4.3478],
        [ALLSTAT_A, 4.3478],
        [IED_C, 4.3478],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.8039],
        [ATT_A, 5.8824],
        [DAMAGE_A, 5.8824],
        [ALLSTAT_A, 7.8431],
        [IED_C, 5.8824],
        [BOSS_C, 5.8824],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 8.5106],
        [ATT_A, 4.2553],
        [DAMAGE_A, 4.2553],
        [ALLSTAT_A, 6.383],
        [ATT_PER_10_LVLS, 4.2553],
        [IED_B, 4.2553],
        [IED_A, 4.2553],
        [BOSS_B, 8.5106],
        [BOSS_A, 4.2553],
      ],
    }),
    FORCE_SHIELD_SOUL_RING: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 14.2105],
        [FLAT_HP_A, 14.2105],
        [FLAT_ATT_A, 9.4737],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.5217],
        [FLAT_HP_A, 6.5217],
        [FLAT_ATT_A, 4.3478],
        [MAINSTAT_A, 6.5217],
        [ATT_A, 2.1739],
        [DAMAGE_A, 2.1739],
        [FLAT_ALLSTAT_A, 4.3478],
        [IED_C, 2.1739],
      ],
      EPIC: [
        [MAINSTAT_A, 12.1951],
        [HP_A, 12.1951],
        [ATT_A, 4.878],
        [DAMAGE_A, 4.878],
        [ALLSTAT_A, 4.878],
        [IED_C, 4.878],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.8039],
        [ATT_A, 5.8824],
        [DAMAGE_A, 5.8824],
        [ALLSTAT_A, 7.8431],
        [IED_C, 5.8824],
        [BOSS_C, 5.8824],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 8.5106],
        [ATT_A, 4.2553],
        [DAMAGE_A, 4.2553],
        [ALLSTAT_A, 6.383],
        [ATT_PER_10_LVLS, 4.2553],
        [IED_B, 4.2553],
        [IED_A, 4.2553],
        [BOSS_B, 8.5106],
        [BOSS_A, 4.2553],
      ],
    }),
    HAT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 8.9286],
        [HP_A, 10.7143],
        [ALLSTAT_A, 7.1429],
        [HP_ITEMS_AND_SKILLS_A, 7.1429],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 8.8889],
        [HP_A, 8.8889],
        [ALLSTAT_A, 6.6667],
        [COOLDOWN_1, 6.6667],
        [COOLDOWN_2, 4.4444],
      ],
    }),
    TOP_OVERALL: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 13.1579],
        [HP_A, 13.1579],
        [ALLSTAT_A, 5.2632],
        [INVIN, 7.8947],
      ],
      UNIQUE: [
        [MAINSTAT_A, 7.5758],
        [HP_A, 9.0909],
        [ALLSTAT_A, 6.0606],
        [INVIN, 6.0606],
        [HP_ITEMS_AND_SKILLS_A, 6.0606],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 9.3023],
        [HP_A, 9.3023],
        [ALLSTAT_A, 6.9767],
        [INVIN, 6.9767],
      ],
    }),
    BOTTOM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 8.9286],
        [HP_A, 10.7143],
        [ALLSTAT_A, 7.1429],
        [HP_ITEMS_AND_SKILLS_A, 7.1429],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 10.8108],
        [HP_A, 10.8108],
        [ALLSTAT_A, 8.1081],
      ],
    }),
    SHOE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 10.8],
        [FLAT_HP_A, 10.8],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.8182],
        [FLAT_HP_A, 6.8182],
        [MAINSTAT_A, 6.8182],
        [HP_A, 4.5455],
        [FLAT_ALLSTAT_A, 4.5455],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 8.9286],
        [HP_A, 10.7143],
        [ALLSTAT_A, 7.1429],
        [HP_ITEMS_AND_SKILLS_A, 7.1429],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 10.0],
        [HP_A, 10.0],
        [ALLSTAT_A, 7.5],
        [DECENT_COMBAT_ORDERS, 7.5],
      ],
    }),
    GLOVE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 12.1951],
        [HP_A, 12.1951],
        [ALLSTAT_A, 4.878],
      ],
      UNIQUE: [
        [MAINSTAT_A, 8.3333],
        [HP_A, 10.0],
        [ALLSTAT_A, 6.6667],
        [MAINSTAT_PER_10_LVLS, 1.6667],
        [HP_ITEMS_AND_SKILLS_A, 6.6667],
        [DECENT_SHARP_EYES, 6.6667],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 9.0909],
        [HP_A, 9.0909],
        [CRITDMG_A, 9.0909],
        [ALLSTAT_A, 6.8182],
        [DECENT_SPEED_INFUSION, 6.8182],
      ],
    }),
    CAPE_BELT_SHOULDER: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.6154],
        [HP_A, 11.5385],
        [ALLSTAT_A, 7.6923],
        [HP_ITEMS_AND_SKILLS_A, 7.6923],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 10.8108],
        [HP_A, 10.8108],
        [ALLSTAT_A, 8.1081],
      ],
    }),
    FACE_EYE_RING_EARRING_PENDANT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 11.3636],
        [HP_A, 13.6364],
        [ALLSTAT_A, 9.0909],
        [HP_ITEMS_AND_SKILLS_A, 9.0909],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 9.3023],
        [HP_A, 9.3023],
        [ALLSTAT_A, 6.9767],
        [MESO_A, 6.9767],
        [DROP_A, 6.9767],
      ],
    }),
    HEART_BADGE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8571],
        [FLAT_HP_A, 12.8571],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 7.5],
        [FLAT_HP_A, 7.5],
        [MAINSTAT_A, 7.5],
        [HP_A, 5.0],
        [FLAT_ALLSTAT_A, 5.0],
      ],
      EPIC: [
        [MAINSTAT_A, 14.2857],
        [HP_A, 14.2857],
        [ALLSTAT_A, 5.7143],
      ],
      UNIQUE: [
        [MAINSTAT_A, 11.3636],
        [HP_A, 13.6364],
        [ALLSTAT_A, 9.0909],
        [HP_ITEMS_AND_SKILLS_A, 9.0909],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 12.9032],
        [HP_A, 12.9032],
        [ALLSTAT_A, 9.6774],
      ],
    }),
  },
  NONCASH_MAIN: {
    WEAPON: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 10.4167],
        [FLAT_HP_A, 15.625],
        [FLAT_ATT_A, 5.2083],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 3.5088],
        [FLAT_HP_A, 5.2632],
        [FLAT_ATT_A, 3.5088],
        [MAINSTAT_A, 3.5088],
        [ATT_A, 1.7544],
        [DAMAGE_A, 1.7544],
        [FLAT_ALLSTAT_A, 3.5088],
        [IED_C, 1.7544],
      ],
      EPIC: [
        [MAINSTAT_A, 7.6923],
        [HP_A, 11.5385],
        [ATT_A, 3.8462],
        [DAMAGE_A, 3.8462],
        [ALLSTAT_A, 3.8462],
        [IED_C, 3.8462],
      ],
      UNIQUE: [
        [MAINSTAT_A, 13.3333],
        [ATT_A, 6.6667],
        [DAMAGE_A, 6.6667],
        [ALLSTAT_A, 6.6667],
        [IED_C, 6.6667],
        [BOSS_C, 6.6667],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 11.1111],
        [ATT_A, 5.5556],
        [DAMAGE_A, 5.5556],
        [ALLSTAT_A, 11.1111],
        [IED_B, 5.5556],
        [IED_A, 2.7778],
        [BOSS_B, 11.1111],
        [BOSS_A, 2.7778],
      ],
    }),
    EMBLEM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 10.4167],
        [FLAT_HP_A, 15.625],
        [FLAT_ATT_A, 5.2083],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 3.5088],
        [FLAT_HP_A, 5.2632],
        [FLAT_ATT_A, 3.5088],
        [MAINSTAT_A, 3.5088],
        [ATT_A, 1.7544],
        [DAMAGE_A, 1.7544],
        [FLAT_ALLSTAT_A, 3.5088],
        [IED_C, 1.7544],
      ],
      EPIC: [
        [MAINSTAT_A, 7.6923],
        [HP_A, 11.5385],
        [ATT_A, 3.8462],
        [DAMAGE_A, 3.8462],
        [ALLSTAT_A, 3.8462],
        [IED_C, 3.8462],
      ],
      UNIQUE: [
        [MAINSTAT_A, 14.2857],
        [ATT_A, 7.1429],
        [DAMAGE_A, 7.1429],
        [ALLSTAT_A, 7.1429],
        [IED_C, 7.1429],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 12.9032],
        [ATT_A, 6.4516],
        [DAMAGE_A, 6.4516],
        [ALLSTAT_A, 12.9032],
        [IED_B, 6.4516],
        [IED_A, 3.2258],
      ],
    }),
    SECONDARY: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 10.4167],
        [FLAT_HP_A, 15.625],
        [FLAT_ATT_A, 5.2083],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 3.5088],
        [FLAT_HP_A, 5.2632],
        [FLAT_ATT_A, 3.5088],
        [MAINSTAT_A, 3.5088],
        [ATT_A, 1.7544],
        [DAMAGE_A, 1.7544],
        [FLAT_ALLSTAT_A, 3.5088],
        [IED_C, 1.7544],
      ],
      EPIC: [
        [MAINSTAT_A, 5.7143],
        [HP_A, 8.5714],
        [ATT_A, 2.8571],
        [DAMAGE_A, 2.8571],
        [ALLSTAT_A, 2.8571],
        [IED_C, 2.8571],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.5238],
        [ATT_A, 4.7619],
        [DAMAGE_A, 4.7619],
        [ALLSTAT_A, 4.7619],
        [IED_C, 4.7619],
        [BOSS_C, 4.7619],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 8.3333],
        [ATT_A, 4.1667],
        [DAMAGE_A, 4.1667],
        [ALLSTAT_A, 8.3333],
        [IED_B, 4.1667],
        [IED_A, 2.0833],
        [BOSS_B, 8.3333],
        [BOSS_A, 2.0833],
      ],
    }),
    FORCE_SHIELD_SOUL_RING: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 12.8205],
        [FLAT_HP_A, 19.2308],
        [FLAT_ATT_A, 6.4103],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 3.9216],
        [FLAT_HP_A, 5.8824],
        [FLAT_ATT_A, 3.9216],
        [MAINSTAT_A, 3.9216],
        [ATT_A, 1.9608],
        [DAMAGE_A, 1.9608],
        [FLAT_ALLSTAT_A, 3.9216],
        [IED_C, 1.9608],
      ],
      EPIC: [
        [MAINSTAT_A, 6.8966],
        [HP_A, 10.3448],
        [ATT_A, 3.4483],
        [DAMAGE_A, 3.4483],
        [ALLSTAT_A, 3.4483],
        [IED_C, 3.4483],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.5238],
        [ATT_A, 4.7619],
        [DAMAGE_A, 4.7619],
        [ALLSTAT_A, 4.7619],
        [IED_C, 4.7619],
        [BOSS_C, 4.7619],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 8.3333],
        [ATT_A, 4.1667],
        [DAMAGE_A, 4.1667],
        [ALLSTAT_A, 8.3333],
        [IED_B, 4.1667],
        [IED_A, 2.0833],
        [BOSS_B, 8.3333],
        [BOSS_A, 2.0833],
      ],
    }),
    HAT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 5.2083],
        [FLAT_HP_A, 7.8125],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 7.4074],
        [HP_A, 11.1111],
        [ALLSTAT_A, 3.7037],
      ],
      UNIQUE: [
        [MAINSTAT_A, 6.8966],
        [HP_A, 10.3448],
        [ALLSTAT_A, 3.4483],
        [HP_ITEMS_AND_SKILLS_A, 10.3448],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [ALLSTAT_A, 5.5556],
        [HP_ITEMS_AND_SKILLS_A, 8.3333],
        [COOLDOWN_1, 8.3333],
        [COOLDOWN_2, 5.5556],
      ],
    }),
    TOP_OVERALL: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 6.6667],
        [HP_A, 10.0],
        [ALLSTAT_A, 3.3333],
        [INVIN, 10.0],
      ],
      UNIQUE: [
        [MAINSTAT_A, 6.0606],
        [HP_A, 9.0909],
        [ALLSTAT_A, 3.0303],
        [INVIN, 9.0909],
        [HP_ITEMS_AND_SKILLS_A, 9.0909],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 5.8824],
        [HP_A, 8.8235],
        [ALLSTAT_A, 5.8824],
        [INVIN, 8.8235],
        [HP_ITEMS_AND_SKILLS_A, 8.8235],
      ],
    }),
    BOTTOM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 7.4074],
        [HP_A, 11.1111],
        [ALLSTAT_A, 3.7037],
      ],
      UNIQUE: [
        [MAINSTAT_A, 6.8966],
        [HP_A, 10.3448],
        [ALLSTAT_A, 3.4483],
        [HP_ITEMS_AND_SKILLS_A, 10.3448],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 5.8824],
        [HP_A, 8.8235],
        [ALLSTAT_A, 5.8824],
        [HP_ITEMS_AND_SKILLS_A, 8.8235],
      ],
    }),
    SHOE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2464],
        [FLAT_HP_A, 10.8696],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 7.1429],
        [MAINSTAT_A, 4.7619],
        [HP_A, 7.1429],
        [FLAT_ALLSTAT_A, 4.7619],
      ],
      EPIC: [
        [MAINSTAT_A, 7.4074],
        [HP_A, 11.1111],
        [ALLSTAT_A, 3.7037],
      ],
      UNIQUE: [
        [MAINSTAT_A, 6.8966],
        [HP_A, 10.3448],
        [ALLSTAT_A, 3.4483],
        [HP_ITEMS_AND_SKILLS_A, 10.3448],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 6.4516],
        [HP_A, 9.6774],
        [ALLSTAT_A, 6.4516],
        [HP_ITEMS_AND_SKILLS_A, 9.6774],
        [DECENT_COMBAT_ORDERS, 9.6774],
      ],
    }),
    GLOVE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 6.0606],
        [HP_A, 9.0909],
        [ALLSTAT_A, 3.0303],
      ],
      UNIQUE: [
        [MAINSTAT_A, 5.7143],
        [HP_A, 8.5714],
        [ALLSTAT_A, 2.8571],
        [HP_ITEMS_AND_SKILLS_A, 8.5714],
        [DECENT_SHARP_EYES, 5.7143],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 4.5455],
        [HP_A, 6.8182],
        [CRITDMG_A, 9.0909],
        [ALLSTAT_A, 4.5455],
        [HP_ITEMS_AND_SKILLS_A, 6.8182],
        [AUTOSTEAL_C, 6.8182],
        [AUTOSTEAL_B, 6.8182],
        [AUTOSTEAL_A, 6.8182],
        [DECENT_SPEED_INFUSION, 6.8182],
      ],
    }),
    CAPE_BELT_SHOULDER: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 7.4074],
        [HP_A, 11.1111],
        [ALLSTAT_A, 3.7037],
      ],
      UNIQUE: [
        [MAINSTAT_A, 7.4074],
        [HP_A, 11.1111],
        [ALLSTAT_A, 3.7037],
        [HP_ITEMS_AND_SKILLS_A, 11.1111],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 7.1429],
        [HP_A, 10.7143],
        [ALLSTAT_A, 7.1429],
        [HP_ITEMS_AND_SKILLS_A, 10.7143],
      ],
    }),
    FACE_EYE_RING_EARRING_PENDANT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 7.1429],
        [MAINSTAT_A, 4.7619],
        [HP_A, 7.1429],
        [FLAT_ALLSTAT_A, 4.7619],
      ],
      EPIC: [
        [MAINSTAT_A, 11.1111],
        [HP_A, 16.6667],
        [ALLSTAT_A, 5.5556],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.5238],
        [HP_A, 14.2857],
        [ALLSTAT_A, 4.7619],
        [HP_ITEMS_AND_SKILLS_A, 14.2857],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 5.8824],
        [HP_A, 8.8235],
        [ALLSTAT_A, 5.8824],
        [HP_ITEMS_AND_SKILLS_A, 8.8235],
        [MESO_A, 8.8235],
        [DROP_A, 8.8235],
      ],
    }),
    HEART_BADGE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 9.8039],
        [FLAT_HP_A, 14.7059],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 5.5556],
        [FLAT_HP_A, 8.3333],
        [MAINSTAT_A, 5.5556],
        [HP_A, 8.3333],
        [FLAT_ALLSTAT_A, 5.5556],
      ],
      EPIC: [
        [MAINSTAT_A, 11.1111],
        [HP_A, 16.6667],
        [ALLSTAT_A, 5.5556],
      ],
      UNIQUE: [
        [MAINSTAT_A, 9.5238],
        [HP_A, 14.2857],
        [ALLSTAT_A, 4.7619],
        [HP_ITEMS_AND_SKILLS_A, 14.2857],
      ],
      LEGENDARY: [
        [MAINSTAT_A, 9.0909],
        [HP_A, 13.6364],
        [ALLSTAT_A, 9.0909],
        [HP_ITEMS_AND_SKILLS_A, 13.6364],
      ],
    }),
  },
  BONUS: {
    WEAPON: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_HP_A, 5.8824],
        [FLAT_MAINSTAT_A, 5.8824],
        [FLAT_ATT_A, 3.9216],
        [HP_A, 3.9216],
        [MAINSTAT_A, 3.9216],
        [ATT_A, 1.9608],
        [DAMAGE_A, 1.9608],
        [FLAT_ALLSTAT_A, 5.8824],
      ],
      EPIC: [
        [HP_A, 8.8235],
        [ATT_A, 5.8824],
        [MAINSTAT_A, 8.8235],
        [DAMAGE_A, 2.9412],
        [ALLSTAT_A, 5.8824],
        [IED_C, 5.8824],
      ],
      UNIQUE: [
        [HP_A, 6.9767],
        [ATT_A, 4.6512],
        [MAINSTAT_A, 6.9767],
        [DAMAGE_A, 2.3256],
        [ALLSTAT_A, 4.6512],
        [MAINSTAT_PER_10_LVLS, 4.6512],
        [IED_C, 2.3256],
        [BOSS_C, 2.3256],
      ],
      LEGENDARY: [
        [HP_A, 7.6923],
        [ATT_A, 5.1282],
        [MAINSTAT_A, 7.6923],
        [DAMAGE_A, 2.5641],
        [ALLSTAT_A, 5.1282],
        [MAINSTAT_PER_10_LVLS, 5.1282],
        [ATT_PER_10_LVLS, 2.5641],
        [IED_C, 2.5641],
        [BOSS_C, 2.5641],
      ],
    }),
    EMBLEM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_HP_A, 5.8824],
        [FLAT_MAINSTAT_A, 5.8824],
        [FLAT_ATT_A, 3.9216],
        [HP_A, 3.9216],
        [MAINSTAT_A, 3.9216],
        [ATT_A, 1.9608],
        [DAMAGE_A, 1.9608],
        [FLAT_ALLSTAT_A, 5.8824],
      ],
      EPIC: [
        [HP_A, 8.8235],
        [ATT_A, 5.8824],
        [MAINSTAT_A, 8.8235],
        [DAMAGE_A, 2.9412],
        [ALLSTAT_A, 5.8824],
        [IED_C, 5.8824],
      ],
      UNIQUE: [
        [HP_A, 7.1429],
        [ATT_A, 4.7619],
        [MAINSTAT_A, 7.1429],
        [DAMAGE_A, 2.381],
        [ALLSTAT_A, 4.7619],
        [MAINSTAT_PER_10_LVLS, 4.7619],
        [IED_C, 2.381],
      ],
      LEGENDARY: [
        [HP_A, 7.8947],
        [ATT_A, 5.2632],
        [MAINSTAT_A, 7.8947],
        [DAMAGE_A, 2.6316],
        [ALLSTAT_A, 5.2632],
        [MAINSTAT_PER_10_LVLS, 5.2632],
        [ATT_PER_10_LVLS, 2.6316],
        [IED_C, 2.6316],
      ],
    }),
    SECONDARY: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_HP_A, 5.8824],
        [FLAT_MAINSTAT_A, 5.8824],
        [FLAT_ATT_A, 3.9216],
        [HP_A, 3.9216],
        [MAINSTAT_A, 3.9216],
        [ATT_A, 1.9608],
        [DAMAGE_A, 1.9608],
        [FLAT_ALLSTAT_A, 5.8824],
      ],
      EPIC: [
        [HP_A, 8.8235],
        [ATT_A, 5.8824],
        [MAINSTAT_A, 8.8235],
        [DAMAGE_A, 2.9412],
        [ALLSTAT_A, 5.8824],
        [IED_C, 5.8824],
      ],
      UNIQUE: [
        [HP_A, 6.9767],
        [ATT_A, 4.6512],
        [MAINSTAT_A, 6.9767],
        [DAMAGE_A, 2.3256],
        [ALLSTAT_A, 4.6512],
        [MAINSTAT_PER_10_LVLS, 4.6512],
        [IED_C, 2.3256],
        [BOSS_C, 2.3256],
      ],
      LEGENDARY: [
        [HP_A, 7.3171],
        [ATT_A, 4.878],
        [CRITDMG_A, 4.878],
        [MAINSTAT_A, 7.3171],
        [DAMAGE_A, 2.439],
        [ALLSTAT_A, 4.878],
        [MAINSTAT_PER_10_LVLS, 4.878],
        [ATT_PER_10_LVLS, 2.439],
        [IED_C, 2.439],
        [BOSS_C, 2.439],
      ],
    }),
    FORCE_SHIELD_SOUL_RING: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_HP_A, 5.8824],
        [FLAT_MAINSTAT_A, 5.8824],
        [FLAT_ATT_A, 3.9216],
        [HP_A, 3.9216],
        [MAINSTAT_A, 3.9216],
        [ATT_A, 1.9608],
        [DAMAGE_A, 1.9608],
        [FLAT_ALLSTAT_A, 5.8824],
      ],
      EPIC: [
        [HP_A, 8.8235],
        [ATT_A, 5.8824],
        [MAINSTAT_A, 8.8235],
        [DAMAGE_A, 2.9412],
        [ALLSTAT_A, 5.8824],
        [IED_C, 5.8824],
      ],
      UNIQUE: [
        [HP_A, 6.9767],
        [ATT_A, 4.6512],
        [MAINSTAT_A, 6.9767],
        [DAMAGE_A, 2.3256],
        [ALLSTAT_A, 4.6512],
        [MAINSTAT_PER_10_LVLS, 4.6512],
        [IED_C, 2.3256],
        [BOSS_C, 2.3256],
      ],
      LEGENDARY: [
        [HP_A, 7.3171],
        [ATT_A, 4.878],
        [CRITDMG_A, 4.878],
        [MAINSTAT_A, 7.3171],
        [DAMAGE_A, 2.439],
        [ALLSTAT_A, 4.878],
        [MAINSTAT_PER_10_LVLS, 4.878],
        [ATT_PER_10_LVLS, 2.439],
        [IED_C, 2.439],
        [BOSS_C, 2.439],
      ],
    }),
    HAT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.5455],
        [FLAT_HP_A, 4.5455],
        [FLAT_ATT_A, 3.0303],
        [MAINSTAT_A, 3.0303],
        [HP_A, 4.5455],
        [CRITDMG_A, 3.0303],
        [ALLSTAT_A, 3.0303],
        [MAINSTAT_PER_10_LVLS, 3.0303],
        [HP_ITEMS_AND_SKILLS_A, 4.5455],
        [COOLDOWN_1, 4.5455],
        [MESO_A, 4.5455],
        [DROP_A, 4.5455],
      ],
    }),
    TOP_OVERALL: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 4.7619],
        [FLAT_ATT_A, 3.1746],
        [MAINSTAT_A, 3.1746],
        [HP_A, 4.7619],
        [CRITDMG_A, 3.1746],
        [ALLSTAT_A, 3.1746],
        [MAINSTAT_PER_10_LVLS, 3.1746],
        [HP_ITEMS_AND_SKILLS_A, 4.7619],
        [MESO_A, 4.7619],
        [DROP_A, 4.7619],
      ],
    }),
    BOTTOM: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 4.7619],
        [FLAT_ATT_A, 3.1746],
        [MAINSTAT_A, 3.1746],
        [HP_A, 4.7619],
        [CRITDMG_A, 3.1746],
        [ALLSTAT_A, 3.1746],
        [MAINSTAT_PER_10_LVLS, 3.1746],
        [HP_ITEMS_AND_SKILLS_A, 4.7619],
        [MESO_A, 4.7619],
        [DROP_A, 4.7619],
      ],
    }),
    SHOE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 4.7619],
        [FLAT_ATT_A, 3.1746],
        [MAINSTAT_A, 3.1746],
        [HP_A, 4.7619],
        [CRITDMG_A, 3.1746],
        [ALLSTAT_A, 3.1746],
        [MAINSTAT_PER_10_LVLS, 3.1746],
        [HP_ITEMS_AND_SKILLS_A, 4.7619],
        [MESO_A, 4.7619],
        [DROP_A, 4.7619],
      ],
    }),
    GLOVE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.6154],
        [FLAT_HP_A, 4.6154],
        [FLAT_ATT_A, 3.0769],
        [MAINSTAT_A, 3.0769],
        [HP_A, 4.6154],
        [CRITDMG_A, 3.0769],
        [ALLSTAT_A, 3.0769],
        [MAINSTAT_PER_10_LVLS, 3.0769],
        [HP_ITEMS_AND_SKILLS_A, 4.6154],
        [MESO_A, 4.6154],
        [DROP_A, 4.6154],
      ],
    }),
    CAPE_BELT_SHOULDER: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.7619],
        [FLAT_HP_A, 4.7619],
        [FLAT_ATT_A, 3.1746],
        [MAINSTAT_A, 3.1746],
        [HP_A, 4.7619],
        [CRITDMG_A, 3.1746],
        [ALLSTAT_A, 3.1746],
        [MAINSTAT_PER_10_LVLS, 3.1746],
        [HP_ITEMS_AND_SKILLS_A, 4.7619],
        [MESO_A, 4.7619],
        [DROP_A, 4.7619],
      ],
    }),
    FACE_EYE_RING_EARRING_PENDANT: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.6875],
        [FLAT_HP_A, 4.6875],
        [FLAT_ATT_A, 3.125],
        [MAINSTAT_A, 3.125],
        [HP_A, 4.6875],
        [ALLSTAT_A, 3.125],
        [MAINSTAT_PER_10_LVLS, 3.125],
        [HP_ITEMS_AND_SKILLS_A, 4.6875],
        [MESO_A, 4.6875],
        [DROP_A, 4.6875],
      ],
    }),
    HEART_BADGE: percent({
      COMMON: [
        [FLAT_MAINSTAT_A, 7.2622],
        [FLAT_HP_A, 10.8932],
        [FLAT_ATT_A, 7.2622],
      ],
      RARE: [
        [FLAT_MAINSTAT_A, 6.383],
        [FLAT_HP_A, 6.383],
        [FLAT_ATT_A, 4.2553],
        [MAINSTAT_A, 4.2553],
        [HP_A, 4.2553],
        [FLAT_ALLSTAT_A, 4.2553],
      ],
      EPIC: [
        [FLAT_MAINSTAT_A, 6.0],
        [FLAT_HP_A, 6.0],
        [FLAT_ATT_A, 4.0],
        [MAINSTAT_A, 4.0],
        [HP_A, 6.0],
        [ALLSTAT_A, 4.0],
      ],
      UNIQUE: [
        [FLAT_MAINSTAT_A, 5.4545],
        [FLAT_HP_A, 5.4545],
        [FLAT_ATT_A, 3.6364],
        [MAINSTAT_A, 3.6364],
        [HP_A, 5.4545],
        [ALLSTAT_A, 3.6364],
        [MAINSTAT_PER_10_LVLS, 3.6364],
        [HP_ITEMS_AND_SKILLS_A, 5.4545],
      ],
      LEGENDARY: [
        [FLAT_MAINSTAT_A, 4.918],
        [FLAT_HP_A, 4.918],
        [FLAT_ATT_A, 3.2787],
        [MAINSTAT_A, 3.2787],
        [HP_A, 4.918],
        [ALLSTAT_A, 3.2787],
        [MAINSTAT_PER_10_LVLS, 3.2787],
        [HP_ITEMS_AND_SKILLS_A, 4.918],
        [MESO_A, 4.918],
        [DROP_A, 4.918],
      ],
    }),
  },
}
