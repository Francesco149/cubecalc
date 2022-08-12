import sys
sys.path.append("../../")
from data.utils import percent
from common import *

# cash cubes (red, black)
cash = {
  WEAPON: percent({
    COMMON: [],
    RARE: [
      [ATT, 2.0408],
    ],
    EPIC: [
      [ATT, 4.3478],
    ],
    UNIQUE: [
      [ATT, 6.9767],
      [IED_30, 6.9767],
      [BOSS_30, 6.9767],
    ],
    LEGENDARY: [
      [ATT, 4.878],
      [IED_35, 4.878],
      [IED_40, 4.878],
      [BOSS_35, 9.7561],
      [BOSS_40, 4.878],
    ],
  }),
  
  EMBLEM: percent({
    COMMON: [],
    RARE: [
      [ATT, 2.0408],
    ],
    EPIC: [
      [ATT, 4.3478],
    ],
    UNIQUE: [
      [ATT, 7.5],
      [IED_30, 7.5],
    ],
    LEGENDARY: [
      [ATT, 5.7143],
      [IED_35, 5.7143],
      [IED_40, 5.7143],
    ],
  }),
  
  SECONDARY: percent({
    COMMON: [],
    RARE: [
      [ATT, 2.0408],
    ],
    EPIC: [
      [ATT, 4.3478],
    ],
    UNIQUE: [
      [ATT, 5.8824],
      [IED_30, 5.8824],
      [BOSS_30, 5.8824],
    ],
    LEGENDARY: [
      [ATT, 4.2553],
      [IED_35, 4.2553],
      [IED_40, 4.2553],
      [BOSS_35, 8.5106],
      [BOSS_40, 4.2553],
    ],
  }),
  
  FORCE_SHIELD_SOUL_RING: percent({
    COMMON: [],
    RARE: [
      [ATT, 2.1739],
    ],
    EPIC: [
      [ATT, 4.878],
    ],
    UNIQUE: [
      [ATT, 5.8824],
      [IED_30, 5.8824],
      [BOSS_30, 5.8824],
    ],
    LEGENDARY: [
      [ATT, 4.2553],
      [IED_35, 4.2553],
      [IED_40, 4.2553],
      [BOSS_35, 8.5106],
      [BOSS_40, 4.2553],
    ],
  }),
  
  HAT: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 8.9286],
      [HP, 10.7143],
      [ALLSTAT, 7.1429],
    ],
    LEGENDARY: [
      [MAINSTAT, 8.8889],
      [HP, 8.8889],
      [ALLSTAT, 6.6667],
      [COOLDOWN_1, 6.6667],
      [COOLDOWN_2, 4.4444],
    ],
  }),
  
  TOP_OVERALL: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 13.1579],
      [HP, 13.1579],
      [ALLSTAT, 5.2632],
      [INVIN, 7.8947],
    ],
    UNIQUE: [
      [MAINSTAT, 7.5758],
      [HP, 9.0909],
      [ALLSTAT, 6.0606],
      [INVIN, 6.0606],
    ],
    LEGENDARY: [
      [MAINSTAT, 9.3023],
      [HP, 9.3023],
      [ALLSTAT, 6.9767],
      [INVIN, 6.9767],
    ],
  }),
  
  BOTTOM: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 8.9286],
      [HP, 10.7143],
      [ALLSTAT, 7.1429],
    ],
    LEGENDARY: [
      [MAINSTAT, 10.8108],
      [HP, 10.8108],
      [ALLSTAT, 8.1081],
    ],
  }),
  
  SHOE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 6.8182],
      [HP, 4.5455],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 8.9286],
      [HP, 10.7143],
      [ALLSTAT, 7.1429],
    ],
    LEGENDARY: [
      [MAINSTAT, 10.0],
      [HP, 10.0],
      [ALLSTAT, 7.5],
    ],
  }),
  
  GLOVE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 12.1951],
      [HP, 12.1951],
      [ALLSTAT, 4.878],
    ],
    UNIQUE: [
      [MAINSTAT, 8.3333],
      [HP, 10.0],
      [ALLSTAT, 6.6667],
      [DECENT_SHARP_EYES, 6.6667],
    ],
    LEGENDARY: [
      [MAINSTAT, 9.0909],
      [HP, 9.0909],
      [CRITDMG, 9.0909],
      [ALLSTAT, 6.8182],
      [DECENT_SPEED_INFUSION, 6.8182],
    ],
  }),
  
  CAPE_BELT_SHOULDER: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 9.6154],
      [HP, 11.5385],
      [ALLSTAT, 7.6923],
    ],
    LEGENDARY: [
      [MAINSTAT, 10.8108],
      [HP, 10.8108],
      [ALLSTAT, 8.1081],
    ],
  }),
  
  FACE_EYE_RING_EARRING_PENDANT: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 11.3636],
      [HP, 13.6364],
      [ALLSTAT, 9.0909],
    ],
    LEGENDARY: [
      [MAINSTAT, 9.3023],
      [HP, 9.3023],
      [ALLSTAT, 6.9767],
      [MESO, 6.9767],
      [DROP, 6.9767],
    ],
  }),
  
  HEART_BADGE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 7.5],
      [HP, 5.0],
    ],
    EPIC: [
      [MAINSTAT, 14.2857],
      [HP, 14.2857],
      [ALLSTAT, 5.7143],
    ],
    UNIQUE: [
      [MAINSTAT, 11.3636],
      [HP, 13.6364],
      [ALLSTAT, 9.0909],
    ],
    LEGENDARY: [
      [MAINSTAT, 12.9032],
      [HP, 12.9032],
      [ALLSTAT, 9.6774],
    ],
  }),
  
}

# non-cash cubes (occult/suspicious, master/yellow, meister/artisan/purple)
noncash = {
  WEAPON: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.7544],
    ],
    EPIC: [
      [ATT, 3.8462],
    ],
    UNIQUE: [
      [ATT, 6.6667],
      [IED_30, 6.6667],
      [BOSS_30, 6.6667],
    ],
    LEGENDARY: [
      [ATT, 5.5556],
      [IED_35, 5.5556],
      [IED_40, 2.7778],
      [BOSS_35, 11.1111],
      [BOSS_40, 2.7778],
    ],
  }),
  
  EMBLEM: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.7544],
    ],
    EPIC: [
      [ATT, 3.8462],
    ],
    UNIQUE: [
      [ATT, 7.1429],
      [IED_30, 7.1429],
    ],
    LEGENDARY: [
      [ATT, 6.4516],
      [IED_35, 6.4516],
      [IED_40, 3.2258],
    ],
  }),
  
  SECONDARY: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.7544],
    ],
    EPIC: [
      [ATT, 2.8571],
    ],
    UNIQUE: [
      [ATT, 4.7619],
      [IED_30, 4.7619],
      [BOSS_30, 4.7619],
    ],
    LEGENDARY: [
      [ATT, 4.1667],
      [IED_35, 4.1667],
      [IED_40, 2.0833],
      [BOSS_35, 8.3333],
      [BOSS_40, 2.0833],
    ],
  }),
  
  FORCE_SHIELD_SOUL_RING: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.9608],
    ],
    EPIC: [
      [ATT, 3.4483],
    ],
    UNIQUE: [
      [ATT, 4.7619],
      [IED_30, 4.7619],
      [BOSS_30, 4.7619],
    ],
    LEGENDARY: [
      [ATT, 4.1667],
      [IED_35, 4.1667],
      [IED_40, 2.0833],
      [BOSS_35, 8.3333],
      [BOSS_40, 2.0833],
    ],
  }),
  
  HAT: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 7.4074],
      [HP, 11.1111],
      [ALLSTAT, 3.7037],
    ],
    UNIQUE: [
      [MAINSTAT, 6.8966],
      [HP, 10.3448],
      [ALLSTAT, 3.4483],
    ],
    LEGENDARY: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
      [ALLSTAT, 5.5556],
      [COOLDOWN_1, 8.3333],
      [COOLDOWN_2, 5.5556],
    ],
  }),
  
  TOP_OVERALL: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 6.6667],
      [HP, 10.0],
      [ALLSTAT, 3.3333],
      [INVIN, 10.0],
    ],
    UNIQUE: [
      [MAINSTAT, 6.0606],
      [HP, 9.0909],
      [ALLSTAT, 3.0303],
      [INVIN, 9.0909],
    ],
    LEGENDARY: [
      [MAINSTAT, 5.8824],
      [HP, 8.8235],
      [ALLSTAT, 5.8824],
      [INVIN, 8.8235],
    ],
  }),
  
  BOTTOM: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 7.4074],
      [HP, 11.1111],
      [ALLSTAT, 3.7037],
    ],
    UNIQUE: [
      [MAINSTAT, 6.8966],
      [HP, 10.3448],
      [ALLSTAT, 3.4483],
    ],
    LEGENDARY: [
      [MAINSTAT, 5.8824],
      [HP, 8.8235],
      [ALLSTAT, 5.8824],
    ],
  }),
  
  SHOE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 4.7619],
      [HP, 7.1429],
    ],
    EPIC: [
      [MAINSTAT, 7.4074],
      [HP, 11.1111],
      [ALLSTAT, 3.7037],
    ],
    UNIQUE: [
      [MAINSTAT, 6.8966],
      [HP, 10.3448],
      [ALLSTAT, 3.4483],
    ],
    LEGENDARY: [
      [MAINSTAT, 6.4516],
      [HP, 9.6774],
      [ALLSTAT, 6.4516],
    ],
  }),
  
  GLOVE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 6.0606],
      [HP, 9.0909],
      [ALLSTAT, 3.0303],
    ],
    UNIQUE: [
      [MAINSTAT, 5.7143],
      [HP, 8.5714],
      [ALLSTAT, 2.8571],
      [DECENT_SHARP_EYES, 5.7143],
    ],
    LEGENDARY: [
      [MAINSTAT, 4.5455],
      [HP, 6.8182],
      [CRITDMG, 9.0909],
      [ALLSTAT, 4.5455],
      [DECENT_SPEED_INFUSION, 6.8182],
    ],
  }),
  
  CAPE_BELT_SHOULDER: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 7.4074],
      [HP, 11.1111],
      [ALLSTAT, 3.7037],
    ],
    UNIQUE: [
      [MAINSTAT, 7.4074],
      [HP, 11.1111],
      [ALLSTAT, 3.7037],
    ],
    LEGENDARY: [
      [MAINSTAT, 7.1429],
      [HP, 10.7143],
      [ALLSTAT, 7.1429],
    ],
  }),
  
  FACE_EYE_RING_EARRING_PENDANT: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 4.7619],
      [HP, 7.1429],
    ],
    EPIC: [
      [MAINSTAT, 11.1111],
      [HP, 16.6667],
      [ALLSTAT, 5.5556],
    ],
    UNIQUE: [
      [MAINSTAT, 9.5238],
      [HP, 14.2857],
      [ALLSTAT, 4.7619],
    ],
    LEGENDARY: [
      [MAINSTAT, 5.8824],
      [HP, 8.8235],
      [ALLSTAT, 5.8824],
      [MESO, 8.8235],
      [DROP, 8.8235],
    ],
  }),
  
  HEART_BADGE: percent({
    COMMON: [],
    RARE: [
      [MAINSTAT, 5.5556],
      [HP, 8.3333],
    ],
    EPIC: [
      [MAINSTAT, 11.1111],
      [HP, 16.6667],
      [ALLSTAT, 5.5556],
    ],
    UNIQUE: [
      [MAINSTAT, 9.5238],
      [HP, 14.2857],
      [ALLSTAT, 4.7619],
    ],
    LEGENDARY: [
      [MAINSTAT, 9.0909],
      [HP, 13.6364],
      [ALLSTAT, 9.0909],
    ],
  }),
  
}

# bonus/additional potential
bonus = {
  WEAPON: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.9608],
    ],
    EPIC: [
      [ATT, 5.8824],
    ],
    UNIQUE: [
      [ATT, 4.6512],
    ],
    LEGENDARY: [
      [ATT, 5.1282],
    ],
  }),
  
  EMBLEM: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.9608],
    ],
    EPIC: [
      [ATT, 5.8824],
    ],
    UNIQUE: [
      [ATT, 4.7619],
    ],
    LEGENDARY: [
      [ATT, 5.2632],
    ],
  }),
  
  SECONDARY: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.9608],
    ],
    EPIC: [
      [ATT, 5.8824],
    ],
    UNIQUE: [
      [ATT, 4.6512],
    ],
    LEGENDARY: [
      [ATT, 4.878],
    ],
  }),
  
  FORCE_SHIELD_SOUL_RING: percent({
    COMMON: [],
    RARE: [
      [ATT, 1.9608],
    ],
    EPIC: [
      [ATT, 5.8824],
    ],
    UNIQUE: [
      [ATT, 4.6512],
    ],
    LEGENDARY: [
      [ATT, 4.878],
    ],
  }),
  
  HAT: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.0303],
      [MAINSTAT, 3.0303],
      [HP, 4.5455],
      [CRITDMG, 3.0303],
      [ALLSTAT, 3.0303],
      [COOLDOWN_1, 4.5455],
      [MESO, 4.5455],
      [DROP, 4.5455],
    ],
  }),
  
  TOP_OVERALL: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.1746],
      [MAINSTAT, 3.1746],
      [HP, 4.7619],
      [CRITDMG, 3.1746],
      [ALLSTAT, 3.1746],
      [MESO, 4.7619],
      [DROP, 4.7619],
    ],
  }),
  
  BOTTOM: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.1746],
      [MAINSTAT, 3.1746],
      [HP, 4.7619],
      [CRITDMG, 3.1746],
      [ALLSTAT, 3.1746],
      [MESO, 4.7619],
      [DROP, 4.7619],
    ],
  }),
  
  SHOE: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.1746],
      [MAINSTAT, 3.1746],
      [HP, 4.7619],
      [CRITDMG, 3.1746],
      [ALLSTAT, 3.1746],
      [MESO, 4.7619],
      [DROP, 4.7619],
    ],
  }),
  
  GLOVE: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.0769],
      [MAINSTAT, 3.0769],
      [HP, 4.6154],
      [CRITDMG, 3.0769],
      [ALLSTAT, 3.0769],
      [MESO, 4.6154],
      [DROP, 4.6154],
    ],
  }),
  
  CAPE_BELT_SHOULDER: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.1746],
      [MAINSTAT, 3.1746],
      [HP, 4.7619],
      [CRITDMG, 3.1746],
      [ALLSTAT, 3.1746],
      [MESO, 4.7619],
      [DROP, 4.7619],
    ],
  }),
  
  FACE_EYE_RING_EARRING_PENDANT: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.125],
      [MAINSTAT, 3.125],
      [HP, 4.6875],
      [ALLSTAT, 3.125],
      [MESO, 4.6875],
      [DROP, 4.6875],
    ],
  }),
  
  HEART_BADGE: percent({
    COMMON: [],
    RARE: [
      [FLAT_ATT, 4.2553],
      [MAINSTAT, 4.2553],
      [HP, 4.2553],
    ],
    EPIC: [
      [FLAT_ATT, 4.0],
      [MAINSTAT, 4.0],
      [HP, 6.0],
      [ALLSTAT, 4.0],
    ],
    UNIQUE: [
      [FLAT_ATT, 3.6364],
      [MAINSTAT, 3.6364],
      [HP, 5.4545],
      [ALLSTAT, 3.6364],
    ],
    LEGENDARY: [
      [FLAT_ATT, 3.2787],
      [MAINSTAT, 3.2787],
      [HP, 4.918],
      [ALLSTAT, 3.2787],
      [MESO, 4.918],
      [DROP, 4.918],
    ],
  }),
  
}
