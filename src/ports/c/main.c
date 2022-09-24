#include "cubecalc.c"
#include "generated.c"

#include <stdio.h>
#include <math.h>

typedef struct _ComboData {
  char const* description;
  Want const* wantBuf;
} ComboData;

#define Combo(desc, want) \
  (ComboData){ .description = (desc), .wantBuf = (want) }

int main() {
  CubeGlobalInit();

  printf("%s", disclaimer);

  static const BufStaticHdr(Want const, wantAny2lAttBoss,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(LINES, 2),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want const, wantAny2lAttBossIed,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(IED, 1),
    WantStat(LINES, 2),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want const, wantAny3lAttBoss,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(LINES, 3),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want const, wantAny3lAttBossIed,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(IED, 1),
    WantStat(LINES, 3),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want const, want18Att,
    WantStat(ATT, 18),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want const, want21Att,
    WantStat(ATT, 21),
    WantOp(AND, -1),
  );

  static const BufStatic(ComboData const, combosWs,
    Combo("any 2l combo of att+boss", wantAny2lAttBoss.data),
    Combo("any 2l combo of att+boss+ied", wantAny2lAttBossIed.data),
    Combo("any 3l combo of att+boss", wantAny3lAttBoss.data),
    Combo("any 3l combo of att+boss+ied", wantAny3lAttBossIed.data),
    Combo("18+ att", want18Att.data),
    Combo("21+ att", want21Att.data),
  );

  BufEach(ComboData const, combosWs, x) {
    float p = CubeCalc(x->wantBuf, WEAPON, RED, LEGENDARY, 150, GMS, 0);
    printf("%s ", x->description);
    if (p > 0) {
      printf("1 in %d cubes, %.4f%%\n", (int)round(1/p), p * 100);
    } else {
      puts("impossible");
    }
  }

  CubeGlobalFree();
  return 0;
}
