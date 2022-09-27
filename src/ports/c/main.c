#include "cubecalc.c"
#include "generated.c"

#include <stdio.h>
#include <math.h>

typedef struct _ComboData {
  char const* description;
  Want const* wantBuf;
} ComboData;

typedef struct _ComboGroup {
  int category;
  int const* cubes;
  int tier;
  int level;
  int region;
  ComboData const* combos;
} ComboGroup;

#define Combo(desc, want) \
  (ComboData){ .description = (desc), .wantBuf = (want) }

#define ComboGroup(category_, cubes_, tier_, combos_) \
  (ComboGroup){ \
    .category = (category_), \
    .cubes = (cubes_), \
    .tier = (tier_), \
    .level = 150, \
    .region = GMS, \
    .combos = (combos_), \
  }

#define WIDTH 80

static
void PrintHdr(char* fmt, ...) {
  va_list va;
  char buf[WIDTH + 1];
  va_start(va, fmt);
  size_t n = vsnprintf(0, 0, fmt, va);
  va_end(va);
  size_t off = (WIDTH - n) / 2;
  if (off <= WIDTH) {
    va_start(va, fmt);
    vsnprintf(buf + off, WIDTH + 1 - off, fmt, va);
    va_end(va);
    RangeBefore(off, i) {
      buf[i] = '=';
    }
    ArrayEachiRange(buf, off + n, -1, i) {
      buf[i] = '=';
    }
    buf[WIDTH] = 0;
    puts(buf);
  } else {
    va_start(va, fmt);
    vprintf(fmt, va);
    va_end(va);
    puts("");
  }
}

int main() {
  CubeGlobalInit();

  PrintHdr(" ! DISCLAIMER ! ");
  printf("\n%s", disclaimer);

#define WantBoss(x) \
  static const BufStaticHdr(Want, want##x##Boss, \
    WantStat(BOSS, x), \
    WantOp(OR, -1), \
  )

  WantBoss(20);
  WantBoss(30);
  WantBoss(35);
  WantBoss(40);
  WantBoss(45);
  WantBoss(50);
  WantBoss(60);

#define WantIed(x) \
  static const BufStaticHdr(Want, want##x##Ied, \
    WantStat(IED, x), \
    WantOp(OR, -1), \
  )

  WantIed(15);
  WantIed(20);
  WantIed(30);
  WantIed(35);
  WantIed(40);
  WantIed(45);
  WantIed(50);
  WantIed(60);
  WantIed(70);

#define AnyNl1(name, x, a) \
  static const BufStaticHdr(Want, wantAny##x##l##name, \
    WantStat(a, 1), \
    WantStat(LINES, x), \
    WantOp(AND, -1), \
  )

#define AnyNl(name, x, a, b) \
  static const BufStaticHdr(Want, wantAny##x##l##name, \
    WantStat(a, 1), \
    WantStat(b, 1), \
    WantStat(LINES, x), \
    WantOp(AND, -1), \
  )

#define AnyNl3(name, x, a, b, c) \
  static const BufStaticHdr(Want, wantAny##x##l##name, \
    WantStat(a, 1), \
    WantStat(b, 1), \
    WantStat(c, 1), \
    WantStat(LINES, x), \
    WantOp(AND, -1), \
  )

  AnyNl(AttBoss, 2, ATT, BOSS_ONLY);
  AnyNl(AttBoss, 3, ATT, BOSS_ONLY);
  AnyNl(AttIed, 2, ATT, IED);
  AnyNl(AttIed, 3, ATT, IED);
  AnyNl3(AttBossIed, 2, ATT, BOSS_ONLY, IED);
  AnyNl3(AttBossIed, 3, ATT, BOSS_ONLY, IED);

#define WantAtt(n) \
  static const BufStaticHdr(Want, want##n##Att, \
    WantStat(ATT, n), \
    WantOp(AND, -1), \
  )

  WantAtt(6);
  WantAtt(9);
  WantAtt(12);
  WantAtt(15);
  WantAtt(18);
  WantAtt(21);
  WantAtt(30);
  WantAtt(33);

  static const BufStaticHdr(Want, want21AttAndBoss,
    WantStat(ATT, 21),
    WantStat(BOSS_ONLY, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want21AttAndIed,
    WantStat(ATT, 21),
    WantStat(IED, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want18AttAndBoss,
    WantStat(ATT, 18),
    WantStat(BOSS_ONLY, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want18AttAndIed,
    WantStat(ATT, 18),
    WantStat(IED, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want60IedAndAtt,
    WantStat(IED, 60),
    WantStat(ATT, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want60IedAndBoss,
    WantStat(IED, 60),
    WantStat(BOSS_ONLY, 1),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, wantAnyBoss,
    WantStat(BOSS_ONLY, 1),
    WantOp(AND, -1),
  );

#define CombosWsCommon \
    Combo("any 2l combo of att+boss", wantAny2lAttBoss.data), \
    Combo("any 2l combo of att+boss+ied", wantAny2lAttBossIed.data), \
    Combo("any 3l combo of att+boss", wantAny3lAttBoss.data), \
    Combo("any 3l combo of att+boss+ied", wantAny3lAttBossIed.data), \

#define CombosLegendaryAttCommon \
    Combo("18+ att", want18Att.data), \
    Combo("21+ att", want21Att.data), \
    Combo("30+ att", want30Att.data), \
    Combo("33+ att", want33Att.data), \

  static const BufStaticHdr(ComboData, combosWs,
    CombosWsCommon
    CombosLegendaryAttCommon
    Combo("21+ att and boss", want21AttAndBoss.data),
    Combo("21+ att and ied", want21AttAndIed.data),
    Combo("18+ att and boss", want18AttAndBoss.data),
    Combo("18+ att and ied", want18AttAndIed.data),
    Combo("60+ied", want60Ied.data),
    Combo("70+ied", want70Ied.data),
    Combo("60+ied and att", want60IedAndAtt.data),
    Combo("60+ied and boss", want60IedAndBoss.data),
  );

#define CombosWSEMasterCommon \
    Combo("9+ att", want9Att.data), \
    Combo("12+ att", want12Att.data), \
    Combo("15+ att", want15Att.data), \
    Combo("21+ att", want21Att.data), \

  static const BufStaticHdr(ComboData, combosWsMaster,
    CombosWsCommon
    CombosWSEMasterCommon
    Combo("any boss", wantAnyBoss.data),
  );

#define CombosECommon \
    Combo("any 2l combo of att+ied", wantAny2lAttIed.data), \
    Combo("any 3l combo of att+ied", wantAny3lAttIed.data), \

  static const BufStaticHdr(ComboData, combosE,
    CombosECommon
    CombosLegendaryAttCommon
    Combo("21+ att and ied", want21AttAndIed.data),
  );

  static const BufStaticHdr(ComboData, combosEMaster,
    CombosECommon
    CombosWSEMasterCommon
  );

  static const BufStaticHdr(ComboData, combosWSEOccult,
    Combo("6+ att", want6Att.data),
    Combo("9+ att", want9Att.data),
    Combo("12+ att", want12Att.data),
  );

  static const BufStaticHdr(ComboData, combosWSEBonus,
    CombosLegendaryAttCommon
  );


#define WantFAtt(x) \
  static const BufStaticHdr(Want, want##x##FAtt, \
    WantStat(FLAT_ATT, x),\
    WantOp(AND, -1), \
  )

  WantFAtt(10);
  WantFAtt(13);

#define DefWantStat(x) \
  static const BufStaticHdr(Want, want##x##Stat, \
    WantStat(STAT, x),\
    WantOp(AND, -1), \
  )

#define WantHP(x) \
  static const BufStaticHdr(Want, want##x##Hp, \
    WantStat(HP, x),\
    WantOp(AND, -1), \
  )

#define WantAllStat(x) \
  static const BufStaticHdr(Want, want##x##AllStat, \
    WantStat(ALLSTAT, x),\
    WantOp(AND, -1), \
  )

  DefWantStat(6);
  DefWantStat(9);
  DefWantStat(12);
  DefWantStat(15);

  DefWantStat(18);
  DefWantStat(21);
  DefWantStat(30);
  DefWantStat(33);

  WantHP(6);
  WantHP(9);
  WantHP(12);
  WantHP(15);

  WantHP(18);
  WantHP(21);
  WantHP(30);
  WantHP(33);

  WantAllStat(3);
  WantAllStat(6);
  WantAllStat(9);
  WantAllStat(12);
  WantAllStat(15);
  WantAllStat(21);

  static const BufStaticHdr(ComboData, combosBonusRare,
    Combo("10+ flat att", want10FAtt.data),
    Combo("13+ flat att", want13FAtt.data),
  );

  #define CombosStatLegendary \
    Combo("18+ stat", want18Stat.data), \
    Combo("21+ stat", want21Stat.data), \
    Combo("30+ stat", want30Stat.data), \
    Combo("33+ stat", want33Stat.data), \
    Combo("18+ hp", want18Hp.data), \
    Combo("21+ hp", want21Hp.data), \
    Combo("30+ hp", want30Hp.data), \
    Combo("33+ hp", want33Hp.data), \
    Combo("12+ all stat", want12AllStat.data), \
    Combo("15+ all stat", want15AllStat.data), \
    Combo("21+ all stat", want21AllStat.data),

  static const BufStaticHdr(ComboData, combosStat,
    CombosStatLegendary
  );


#define WantMeso(x) \
  static const BufStaticHdr(Want, want##x##Meso, \
    WantStat(MESO, x),\
    WantOp(AND, -1), \
  )

#define WantDrop(x) \
  static const BufStaticHdr(Want, want##x##Drop, \
    WantStat(DROP, x),\
    WantOp(AND, -1), \
  )

#define WantMesoDrop(x) \
  static const BufStaticHdr(Want, want##x##MesoDrop, \
    WantStat(MESO, x),\
    WantStat(DROP, x),\
    WantOp(AND, -1), \
  )

#define WantMesoOrDrop(x) \
  static const BufStaticHdr(Want, want##x##MesoOrDrop, \
    WantStat(MESO, x),\
    WantStat(DROP, x),\
    WantOp(OR, -1), \
  )

#define WantMesoOrDropWithStat(x, s) \
  static const BufStaticHdr(Want, want##x##MesoOrDropWith##s##Stat, \
    WantStat(MESO, x),\
    WantStat(DROP, x),\
    WantOp(OR, 2), \
    WantStat(STAT, s),\
    WantOp(AND, 2), \
  )

  WantMeso(20);
  WantMeso(25);
  WantMeso(30);
  WantMeso(40);
  WantMeso(50);
  WantMeso(70);
  WantDrop(20);
  WantDrop(25);
  WantDrop(30);
  WantDrop(40);
  WantDrop(50);
  WantDrop(70);
  WantDrop(100);
  WantMesoDrop(20);
  WantMesoDrop(25);
  WantMesoDrop(40);
  WantMesoDrop(50);
  WantMesoOrDrop(20);
  WantMesoOrDrop(40);
  WantMesoOrDropWithStat(20, 6);
  WantMesoOrDropWithStat(20, 9);
  WantMesoOrDropWithStat(20, 15);
  WantMesoOrDropWithStat(20, 18);
  WantMesoOrDropWithStat(20, 21);

  static const BufStaticHdr(ComboData, combosAccessory,
    CombosStatLegendary
    Combo("20+ meso or 20+ drop", want20MesoOrDrop.data),
    Combo("20+ meso", want20Meso.data),
    Combo("20+ drop", want20Drop.data),
    Combo("40 meso or 40 drop", want40MesoOrDrop.data),
    Combo("40 meso", want40Meso.data),
    Combo("40 drop", want40Drop.data),
    Combo("20+ meso and 20+ drop", want20MesoDrop.data),
    Combo("20+ meso or drop, with 6+ stat", want20MesoOrDropWith6Stat.data),
    Combo("20+ meso or drop, with 9+ stat", want20MesoOrDropWith9Stat.data),
    Combo("20+ meso or drop, with 15+ stat", want20MesoOrDropWith15Stat.data),
    Combo("20+ meso or drop, with 18+ stat", want20MesoOrDropWith18Stat.data),
    Combo("20+ meso or drop, with 21+ stat", want20MesoOrDropWith21Stat.data),
  );

#define WantCdAndStat(x, s) \
  static const BufStaticHdr(Want, want##x##CdAnd##s##Stat, \
    WantStat(COOLDOWN, x),\
    WantStat(STAT, s),\
    WantOp(AND, -1), \
  )

#define WantCd(x) \
  static const BufStaticHdr(Want, want##x##Cd, \
    WantStat(COOLDOWN, x),\
    WantOp(AND, -1), \
  )

  WantCd(1);
  WantCd(2);
  WantCd(3);
  WantCd(4);
  WantCd(5);
  WantCd(6);
  WantCdAndStat(2, 1);
  WantCdAndStat(2, 9);
  WantCdAndStat(2, 12);
  WantCdAndStat(2, 18);
  WantCdAndStat(3, 1);
  WantCdAndStat(4, 1);

  static const BufStaticHdr(ComboData, combosHat,
    CombosStatLegendary
    Combo("2+s cooldown", want2Cd.data),
    Combo("2+s cooldown and any stat", want2CdAnd1Stat.data),
    Combo("2+s cooldown and 9+ stat", want2CdAnd9Stat.data),
    Combo("2+s cooldown and 12+ stat", want2CdAnd12Stat.data),
    Combo("2+s cooldown and 18+ stat", want2CdAnd18Stat.data),
    Combo("3+s cooldown", want3Cd.data),
    Combo("3+s cooldown and any stat", want3CdAnd1Stat.data),
    Combo("4+s cooldown", want4Cd.data),
    Combo("4+s cooldown and any stat", want4CdAnd1Stat.data),
    Combo("5+s cooldown", want5Cd.data),
    Combo("6+s cooldown", want6Cd.data),
  );

#define CombosStatOccult \
    Combo("6+ stat", want6Stat.data), \
    Combo("9+ stat", want9Stat.data), \
    Combo("12+ stat", want12Stat.data), \
    Combo("3+ all stat", want3AllStat.data), \
    Combo("6+ all stat", want6AllStat.data), \
    Combo("6+ hp", want6Hp.data), \
    Combo("9+ hp", want9Hp.data), \
    Combo("12+ hp", want12Hp.data),

  static const BufStaticHdr(ComboData, combosStatOccult,
    CombosStatOccult
  );

  static const BufStaticHdr(ComboData, combosStatMaster,
    CombosStatOccult
    Combo("15+ stat", want15Stat.data),
    Combo("9+ all stat", want9AllStat.data),
    Combo("15+ hp", want15Hp.data),
  );

#define WantCritDmg(x) \
  static const BufStaticHdr(Want, want##x##CritDmg, \
    WantStat(CRITDMG, x),\
    WantOp(AND, -1), \
  )

#define WantCritDmgStat(x, s) \
  static const BufStaticHdr(Want, want##x##CritDmg##s##Stat, \
    WantStat(CRITDMG, x),\
    WantStat(STAT, s),\
    WantOp(AND, -1), \
  )

  WantCritDmg(8);
  WantCritDmgStat(8, 6);
  WantCritDmgStat(8, 9);
  WantCritDmgStat(8, 12);
  WantCritDmgStat(8, 18);
  WantCritDmgStat(8, 24);
  WantCritDmg(16);
  WantCritDmgStat(16, 6);
  WantCritDmgStat(16, 9);
  WantCritDmgStat(16, 12);
  WantCritDmg(24);

  static const BufStaticHdr(ComboData, combosGlove,
    CombosStatLegendary
    Combo("8+ crit damage", want8CritDmg.data),
    Combo("8+ crit damage and 6+ stat", want8CritDmg6Stat.data),
    Combo("8+ crit damage and 9+ stat", want8CritDmg9Stat.data),
    Combo("8+ crit damage and 12+ stat", want8CritDmg12Stat.data),
    Combo("8+ crit damage and 18+ stat", want8CritDmg18Stat.data),
    Combo("8+ crit damage and 24 stat", want8CritDmg24Stat.data),
    Combo("16+ crit damage", want16CritDmg.data),
    Combo("16+ crit damage and 6+ stat", want16CritDmg6Stat.data),
    Combo("16+ crit damage and 9+ stat", want16CritDmg9Stat.data),
    Combo("16+ crit damage and 12 stat", want16CritDmg12Stat.data),
    Combo("24 crit damage", want24CritDmg.data),
  );

#define WantAutoSteal(x) \
  static const BufStaticHdr(Want, want##x##AutoSteal, \
    WantStat(AUTOSTEAL, x),\
    WantOp(AND, -1), \
  )

  WantAutoSteal(1);
  WantAutoSteal(2);
  WantAutoSteal(3);
  WantAutoSteal(4);
  WantAutoSteal(5);
  WantAutoSteal(6);
  WantAutoSteal(7);
  WantAutoSteal(8);
  WantAutoSteal(9);
  WantAutoSteal(10);
  WantAutoSteal(12);
  WantAutoSteal(13);
  WantAutoSteal(14);
  WantAutoSteal(15);
  WantAutoSteal(17);
  WantAutoSteal(19);
  WantAutoSteal(21);

  static const BufStaticHdr(ComboData, combosAutoSteal,
    Combo("3+ auto steal", want3AutoSteal.data),
    Combo("5+ auto steal", want5AutoSteal.data),
    Combo("7+ auto steal", want7AutoSteal.data),
    Combo("10+ auto steal", want10AutoSteal.data),
    Combo("12+ auto steal", want12AutoSteal.data),
    Combo("13+ auto steal", want13AutoSteal.data),
    Combo("14+ auto steal", want14AutoSteal.data),
    Combo("15+ auto steal", want15AutoSteal.data),
    Combo("17+ auto steal", want17AutoSteal.data),
    Combo("19+ auto steal", want19AutoSteal.data),
    Combo("21 auto steal", want21AutoSteal.data),
  );

#define WantItemsRecovery(x) \
  static const BufStaticHdr(Want, want##x##ItemsRecovery, \
    WantStat(HP_ITEMS_AND_SKILLS, x),\
    WantOp(AND, -1), \
  )

  WantItemsRecovery(30);
  WantItemsRecovery(60);
  WantItemsRecovery(70);
  WantItemsRecovery(100);
  WantItemsRecovery(110);
  WantItemsRecovery(120);

  static const BufStaticHdr(ComboData, combosHeartBadge,
    CombosStatLegendary
    Combo("30+ hp items and skills recovery", want30ItemsRecovery.data),
    Combo("60+ hp items and skills recovery", want60ItemsRecovery.data),
  );

  static const BufStaticHdr(ComboData, combosHeartBadgeMeister,
    CombosStatLegendary
    Combo("30+ hp items and skills recovery", want30ItemsRecovery.data),
    Combo("60+ hp items and skills recovery", want60ItemsRecovery.data),
    Combo("70+ hp items and skills recovery", want70ItemsRecovery.data),
    Combo("100+ hp items and skills recovery", want100ItemsRecovery.data),
    Combo("110+ hp items and skills recovery", want110ItemsRecovery.data),
    Combo("120 hp items and skills recovery", want120ItemsRecovery.data),
  );

  static const BufStaticHdr(Want, want9AttOr30BossOr30Ied,
    WantStat(ATT, 9),
    WantStat(BOSS, 30),
    WantStat(IED, 30),
    WantOp(OR, -1),
  );

  static const BufStaticHdr(Want, want9AttOr30Boss,
    WantStat(ATT, 9),
    WantStat(BOSS, 30),
    WantOp(OR, -1),
  );

  static const BufStaticHdr(Want, want9AttOr30Ied,
    WantStat(ATT, 9),
    WantStat(IED, 30),
    WantOp(OR, -1),
  );


  static const BufStaticHdr(ComboData, combosWsUni,
    Combo("9+ att or 30+ boss or 30+ ied", want9AttOr30BossOr30Ied.data),
    Combo("9+ att or 30+ boss", want9AttOr30Boss.data),
    Combo("30+ boss", want30Boss.data),
    Combo("9+ att or 30+ ied", want9AttOr30Ied.data),
    Combo("9+ att", want9Att.data),
    Combo("30+ ied", want30Ied.data),
    Combo("35+ boss", want35Boss.data),
    Combo("40 boss", want40Boss.data),
    Combo("12 att", want12Att.data),
    Combo("40 ied", want40Ied.data),
    Combo("35+ ied", want35Ied.data),
  );

  static const BufStaticHdr(ComboData, combosEUni,
    Combo("9+ att or 30+ ied", want9AttOr30Ied.data),
    Combo("9+ att", want9Att.data),
    Combo("30+ ied", want30Ied.data),
    Combo("12 att", want12Att.data),
    Combo("40 ied", want40Ied.data),
    Combo("35+ ied", want35Ied.data),
  );

#define CombosStatUniCommon \
    Combo("6+ stat", want6Stat.data), \
    Combo("9+ stat", want9Stat.data), \
    Combo("9+ hp", want9Hp.data), \
    Combo("6 allstat", want6AllStat.data), \
    Combo("12 stat", want12Stat.data), \
    Combo("12 hp", want12Stat.data), \
    Combo("9 allstat", want9AllStat.data), \

  static const BufStaticHdr(ComboData, combosStatUni,
    CombosStatUniCommon
  );

  static const BufStaticHdr(ComboData, combosAccessoryUni,
    CombosStatUniCommon
    Combo("20 meso", want20Meso.data),
    Combo("20 drop", want20Drop.data),
    Combo("20 meso or 20 drop", want20MesoOrDrop.data),
  );

  static const BufStaticHdr(ComboData, combosGloveUni,
    CombosStatUniCommon
    Combo("8 crit damage", want8CritDmg.data),
  );

  static const BufStaticHdr(ComboData, combosHatUni,
    CombosStatUniCommon
    Combo("1+s cooldown", want1Cd.data),
    Combo("2s cooldown", want2Cd.data),
  );

#define WantHpHeal(x) \
  static const BufStaticHdr(Want, want##x##HpHealing, \
    WantStat(HEAL_HP, x), \
    WantOp(AND, -1), \
  )

  WantHpHeal(5);
  WantHpHeal(10);
  WantHpHeal(15);
  WantHpHeal(20);

#define WantMpHeal(x) \
  static const BufStaticHdr(Want, want##x##MpHealing, \
    WantStat(HEAL_MP, x), \
    WantOp(AND, -1), \
  )

  WantMpHeal(5);
  WantMpHeal(10);
  WantMpHeal(15);
  WantMpHeal(20);

  AnyNl(BossHpHeal, 2, HEAL_HP, BOSS_ONLY);
  AnyNl(DropAutoSteal, 2, DROP, AUTOSTEAL);

#define WantDamage(x) \
  static const BufStaticHdr(Want, want##x##Damage, \
    WantStat(DAMAGE, x), \
    WantOp(AND, -1), \
  )

  WantDamage(1);
  WantDamage(2);
  WantDamage(3);


#define CombosFamCommon \
    Combo("15+ ied", want15Ied.data), \
    Combo("30+ meso", want30Meso.data), \
    Combo("30+ drop", want30Drop.data), \
    Combo("1+ damage", want1Damage.data), \

  static const BufStaticHdr(ComboData, combosFamCommon,
    CombosFamCommon
  );

  static const BufStaticHdr(ComboData, combosFamRare,
    CombosFamCommon
    Combo("30+ ied", want30Ied.data),
    Combo("2+ damage", want2Damage.data),
    Combo("3+ damage", want3Damage.data),
    Combo("20+ meso", want20Meso.data),
    Combo("20+ drop", want20Drop.data),
    Combo("20+ meso and drop", want20MesoDrop.data),
    Combo("50+ meso", want50Meso.data),
    Combo("50+ drop", want50Drop.data),
    Combo("70+ drop", want70Drop.data),
    Combo("70+ meso", want70Meso.data),
    Combo("5+ hp healing", want5HpHealing.data),
    Combo("5+ mp healing", want5MpHealing.data),
  );

#define CombosFamEpic \
    Combo("20+ boss", want20Boss.data), \
    Combo("30+ boss", want30Boss.data), \
    Combo("any 2l combo of boss and hp healing", wantAny2lBossHpHeal.data), \
    Combo("20+ ied", want20Ied.data), \
    Combo("30+ ied", want30Ied.data), \
    Combo("25+ drop", want25Drop.data), \
    Combo("50+ drop", want50Drop.data), \
    Combo("100+ drop", want100Drop.data), \
    Combo("25+ meso", want25Meso.data), \
    Combo("25+ meso and drop", want25MesoDrop.data), \
    Combo("40+ meso and drop", want40MesoDrop.data), \
    Combo("1+ auto steal", want1AutoSteal.data), \
    Combo("2+ auto steal", want2AutoSteal.data), \
    Combo("any 2l combo of drop and auto steal", wantAny2lDropAutoSteal.data), \
    Combo("10+ hp healing", want10HpHealing.data), \
    Combo("10+ mp healing", want10MpHealing.data), \
    Combo("15+ hp healing", want15HpHealing.data), \
    Combo("15+ mp healing", want15MpHealing.data), \

  static const BufStaticHdr(ComboData, combosFamEpic,
    CombosFamEpic
  );

  AnyNl(HpHealingHpItems, 2, HEAL_HP, HP_ITEMS_AND_SKILLS);
  AnyNl(MesoDrop, 2, MESO, DROP);
  AnyNl(BossIed, 2, BOSS_ONLY, IED);
  AnyNl1(Boss, 2, BOSS_ONLY);

#define WantBossHpHealing(x) \
  static const BufStaticHdr(Want, want##x##BossAndHpHealing, \
    WantStat(BOSS_ONLY, x), \
    WantStat(HEAL_HP, 1), \
    WantOp(AND, -1), \
  )

  WantBossHpHealing(35);
  WantBossHpHealing(40);
  WantBossHpHealing(45);
  WantBossHpHealing(50);

  static const BufStaticHdr(Want, want25Meso90Drop,
    WantStat(MESO, 25),
    WantStat(DROP, 90),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want15HpHealingHpItems,
    WantStat(HEAL_HP, 15),
    WantStat(HP_ITEMS_AND_SKILLS, 15),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(ComboData, combosFamUnique,
    CombosFamEpic
    Combo("35+ boss", want35Boss.data),
    Combo("40+ boss", want40Boss.data),
    Combo("35+ boss and any hp healing", want35BossAndHpHealing.data),
    Combo("40+ boss and any hp healing", want40BossAndHpHealing.data),
    Combo("35+ ied", want35Ied.data),
    Combo("40+ ied", want40Ied.data),
    Combo("any 2l combo of boss and ied", wantAny2lBossIed.data),
    Combo("any 2l combo of boss", wantAny2lBoss.data),
    Combo("50+ boss ", want50Boss.data),
    Combo("50+ meso and drop", want50MesoDrop.data),
    Combo("25+ meso and 90+ drop", want25Meso90Drop.data),
    Combo("any 2l combo of meso and drop", wantAny2lMesoDrop.data),
    Combo("any 2l combo of drop and auto steal", wantAny2lDropAutoSteal.data),
    Combo("3+ auto steal", want3AutoSteal.data),
    Combo("4+ auto steal", want4AutoSteal.data),
    Combo("5+ auto steal", want5AutoSteal.data),
    Combo("6+ auto steal", want6AutoSteal.data),
    Combo("7+ auto steal", want7AutoSteal.data),
    Combo("8+ auto steal", want8AutoSteal.data),
    Combo("9+ auto steal", want9AutoSteal.data),
    Combo("any 2l combo of hp heal and items/skills rec", wantAny2lHpHealingHpItems.data),
    Combo("15+ hp healing and 15+ items/skills rec", want15HpHealingHpItems.data),
    Combo("20+ hp healing", want20HpHealing.data),
    Combo("20+ mp healing", want20MpHealing.data),
  );

  static const BufStaticHdr(ComboData, combosFamLegendary,
    Combo("40+ boss", want40Boss.data),
    Combo("45+ boss", want45Boss.data),
    Combo("50+ boss", want50Boss.data),
    Combo("60+ boss", want60Boss.data),
    Combo("any 2l combo of boss and hp healing", wantAny2lBossHpHeal.data),
    Combo("45+ boss and any hp healing", want45BossAndHpHealing.data),
    Combo("50+ boss and any hp healing", want50BossAndHpHealing.data),
    Combo("any 2l combo of hp heal and items/skills rec", wantAny2lHpHealingHpItems.data),
    Combo("15+ hp healing and 15+ items/skills rec", want15HpHealingHpItems.data),
    Combo("40+ ied", want40Ied.data),
    Combo("45+ ied", want45Ied.data),
    Combo("50+ ied", want50Ied.data),
    Combo("60+ ied", want60Ied.data),
    Combo("any 2l combo of drop and auto steal", wantAny2lDropAutoSteal.data),
    Combo("4+ auto steal", want4AutoSteal.data),
    Combo("6+ auto steal", want6AutoSteal.data),
    Combo("8+ auto steal", want8AutoSteal.data),
    Combo("12+ auto steal", want12AutoSteal.data),
    Combo("13+ auto steal", want13AutoSteal.data),
    Combo("14+ auto steal", want14AutoSteal.data),
  );

  static const BufStaticHdr(int, redBlackMeister, RED, BLACK, MEISTER);
  static const BufStaticHdr(int, redBlack, RED, BLACK);
  static const BufStaticHdr(int, violetEquality, VIOLET, EQUALITY);
  static const BufStaticHdr(int, master, MASTER);
  static const BufStaticHdr(int, meister, MEISTER);
  static const BufStaticHdr(int, red, RED);
  static const BufStaticHdr(int, occult, OCCULT);
  static const BufStaticHdr(int, bonus, BONUS);
  static const BufStaticHdr(int, uni, UNI);
  static const BufStaticHdr(int, familiar, FAMILIAR);
  static const BufStaticHdr(int, familiarCard, RED_FAM_CARD);

  static const BufStaticHdr(ComboGroup, groups,
    ComboGroup(WEAPON, redBlackMeister.data, LEGENDARY, combosWs.data),
    ComboGroup(SECONDARY, redBlackMeister.data, LEGENDARY, combosWs.data),
    ComboGroup(WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING,
      violetEquality.data, LEGENDARY, combosWs.data),
    ComboGroup(WEAPON, master.data, UNIQUE, combosWsMaster.data),
    ComboGroup(SECONDARY, master.data, UNIQUE, combosWsMaster.data),
    ComboGroup(EMBLEM, redBlackMeister.data, LEGENDARY, combosE.data),
    ComboGroup(EMBLEM, violetEquality.data, LEGENDARY, combosE.data),
    ComboGroup(EMBLEM, master.data, UNIQUE, combosEMaster.data),
    ComboGroup(WEAPON, occult.data, EPIC, combosWSEOccult.data),
    ComboGroup(SECONDARY, occult.data, EPIC, combosWSEOccult.data),
    ComboGroup(EMBLEM, occult.data, EPIC, combosWSEOccult.data),
    ComboGroup(WEAPON, bonus.data, LEGENDARY, combosWSEBonus.data),
    ComboGroup(SECONDARY, bonus.data, LEGENDARY, combosWSEBonus.data),
    ComboGroup(EMBLEM, bonus.data, LEGENDARY, combosWSEBonus.data),
    ComboGroup(HAT, bonus.data, RARE, combosBonusRare.data),
    ComboGroup(TOP_OVERALL, redBlackMeister.data, LEGENDARY, combosStat.data),
    ComboGroup(TOP_OVERALL, violetEquality.data, LEGENDARY, combosStat.data),
    ComboGroup(CAPE_BELT_SHOULDER, redBlackMeister.data, LEGENDARY, combosStat.data),
    ComboGroup(CAPE_BELT_SHOULDER, violetEquality.data, LEGENDARY, combosStat.data),
    ComboGroup(SHOE, violetEquality.data, LEGENDARY, combosStat.data),
    ComboGroup(BOTTOM, redBlackMeister.data, LEGENDARY, combosStat.data),
    ComboGroup(BOTTOM, violetEquality.data, LEGENDARY, combosStat.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT,
      redBlackMeister.data, LEGENDARY, combosAccessory.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT,
      violetEquality.data, LEGENDARY, combosAccessory.data),
    ComboGroup(HAT, redBlackMeister.data, LEGENDARY, combosHat.data),
    ComboGroup(HAT, violetEquality.data, LEGENDARY, combosHat.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT, occult.data, EPIC, combosStatOccult.data),
    ComboGroup(TOP_OVERALL, occult.data, EPIC, combosStatOccult.data),
    ComboGroup(HAT, occult.data, EPIC, combosStatOccult.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT, master.data, UNIQUE, combosStatMaster.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT, meister.data, UNIQUE, combosStatMaster.data),
    ComboGroup(TOP_OVERALL, master.data, UNIQUE, combosStatMaster.data),
    ComboGroup(TOP_OVERALL, meister.data, UNIQUE, combosStatMaster.data),
    ComboGroup(HAT, master.data, UNIQUE, combosStatMaster.data),
    ComboGroup(HAT, meister.data, UNIQUE, combosStatMaster.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT, red.data, UNIQUE, combosStatMaster.data),
    ComboGroup(TOP_OVERALL, red.data, UNIQUE, combosStatMaster.data),
    ComboGroup(HAT, red.data, UNIQUE, combosStatMaster.data),
    ComboGroup(GLOVE, redBlackMeister.data, LEGENDARY, combosGlove.data),
    ComboGroup(GLOVE, violetEquality.data, LEGENDARY, combosGlove.data),
    ComboGroup(GLOVE, meister.data, LEGENDARY, combosAutoSteal.data),
    ComboGroup(HEART_BADGE, redBlack.data, LEGENDARY, combosHeartBadge.data),
    ComboGroup(HEART_BADGE, meister.data, LEGENDARY, combosHeartBadgeMeister.data),

    ComboGroup(WEAPON | SECONDARY | FORCE_SHIELD_SOUL_RING, uni.data, LEGENDARY, combosWsUni.data),
    ComboGroup(EMBLEM, uni.data, LEGENDARY, combosEUni.data),
    ComboGroup(CAPE_BELT_SHOULDER, uni.data, LEGENDARY, combosStatUni.data),
    ComboGroup(SHOE, uni.data, LEGENDARY, combosStatUni.data),
    ComboGroup(BOTTOM, uni.data, LEGENDARY, combosStatUni.data),
    ComboGroup(TOP_OVERALL, uni.data, LEGENDARY, combosStatUni.data),
    ComboGroup(FACE_EYE_RING_EARRING_PENDANT, uni.data, LEGENDARY, combosAccessoryUni.data),
    ComboGroup(GLOVE, uni.data, LEGENDARY, combosGloveUni.data),
    ComboGroup(HAT, uni.data, LEGENDARY, combosHatUni.data),

    ComboGroup(FAMILIAR_STATS, familiar.data, COMMON, combosFamCommon.data),
    ComboGroup(FAMILIAR_STATS, familiar.data, RARE, combosFamRare.data),
    ComboGroup(FAMILIAR_STATS, familiar.data, EPIC, combosFamEpic.data),
    ComboGroup(FAMILIAR_STATS, familiar.data, UNIQUE, combosFamUnique.data),
    ComboGroup(FAMILIAR_STATS, familiar.data, LEGENDARY, combosFamLegendary.data),
    ComboGroup(FAMILIAR_STATS, familiarCard.data, LEGENDARY, combosFamLegendary.data),
  );

  BufEach(ComboGroup const, groups.data, g) {
    char* scategory = CategoryToStrSep(", ", g->category);

    BufEach(int const, g->cubes, cube) {
      Align* a = AlignInit();

      char* scube = CubeToStr(*cube);
      PrintHdr(" %s (%s on lv%d %s) ", scategory, scube, g->level, TierToStr(g->tier));

      BufEach(ComboData const, g->combos, x) {
        float p = CubeCalc(x->wantBuf, g->category, *cube, g->tier, g->level, g->region, 0);
        if (p > 0) {
          AlignFeed(a, "%s", " 1 in %.0f cubes, %.4f%%", x->description, round(1/p), p * 100);
        } else {
          AlignFeed(a, "%s", " impossible", x->description);
        }
      }

      BufFree(&scube);

      AlignPrint(a, stdout);
      AlignFree(a);
    }

    BufFree(&scategory);
  }

  CubeGlobalFree();
  return 0;
}
