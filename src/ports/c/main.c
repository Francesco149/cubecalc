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
  int* cubes;
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
}

int main() {
  CubeGlobalInit();

  PrintHdr(" ! DISCLAIMER ! ");
  printf("\n%s", disclaimer);

  static const BufStaticHdr(Want, wantAny2lAttBoss,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(LINES, 2),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, wantAny2lAttBossIed,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(IED, 1),
    WantStat(LINES, 2),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, wantAny3lAttBoss,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(LINES, 3),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, wantAny3lAttBossIed,
    WantStat(ATT, 1),
    WantStat(BOSS_ONLY, 1),
    WantStat(IED, 1),
    WantStat(LINES, 3),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want18Att,
    WantStat(ATT, 18),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(Want, want21Att,
    WantStat(ATT, 21),
    WantOp(AND, -1),
  );

  static const BufStaticHdr(ComboData, combosWs,
    Combo("any 2l combo of att+boss", wantAny2lAttBoss.data),
    Combo("any 2l combo of att+boss+ied", wantAny2lAttBossIed.data),
    Combo("any 3l combo of att+boss", wantAny3lAttBoss.data),
    Combo("any 3l combo of att+boss+ied", wantAny3lAttBossIed.data),
    Combo("18+ att", want18Att.data),
    Combo("21+ att", want21Att.data),
  );

  static const BufStaticHdr(int, redBlack, RED, BLACK);

  static const BufStaticHdr(ComboGroup, groups,
    ComboGroup(WEAPON, redBlack.data, LEGENDARY, combosWs.data),
  );

  BufEach(ComboGroup const, groups.data, g) {
    char* scategory = CategoryToStr(g->category);

    BufEach(int const, g->cubes, cube) {
      Align* a = AlignInit();

      char* scube = CubeToStr(*cube);
      PrintHdr(" %s (%s on lvl%d %s) ", scategory, scube, g->level, TierToStr(g->tier));

      BufEach(ComboData const, g->combos, x) {
        float p = CubeCalc(x->wantBuf, g->category, *cube, g->tier, g->level, g->region, 0);
        if (p > 0) {
          AlignFeed(a, "%s", " 1 in %d cubes, %.4f%%", x->description, (int)round(1/p), p * 100);
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
