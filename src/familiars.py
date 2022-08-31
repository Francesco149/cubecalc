# this file was automatically generated by /data/familiars/run.sh
# do not edit, edit the scraper
import sys
from datautils import percent
from common import *

familiars = {
  FAMILIAR: {
    FAMILIAR_STATS: percent({
      BASE: [
        [FLAT_ATT_A, 4.412], # ATT: +1
        [FLAT_HP_A, 5.882], # Max HP: +5
        [FLAT_MAINSTAT_A, 5.882], # Main Stat: +1
      ],
      COMMON: [
        [FLAT_ATT_A, 1.852], # ATT: +2
        [FLAT_ATT_B, 1.852], # ATT: +1
        [ATT_A, 0.37], # ATT: +1%
        [FLAT_ALLSTAT_A, 0.617], # All Stats: +1
        [IED_C, 0.617], # Attacks ignore 15% Monster DEF
        [SMALL_DROP, 1.235], # Increases Item Drop Rate by a small amount (30)
        [SMALL_MESO, 1.235], # Increases Meso Drop Rate by a small amount (30)
        [FLAT_HP_A, 2.469], # Max HP: +10
        [FLAT_HP_B, 2.469], # Max HP: +5
        [HP_A, 0.37], # Max HP: +1%
        [FLAT_MAINSTAT_A, 2.469], # Main Stat: +2
        [FLAT_MAINSTAT_B, 2.469], # Main Stat: +1
        [MAINSTAT_A, 0.37], # Main Stat: +1%
        [DAMAGE_A, 0.37], # Total Damage: +1%
      ],
      RARE: [
        [FLAT_ATT_A, 1.319], # ATT: +4
        [FLAT_ATT_B, 1.319], # ATT: +3
        [ATT_A, 0.264], # ATT: +2%
        [ALLSTAT_A, 0.176], # All Stats: +1%
        [IED_C, 0.264], # Attacks ignore 15% Monster DEF
        [DROP_A, 0.88], # Increases Item Drop Rate (50)
        [SMALL_DROP, 0.88], # Increases Item Drop Rate by a small amount (30)
        [SMALL_DROP_MESO, 0.88], # Increases Item and Meso Drop Rate by a small amount (20)
        [MESO_A, 0.88], # Increases Meso Drop Rate (50)
        [SMALL_MESO, 0.88], # Increases Meso Drop Rate by a small amount (30)
        [FLAT_HP_A, 1.759], # Max HP: +15
        [FLAT_HP_B, 1.759], # Max HP: +12
        [HP_A, 0.264], # Max HP: +2%
        [FLAT_MAINSTAT_A, 1.759], # Main Stat: +4
        [FLAT_MAINSTAT_B, 1.759], # Main Stat: +3
        [MAINSTAT_A, 0.264], # Main Stat: +2%
        [DAMAGE_A, 0.264], # Total Damage: +2%
        [INVIN, 0.44], # When hit, get +1 sec of invincibility
      ],
      EPIC: [
        [AUTOSTEAL_B, 0.367], # 1% chance to Auto Steal
        [AUTOSTEAL_A, 0.367], # 2% chance to Auto Steal
        [FLAT_ATT_A, 1.101], # ATT: +6
        [FLAT_ATT_B, 1.101], # ATT: +5
        [ATT_A, 0.22], # ATT: +3%
        [ALLSTAT_A, 0.147], # All Stats: +2%
        [IED_A, 0.22], # Attacks ignore 30% Monster DEF
        [IED_C, 0.22], # Attacks ignore 20% Monster DEF
        [BOSS_C, 0.147], # Damage to Bosses: +20%
        [BOSS_A, 0.147], # Damage to Bosses: +30%
        [DROP_A, 0.734], # Increases Item Drop Rate (60)
        [LARGE_DROP, 0.734], # Increases Item Drop Rate by a large amount (100)
        [NORMAL_DROP_MESO, 0.734], # Increases Item and Meso Drop Rate (40)
        [SMALL_DROP_MESO, 0.734], # Increases Item and Meso Drop Rate by a small amount (25)
        [MESO_A, 0.734], # Increases Meso Drop Rate (60)
        [LARGE_MESO, 0.734], # Increases Meso Drop Rate by a large amount (100)
        [FLAT_HP_A, 1.468], # Max HP: +20
        [FLAT_HP_B, 1.468], # Max HP: +18
        [HP_A, 0.22], # Max HP: +3%
        [FLAT_MAINSTAT_A, 1.468], # Main Stat: +6
        [FLAT_MAINSTAT_B, 1.468], # Main Stat: +5
        [MAINSTAT_A, 0.22], # Main Stat: +3%
        [DAMAGE_A, 0.22], # Total Damage: +3%
        [INVIN, 0.367], # When hit, get +2 sec of invincibility
      ],
      UNIQUE: [
        [AUTOSTEAL_E, 0.365], # 3% chance to Auto Steal
        [AUTOSTEAL_C, 0.365], # 5% chance to Auto Steal
        [AUTOSTEAL_A, 0.365], # 7% chance to Auto Steal
        [AUTOSTEAL_D, 0.365], # 4% chance to Auto Steal
        [AUTOSTEAL_B, 0.365], # 6% chance to Auto Steal
        [FLAT_ATT_A, 1.095], # ATT: +8
        [FLAT_ATT_B, 1.095], # ATT: +7
        [ATT_A, 0.219], # ATT: +6%
        [ATT_B, 0.219], # ATT: +5%
        [FLAT_ALLSTAT_A, 0.365], # All Stats: +4
        [ALLSTAT_A, 0.146], # All Stats: +3%
        [ALLSTAT_B, 0.146], # All Stats: +2%
        [IED_B, 0.219], # Attacks ignore 35% Monster DEF
        [IED_A, 0.219], # Attacks ignore 40% Monster DEF
        [IED_C, 0.219], # Attacks ignore 30% Monster DEF
        [BOSS_C, 0.146], # Boss Damage: +30%
        [BOSS_B, 0.146], # Boss Damage: +35%
        [BOSS_A, 0.146], # Boss Damage: +40%
        [CRITDMG_A, 0.438], # Critical Damage: +3%
        [CRITDMG_B, 0.438], # Critical Damage: +2%
        [LARGE_DROP_MESO, 0.73], # Increases Item and Meso Drop Rate by a large amount (50)
        [FLAT_ALLSTAT_C, 0.73], # Increases Main Stat, INT, DEX, and LUK of players on the same map (2)
        [FLAT_DEX_ONLY, 1.46], # Increases Speed, Jump, DEX, and Defense by a small amount (1)
        [FLAT_ALLSTAT_B, 0.73], # Increases your party's Main Stat, INT, DEX, and LUK (3)
        [SMALL_DROP, 0.365], # Item Acquisition Rate: +10%
        [FLAT_HP_B, 1.46], # Max HP: +22
        [FLAT_HP_A, 1.46], # Max HP: +25
        [HP_A, 0.219], # Max HP: +6%
        [HP_B, 0.219], # Max HP: +5%
        [FLAT_MESO, 0.365], # Mesos Obtained: +10
        [FLAT_MAINSTAT_A, 1.46], # Main Stat: +8
        [FLAT_MAINSTAT_B, 1.46], # Main Stat: +7
        [MAINSTAT_A, 0.219], # Main Stat: +6%
        [MAINSTAT_B, 0.219], # Main Stat: +5%
        [DAMAGE_A, 0.219], # Total Damage: +6%
        [DAMAGE_B, 0.219], # Total Damage: +5%
        [INVIN, 0.365], # When hit, gain +3 sec of invincibility
      ],
      LEGENDARY: [
        [AUTOSTEAL_C, 2.427], # 4% chance to Auto Steal
        [AUTOSTEAL_B, 2.427], # 6% chance to Auto Steal
        [AUTOSTEAL_A, 2.427], # 8% chance to Auto Steal
        [ATT_A, 1.456], # ATT: +9%
        [ALLSTAT_A, 0.971], # All Stats: +5%
        [IED_B, 1.456], # Attacks ignore 45% Monster DEF
        [IED_A, 1.456], # Attacks ignore 50% Monster DEF
        [BOSS_C, 0.971], # Boss Damage: +40%
        [BOSS_B, 0.971], # Boss Damage: +45%
        [BOSS_A, 0.971], # Boss Damage: +50%
        [CRITDMG_A, 2.912], # Critical Damage: +6%
        [SMALL_DROP, 2.427], # Item Acquisition Rate: +12%
        [HP_A, 1.456], # Max HP: +9%
        [FLAT_MESO, 2.427], # Mesos Obtained: +12
        [MAINSTAT_A, 1.456], # Main Stat: +9%
        [DAMAGE_A, 1.456], # Total Damage: +9%
        [INVIN, 2.427], # When hit, gain +4 sec of invincibility
      ],
    }),
  },
}

values = {
  BASE: {
    ANY: 1,
    FLAT_ATT_A: 1,
    FLAT_HP_A: 5,
    FLAT_MAINSTAT_A: 1,
  },
  COMMON: {
    ANY: 1,
    FLAT_ATT_A: 2,
    FLAT_ATT_B: 1,
    ATT_A: 1,
    FLAT_ALLSTAT_A: 1,
    IED_C: 15,
    SMALL_DROP: 30,
    SMALL_MESO: 30,
    FLAT_HP_A: 10,
    FLAT_HP_B: 5,
    HP_A: 1,
    FLAT_MAINSTAT_A: 2,
    FLAT_MAINSTAT_B: 1,
    MAINSTAT_A: 1,
    DAMAGE_A: 1,
  },
  RARE: {
    ANY: 1,
    FLAT_ATT_A: 4,
    FLAT_ATT_B: 3,
    ATT_A: 2,
    ALLSTAT_A: 1,
    IED_C: 15,
    DROP_A: 50,
    SMALL_DROP: 30,
    SMALL_DROP_MESO: 20,
    MESO_A: 50,
    SMALL_MESO: 30,
    FLAT_HP_A: 15,
    FLAT_HP_B: 12,
    HP_A: 2,
    FLAT_MAINSTAT_A: 4,
    FLAT_MAINSTAT_B: 3,
    MAINSTAT_A: 2,
    DAMAGE_A: 2,
    INVIN: 1,
  },
  EPIC: {
    ANY: 1,
    AUTOSTEAL_B: 1,
    AUTOSTEAL_A: 2,
    FLAT_ATT_A: 6,
    FLAT_ATT_B: 5,
    ATT_A: 3,
    ALLSTAT_A: 2,
    IED_A: 30,
    IED_C: 20,
    BOSS_C: 20,
    BOSS_A: 30,
    DROP_A: 60,
    LARGE_DROP: 100,
    NORMAL_DROP_MESO: 40,
    SMALL_DROP_MESO: 25,
    MESO_A: 60,
    LARGE_MESO: 100,
    FLAT_HP_A: 20,
    FLAT_HP_B: 18,
    HP_A: 3,
    FLAT_MAINSTAT_A: 6,
    FLAT_MAINSTAT_B: 5,
    MAINSTAT_A: 3,
    DAMAGE_A: 3,
    INVIN: 2,
  },
  UNIQUE: {
    ANY: 1,
    AUTOSTEAL_E: 3,
    AUTOSTEAL_C: 5,
    AUTOSTEAL_A: 7,
    AUTOSTEAL_D: 4,
    AUTOSTEAL_B: 6,
    FLAT_ATT_A: 8,
    FLAT_ATT_B: 7,
    ATT_A: 6,
    ATT_B: 5,
    FLAT_ALLSTAT_A: 4,
    ALLSTAT_A: 3,
    ALLSTAT_B: 2,
    IED_B: 35,
    IED_A: 40,
    IED_C: 30,
    BOSS_C: 30,
    BOSS_B: 35,
    BOSS_A: 40,
    CRITDMG_A: 3,
    CRITDMG_B: 2,
    LARGE_DROP_MESO: 50,
    FLAT_ALLSTAT_C: 2,
    FLAT_DEX_ONLY: 1,
    FLAT_ALLSTAT_B: 3,
    SMALL_DROP: 10,
    FLAT_HP_B: 22,
    FLAT_HP_A: 25,
    HP_A: 6,
    HP_B: 5,
    FLAT_MESO: 10,
    FLAT_MAINSTAT_A: 8,
    FLAT_MAINSTAT_B: 7,
    MAINSTAT_A: 6,
    MAINSTAT_B: 5,
    DAMAGE_A: 6,
    DAMAGE_B: 5,
    INVIN: 3,
  },
  LEGENDARY: {
    ANY: 1,
    AUTOSTEAL_C: 4,
    AUTOSTEAL_B: 6,
    AUTOSTEAL_A: 8,
    ATT_A: 9,
    ALLSTAT_A: 5,
    IED_B: 45,
    IED_A: 50,
    BOSS_C: 40,
    BOSS_B: 45,
    BOSS_A: 50,
    CRITDMG_A: 6,
    SMALL_DROP: 12,
    HP_A: 9,
    FLAT_MESO: 12,
    MAINSTAT_A: 9,
    DAMAGE_A: 9,
    INVIN: 4,
  },
}

desc = {
  BASE: {
    FLAT_ATT_A: "ATT: +1",
    FLAT_HP_A: "Max HP: +5",
    FLAT_MAINSTAT_A: "Main Stat: +1",
  },
  COMMON: {
    FLAT_ATT_A: "ATT: +2",
    FLAT_ATT_B: "ATT: +1",
    ATT_A: "ATT: +1%",
    FLAT_ALLSTAT_A: "All Stats: +1",
    IED_C: "Attacks ignore 15% Monster DEF",
    SMALL_DROP: "Increases Item Drop Rate by a small amount (30)",
    SMALL_MESO: "Increases Meso Drop Rate by a small amount (30)",
    FLAT_HP_A: "Max HP: +10",
    FLAT_HP_B: "Max HP: +5",
    HP_A: "Max HP: +1%",
    FLAT_MAINSTAT_A: "Main Stat: +2",
    FLAT_MAINSTAT_B: "Main Stat: +1",
    MAINSTAT_A: "Main Stat: +1%",
    DAMAGE_A: "Total Damage: +1%",
  },
  RARE: {
    FLAT_ATT_A: "ATT: +4",
    FLAT_ATT_B: "ATT: +3",
    ATT_A: "ATT: +2%",
    ALLSTAT_A: "All Stats: +1%",
    IED_C: "Attacks ignore 15% Monster DEF",
    DROP_A: "Increases Item Drop Rate (50)",
    SMALL_DROP: "Increases Item Drop Rate by a small amount (30)",
    SMALL_DROP_MESO: "Increases Item and Meso Drop Rate by a small amount (20)",
    MESO_A: "Increases Meso Drop Rate (50)",
    SMALL_MESO: "Increases Meso Drop Rate by a small amount (30)",
    FLAT_HP_A: "Max HP: +15",
    FLAT_HP_B: "Max HP: +12",
    HP_A: "Max HP: +2%",
    FLAT_MAINSTAT_A: "Main Stat: +4",
    FLAT_MAINSTAT_B: "Main Stat: +3",
    MAINSTAT_A: "Main Stat: +2%",
    DAMAGE_A: "Total Damage: +2%",
    INVIN: "When hit, get +1 sec of invincibility",
  },
  EPIC: {
    AUTOSTEAL_B: "1% chance to Auto Steal",
    AUTOSTEAL_A: "2% chance to Auto Steal",
    FLAT_ATT_A: "ATT: +6",
    FLAT_ATT_B: "ATT: +5",
    ATT_A: "ATT: +3%",
    ALLSTAT_A: "All Stats: +2%",
    IED_A: "Attacks ignore 30% Monster DEF",
    IED_C: "Attacks ignore 20% Monster DEF",
    BOSS_C: "Damage to Bosses: +20%",
    BOSS_A: "Damage to Bosses: +30%",
    DROP_A: "Increases Item Drop Rate (60)",
    LARGE_DROP: "Increases Item Drop Rate by a large amount (100)",
    NORMAL_DROP_MESO: "Increases Item and Meso Drop Rate (40)",
    SMALL_DROP_MESO: "Increases Item and Meso Drop Rate by a small amount (25)",
    MESO_A: "Increases Meso Drop Rate (60)",
    LARGE_MESO: "Increases Meso Drop Rate by a large amount (100)",
    FLAT_HP_A: "Max HP: +20",
    FLAT_HP_B: "Max HP: +18",
    HP_A: "Max HP: +3%",
    FLAT_MAINSTAT_A: "Main Stat: +6",
    FLAT_MAINSTAT_B: "Main Stat: +5",
    MAINSTAT_A: "Main Stat: +3%",
    DAMAGE_A: "Total Damage: +3%",
    INVIN: "When hit, get +2 sec of invincibility",
  },
  UNIQUE: {
    AUTOSTEAL_E: "3% chance to Auto Steal",
    AUTOSTEAL_C: "5% chance to Auto Steal",
    AUTOSTEAL_A: "7% chance to Auto Steal",
    AUTOSTEAL_D: "4% chance to Auto Steal",
    AUTOSTEAL_B: "6% chance to Auto Steal",
    FLAT_ATT_A: "ATT: +8",
    FLAT_ATT_B: "ATT: +7",
    ATT_A: "ATT: +6%",
    ATT_B: "ATT: +5%",
    FLAT_ALLSTAT_A: "All Stats: +4",
    ALLSTAT_A: "All Stats: +3%",
    ALLSTAT_B: "All Stats: +2%",
    IED_B: "Attacks ignore 35% Monster DEF",
    IED_A: "Attacks ignore 40% Monster DEF",
    IED_C: "Attacks ignore 30% Monster DEF",
    BOSS_C: "Boss Damage: +30%",
    BOSS_B: "Boss Damage: +35%",
    BOSS_A: "Boss Damage: +40%",
    CRITDMG_A: "Critical Damage: +3%",
    CRITDMG_B: "Critical Damage: +2%",
    LARGE_DROP_MESO: "Increases Item and Meso Drop Rate by a large amount (50)",
    FLAT_ALLSTAT_C: "Increases Main Stat, INT, DEX, and LUK of players on the same map (2)",
    FLAT_DEX_ONLY: "Increases Speed, Jump, DEX, and Defense by a small amount (1)",
    FLAT_ALLSTAT_B: "Increases your party's Main Stat, INT, DEX, and LUK (3)",
    SMALL_DROP: "Item Acquisition Rate: +10%",
    FLAT_HP_B: "Max HP: +22",
    FLAT_HP_A: "Max HP: +25",
    HP_A: "Max HP: +6%",
    HP_B: "Max HP: +5%",
    FLAT_MESO: "Mesos Obtained: +10",
    FLAT_MAINSTAT_A: "Main Stat: +8",
    FLAT_MAINSTAT_B: "Main Stat: +7",
    MAINSTAT_A: "Main Stat: +6%",
    MAINSTAT_B: "Main Stat: +5%",
    DAMAGE_A: "Total Damage: +6%",
    DAMAGE_B: "Total Damage: +5%",
    INVIN: "When hit, gain +3 sec of invincibility",
  },
  LEGENDARY: {
    AUTOSTEAL_C: "4% chance to Auto Steal",
    AUTOSTEAL_B: "6% chance to Auto Steal",
    AUTOSTEAL_A: "8% chance to Auto Steal",
    ATT_A: "ATT: +9%",
    ALLSTAT_A: "All Stats: +5%",
    IED_B: "Attacks ignore 45% Monster DEF",
    IED_A: "Attacks ignore 50% Monster DEF",
    BOSS_C: "Boss Damage: +40%",
    BOSS_B: "Boss Damage: +45%",
    BOSS_A: "Boss Damage: +50%",
    CRITDMG_A: "Critical Damage: +6%",
    SMALL_DROP: "Item Acquisition Rate: +12%",
    HP_A: "Max HP: +9%",
    FLAT_MESO: "Mesos Obtained: +12",
    MAINSTAT_A: "Main Stat: +9%",
    DAMAGE_A: "Total Damage: +9%",
    INVIN: "When hit, gain +4 sec of invincibility",
  },
}

red_card_estimate = {
  RED_FAM_CARD: {
    FAMILIAR_STATS: percent({
      BASE: [],
      COMMON: [],
      RARE: [],
      EPIC: [],
      UNIQUE: [
        [LARGE_DROP_MESO, 54 / 2903 * 100],
        [FLAT_ALLSTAT_B, 53 / 2903 * 100],
        [FLAT_DEX_ONLY, 49 / 2903 * 100],
        [FLAT_HP_A, 37 / 2903 * 100],
        [FLAT_ATT_B, 35 / 2903 * 100],
        [FLAT_MAINSTAT_A, 33 / 2903 * 100],
        [INVIN, 33 / 2903 * 100],
        [FLAT_ATT_A, 28 / 2903 * 100],
        [FLAT_ALLSTAT_A, 28 / 2903 * 100],
        [AUTOSTEAL_D, 28 / 2903 * 100],
        [FLAT_HP_B, 27 / 2903 * 100],
        [AUTOSTEAL_A, 27 / 2903 * 100],
        [AUTOSTEAL_E, 26 / 2903 * 100],
        [AUTOSTEAL_B, 25 / 2903 * 100],
        [HP_B, 24 / 2903 * 100],
        [CRITDMG_B, 22 / 2903 * 100],
        [AUTOSTEAL_C, 21 / 2903 * 100],
        [FLAT_MAINSTAT_B, 21 / 2903 * 100],
        [MAINSTAT_B, 18 / 2903 * 100],
        [HP_A, 18 / 2903 * 100],
        [FLAT_ALLSTAT_C, 18 / 2903 * 100],
        [MAINSTAT_A, 17 / 2903 * 100],
        [CRITDMG_A, 17 / 2903 * 100],
        [FLAT_MESO, 16 / 2903 * 100],
        [ATT_A, 16 / 2903 * 100],
        [ALLSTAT_B, 11 / 2903 * 100],
        [ALLSTAT_A, 10 / 2903 * 100],
        [DAMAGE_A, 9 / 2903 * 100],
        [ATT_B, 8 / 2903 * 100],
        [IED_B, 7 / 2903 * 100],
        [BOSS_C, 7 / 2903 * 100],
        [SMALL_DROP, 6 / 2903 * 100],
        [BOSS_B, 6 / 2903 * 100],
        [IED_C, 6 / 2903 * 100],
        [DAMAGE_B, 6 / 2903 * 100],
        [IED_A, 3 / 2903 * 100],
        [BOSS_A, 1 / 2903 * 100],
      ],
      LEGENDARY: [
        [AUTOSTEAL_A, 104 / 2903 * 100],
        [INVIN, 88 / 2903 * 100],
        [AUTOSTEAL_C, 88 / 2903 * 100],
        [AUTOSTEAL_B, 83 / 2903 * 100],
        [MAINSTAT_A, 72 / 2903 * 100],
        [HP_A, 68 / 2903 * 100],
        [ATT_A, 37 / 2903 * 100],
        [CRITDMG_A, 34 / 2903 * 100],
        [IED_B, 23 / 2903 * 100],
        [FLAT_MESO, 23 / 2903 * 100],
        [BOSS_A, 22 / 2903 * 100],
        [DAMAGE_A, 20 / 2903 * 100],
        [BOSS_C, 18 / 2903 * 100],
        [SMALL_DROP, 17 / 2903 * 100],
        [BOSS_B, 16 / 2903 * 100],
        [IED_A, 15 / 2903 * 100],
        [ALLSTAT_A, 12 / 2903 * 100],
      ],
    }),
  },
}
