def find_line_values(cube, category, region):
  MAXLVL = 300
  HIGHLVL_KMS = 250

  has_gms_lines = (region & HAS_GMS_LINES) != 0
  highlvl = 151 if has_gms_lines else HIGHLVL_KMS
  lowlvlmax = highlvl - 1

  minlvl = lambda minlvl, amt: [ (minlvl - 1, 0), (MAXLVL, amt) ]

  def addtier(values, amount, minlv=highlvl):
    _, lastamt = values[-1]
    return values[:-1] + [(minlv - 1, lastamt), (MAXLVL, amount)]

  mpot_4 = [
    (30, 1),
    (70, 2),
    (lowlvlmax, 3),
    (MAXLVL, 4),
  ]

  mpot_7 = [
    (30, 2),
    (70, 4),
    (lowlvlmax, 6),
    (MAXLVL, 7),
  ]

  mpot_8 = [
    (49, 0),
    (60, 5),
    (80, 6),
    (MAXLVL, 8),
  ]

  mpot_9 = [
    (30, 3),
    (70, 6),
    (MAXLVL, 9),
  ]

  mpot_10_kms = addtier(mpot_9, 10, HIGHLVL_KMS)
  mpot_10 = addtier(mpot_9, 10) if has_gms_lines else mpot_10_kms

  mpot_12 = [
    (30, 6),
    (70, 9),
    (150, 12),
  ]

  mpot_13_kms = addtier(mpot_12, 13, HIGHLVL_KMS)
  mpot_13 = addtier(mpot_12, 13) if has_gms_lines else mpot_13_kms

  mpot_20 = [
    (30, 10),
    (70, 15),
    (MAXLVL, 20),
  ]

  flat_mainstat_13 = [
    (20, 2),
    (40, 4),
    (50, 6),
    (70, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_hp_125 = [(x, x) for x in range(10, 120, 10)] + [
    (lowlvlmax, 120),
    (MAXLVL, 125),
  ]

  flat_att_13 = [
    (20, 2),
    (40, 4),
    (60, 6),
    (80, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_allstat_6 = [(x, x//20) for x in range(20, 100, 20)] + [
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  flat_mainstat_6 = [
    (20, 1),
    (40, 2),
    (50, 3),
    (70, 4),
    (90, 5),
    (MAXLVL, 6),
  ]

  flat_hp_60 = [(x, x//2) for x in range(10, 120, 10)] + [(MAXLVL, 60)]

  flat_att_6 = [
    (20, 1),
    (40, 2),
    (60, 3),
    (80, 4),
    (90, 5),
    (MAXLVL, 6),
  ]

  hp_recovery_30 = [
    (30, 10),
    (70, 20),
    (MAXLVL, 30),
  ]

  hp_recovery_40 = [
    (30, 20),
    (70, 30),
    (MAXLVL, 40),
  ]

  values = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_HP_A: flat_hp_60,
      FLAT_ATT_A: flat_att_6,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_13,
      FLAT_HP_A: flat_hp_125,
      FLAT_ATT_A: flat_att_13,
      MAINSTAT_A: mpot_4,
      HP_A: mpot_4,
      FLAT_ALLSTAT_A: flat_allstat_6,
      ATT_A: mpot_4,
      DAMAGE_A: mpot_4,
      IED_C: minlvl(30, 15),
    },

    EPIC: {
      ANY: 1,
      MAINSTAT_A: mpot_7,
      ALLSTAT_A: mpot_4,
      HP_A: mpot_7,
      INVIN: 1,
      ATT_A: mpot_7,
      DAMAGE_A: mpot_7,
      IED_C: minlvl(50, 15),
    },

    UNIQUE: {
      ANY: 1,
      BOSS_C: minlvl(100, 30),
      IED_C: minlvl(50, 30),
      ATT_A: mpot_10,
      DAMAGE_A: mpot_10,
      MAINSTAT_A: mpot_10,
      ALLSTAT_A: mpot_7,
      HP_A: mpot_10_kms,
      INVIN: 2,
      DECENT_SHARP_EYES: minlvl(120, 1),
      MAINSTAT_PER_10_LVLS: minlvl(30, 1),
      HP_ITEMS_AND_SKILLS_A: hp_recovery_30,
    },

    LEGENDARY: {
      ANY: 1,
      BOSS_C: minlvl(50, 30),
      BOSS_B: minlvl(100, 35),
      BOSS_A: minlvl(100, 40),
      IED_B: minlvl(50, 35),
      IED_A: minlvl(100, 40),
      ATT_A: mpot_13,
      DAMAGE_A: mpot_13,
      MAINSTAT_A: mpot_13,
      ALLSTAT_A: mpot_10,
      HP_A: mpot_13_kms,
      COOLDOWN_2: minlvl(120, 2),
      COOLDOWN_1: minlvl(70, 1),
      CRITDMG_A: mpot_8,
      MESO_A: mpot_20,
      DROP_A: mpot_20,
      INVIN: 3,
      DECENT_SPEED_INFUSION: minlvl(120, 1),
      DECENT_COMBAT_ORDERS: minlvl(70, 1),
      ATT_PER_10_LVLS: minlvl(30, 1),
      AUTOSTEAL_A: 7,
      AUTOSTEAL_B: 5,
      AUTOSTEAL_C: 3,
      HP_ITEMS_AND_SKILLS_A: hp_recovery_40,
    },
  }

  flat_att_3 = [
    (50, 1),
    (100, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_11 = [
    (20, 2),
    (50, 4),
    (70, 6),
    (90, 8),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  flat_att_11 = [
    (20, 1),
    (40, 2),
    (60, 4),
    (80, 6),
    (90, 8),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  flat_hp_125 = [
    (20, 10),
    (50, 15),
    (90, 50),
    (lowlvlmax, 100),
    (MAXLVL, 125),
  ]

  mainstat_3 = [
    (90, 1),
    (lowlvlmax, 2),
    (MAXLVL, 3),
  ]

  flat_allstat_3 = [
    (50, 1),
    (90, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_15 = [
    (20, 4),
    (40, 5),
    (50, 8),
    (70, 10),
    (90, 12),
    (lowlvlmax, 14),
    (MAXLVL, 15),
  ]

  flat_att_12 = [
    (20, 4),
    (50, 6),
    (90, 8),
    (lowlvlmax, 11),
    (MAXLVL, 12),
  ]

  flat_hp_195 = [(x, int(x*1.5)) for x in range(10, 120, 10)] + [
    (lowlvlmax, 180),
  ]

  if has_gms_lines:
    flat_hp_195 += [(HIGHLVL_KMS - 1, 185)]

  flat_hp_195 += [(MAXLVL, 195)]

  mainstat_5 = [
    (20, 1),
    (50, 2),
    (90, 3),
    (lowlvlmax, 4),
    (MAXLVL, 4),
  ]

  hp_6 = mainstat_5[:3] + [
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  allstat_3 = [
    (90, 1),
    (lowlvlmax, 2),
    (MAXLVL, 3),
  ]

  flat_mainstat_17 = [
    (20, 8),
    (50, 10),
    (70, 12),
    (90, 14),
    (lowlvlmax, 16),
    (MAXLVL, 17),
  ]

  flat_att_13 = [
    (20, 6),
    (50, 8),
    (90, 10),
    (lowlvlmax, 12),
    (MAXLVL, 13),
  ]

  flat_hp_250 = [(x, x*2) for x in range(10, 120, 10)] + [
    (lowlvlmax, 240),
    (MAXLVL, 250),
  ]

  mainstat_6 = [
    (20, 2),
    (50, 3),
    (90, 4),
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  hp_8 = mainstat_6[:2] + [
    (90, 5),
    (lowlvlmax, 7),
    (MAXLVL, 8),
  ]

  allstat_5 = [
    (20, 1),
    (50, 2),
    (90, 3),
    (lowlvlmax, 4),
    (MAXLVL, 5),
  ]

  flat_mainstat_19 = [
    (20, 8),
    (40, 10),
    (50, 12),
    (70, 14),
    (90, 16),
    (lowlvlmax, 18),
    (MAXLVL, 19),
  ]

  flat_att_15 = [
    (20, 8),
    (50, 10),
    (90, 12),
    (lowlvlmax, 14),
    (MAXLVL, 15),
  ]

  flat_hp_310 = [(x, int(x*2.5)) for x in range(10, 120, 10)] + [
    (lowlvlmax, 300),
    (MAXLVL, 310),
  ]

  mainstat_8 = [
    (20, 3),
    (50, 4),
    (90, 5),
    (lowlvlmax, 7),
    (MAXLVL, 8),
  ]

  hp_11 = [
    (20, 3),
    (50, 5),
    (90, 7),
    (lowlvlmax, 10),
    (MAXLVL, 11),
  ]

  allstat_6 = [
    (20, 2),
    (50, 3),
    (90, 4),
    (lowlvlmax, 5),
    (MAXLVL, 6),
  ]

  hp_recovery_20_bonus = [
    (20, 5),
    (50, 10),
    (90, 15),
    (MAXLVL, 20),
  ]

  hp_recovery_30_bonus = [
    (20, 10),
    (50, 15),
    (90, 20),
    (MAXLVL, 30),
  ]

  values_bonus = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_ATT_A: flat_att_3,
      FLAT_HP_A: flat_hp_60,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_11,
      FLAT_ATT_A: flat_att_11,
      FLAT_HP_A: flat_hp_125,
      MAINSTAT_A: mainstat_3,
      HP_A: mainstat_3,
      FLAT_ALLSTAT_A: flat_allstat_3,
    },

    EPIC: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_15,
      FLAT_ATT_A: flat_att_12,
      FLAT_HP_A: flat_hp_195,
      MAINSTAT_A: mainstat_5,
      HP_A: hp_6,
      ALLSTAT_A: allstat_3,
    },

    UNIQUE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_17,
      FLAT_ATT_A: flat_att_13,
      FLAT_HP_A: flat_hp_250,
      MAINSTAT_A: mainstat_6,
      HP_A: hp_8,
      ALLSTAT_A: allstat_5,
      MAINSTAT_PER_10_LVLS: 1,
      HP_ITEMS_AND_SKILLS_A: hp_recovery_20_bonus,
    },

    LEGENDARY: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_19,
      FLAT_ATT_A: flat_att_15,
      FLAT_HP_A: flat_hp_310,
      MAINSTAT_A: mainstat_8,
      HP_A: hp_11,
      CRITDMG_A: 1,
      ALLSTAT_A: allstat_6,
      MAINSTAT_PER_10_LVLS: 2,
      COOLDOWN_1: 1,
      MESO_A: 5,
      DROP_A: 5,
      HP_ITEMS_AND_SKILLS_A: hp_recovery_30_bonus,
    },
  }

  flat_hp_125_wse = [
    (20, 10),
    (50, 15),
    (90, 50),
    (lowlvlmax, 100),
    (MAXLVL, 125),
  ]

  values_bonus_wse = {
    COMMON: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_6,
      FLAT_ATT_A: flat_att_6,
      FLAT_HP_A: flat_hp_60,
    },

    RARE: {
      ANY: 1,
      FLAT_MAINSTAT_A: flat_mainstat_13,
      FLAT_ATT_A: flat_att_13,
      FLAT_HP_A: flat_hp_125_wse,
      MAINSTAT_A: mpot_4,
      ATT_A: mpot_4,
      DAMAGE_A: mpot_4,
      HP_A: mainstat_3,
      FLAT_ALLSTAT_A: flat_allstat_6,
    },

    EPIC: {
      ANY: 1,
      MAINSTAT_A: mpot_7,
      ATT_A: mpot_7,
      DAMAGE_A: mpot_7,
      HP_A: hp_6,
      ALLSTAT_A: mpot_4,
      IED_C: 3,
    },

    UNIQUE: {
      ANY: 1,
      MAINSTAT_A: mpot_10,
      ATT_A: mpot_10,
      DAMAGE_A: mpot_10,
      HP_A: hp_8,
      ALLSTAT_A: mpot_7,
      BOSS_C: 12,
      IED_C: 4,
      MAINSTAT_PER_10_LVLS: 1,
    },

    LEGENDARY: {
      ANY: 1,
      MAINSTAT_A: mpot_13,
      ATT_A: mpot_13,
      DAMAGE_A: mpot_13,
      HP_A: hp_11,
      ALLSTAT_A: mpot_10,
      CRITDMG_A: 1,
      BOSS_C: 18,
      IED_C: 5,
      MAINSTAT_PER_10_LVLS: 2,
      ATT_PER_10_LVLS: 1,
    },
  }

  if cube & BONUS:
    if category & (WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING | EMBLEM):
      return values_bonus_wse
    else:
      return values_bonus
  elif cube & (FAMILIAR | RED_FAM_CARD):
    from familiars import values as values_familiar
    return values_familiar
  return values
