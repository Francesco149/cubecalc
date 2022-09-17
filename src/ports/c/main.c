#include "utils.c"
#include "generated.c"

#include <stdio.h>
#include <math.h>
#include <string.h>

#define WantOps(f) \
  f(NULL) \
  f(AND) \
  f(OR) \

#undef SUFFIX
#define SUFFIX WANT
enum WantOp { WantOps(AppendComma) };
#undef SUFFIX
#define SUFFIX
char const* const wantOpNames[] = { WantOps(StringifyComma) };

typedef enum _WantType {
  WANT_STAT,
  WANT_OPERATOR,
  WANT_MASK,
} WantType;

typedef struct _Want {
  WantType type;
  union {
    struct {
      int lineLo;
      int lineHi;
      int value;
    };
    int op;
    int* mask;
  };
} Want;

char* LineToStr(int hi, int lo) {
  char* res = 0;
  size_t nflags = 0;
  hi &= ~(LINE_A_HI | LINE_B_HI | LINE_C_HI);
  lo &= ~(LINE_A_LO | LINE_B_LO | LINE_C_LO);
  for (size_t i = 0; i < ArrayLength(allLinesHi); ++i) {
    if (((hi & allLinesHi[i]) || !allLinesHi[i]) &&
        ((lo & allLinesLo[i]) || !allLinesLo[i]))
    {
      BufAllocCharsf(&res, "%s | ", allLineNames[i]);
      ++nflags;
    }
  }
  // remove trailing separator
  if (nflags) {
    BufHdr(res)->len -= 3; // 2 chars + null char
    BufAt(res, -1) = 0;
  }
  return res;
}

void WantPrint(Want* wantBuf) {
  BufEach(Want, wantBuf, w) {
    switch (w->type) {
      case WANT_STAT: {
        char* line = LineToStr(w->lineHi, w->lineLo);
        printf("%d %s\n", w->value, line);
        BufFree(&line);
        break;
      }
      case WANT_OPERATOR:
        printf("<%s>\n", wantOpNames[w->op]);
        break;
      case WANT_MASK:
        puts("*mask*");
        break;
    }
  }
}

Map* DataFindMap(int cubeMask) {
  if (cubeMask & FAMILIAR) {
    return fams;
  }
  if (cubeMask & (VIOLET | EQUALITY | UNI)) {
    return tms;
  }
  return kms;
}

Map* DataFind(int categoryMask, int cubeMask) {
  Map* res = 0;
  Map* data = DataFindMap(categoryMask);
  int* cubes = MapKeys(data);
  BufEach(int, cubes, cube) {
    // TODO: vectorize
    if (*cube & cubeMask) {
      Map* categoryMap = MapGet(data, *cube);
      int* categories = MapKeys(categoryMap);
      BufEach(int, categories, category) {
        if (*category & categoryMask) {
          res = MapGet(categoryMap, *category);
          break;
        }
      }
      BufFree(&categories);
      if (res) {
        break;
      }
    }
  }
cleanup:
  BufFree(&cubes);
  return res;
}

void DataPrint(Map* data, int tier) {
  LineData* ld = MapGet(data, tier);
  if (!ld) {
    puts("(null)");
    return;
  }
  size_t maxlen = 0;
  size_t* lens = 0;
  char** ss = 0;
  BufEachi(ld->lineHi, i) {
    char* s = LineToStr(ld->lineHi[i], ld->lineLo[i]);
    size_t len = strlen(s);
    maxlen = Max(len, maxlen);
    *BufAlloc(&lens) = len;
    *BufAlloc(&ss) = s;
  }
  BufEachi(ld->lineHi, i) {
    for (size_t x = 0; x < maxlen + 1 - lens[i]; ++x) putchar(' ');
    printf("%s 1 in %g\n", ss[i], ld->onein[i]);
    BufFree(&ss[i]);
  }
  BufFree(&lens);
  BufFree(&ss);
}

// return non-zero on success
int ValueGet(int* out, int cubeMask, int categoryMask, int regionMask, int maxLevel, int tier,
    int lineHi, int lineLo)
{
  size_t i = valueGroupFind(cubeMask, categoryMask, regionMask, maxLevel);
  if (i >= valueGroupsLen) return 0;
  if (!valueGroups[i]) return 0;

  Map* hi = MapGet(valueGroups[i], tier);
  if (!hi) return 0;

  Map* lo = MapGet(hi, lineHi);
  if (!lo) return 0;

  if (!MapHas(lo, lineLo)) return 0;
  *out = (int)(intptr_t)MapGet(lo, lineLo);

  return 1;
}

double CubeCalc(Want* wantBuf, int category, int cube, int tier, int lvl, int region, Map* data) {
  WantPrint(wantBuf);
  puts("# prime");
  DataPrint(data, tier);
  puts("");
  puts("# nonprime");
  DataPrint(data, tier - 1);
  return 0;
}

#define _WantStatLine(line) .lineLo = line##_LO, .lineHi = line##_HI
#define WantStat(line, val) (Want){ .type = WANT_STAT, _WantStatLine(line), .value = val }
#define Line(x) x##_LO, x##_HI

int main() {
  cubecalcGeneratedGlobalInit();

  Map* weaponCash = DataFind(RED, WEAPON);

  BufStatic(Want, want,
    WantStat(ATT, 21),
    WantStat(BOSS, 30),
  );

  double p = CubeCalc(want, WEAPON, RED, LEGENDARY, 150, KMS, weaponCash);
  puts("");
  if (p > 0) {
    printf("1 in %d\n", (int)round(1/p));
  } else {
    puts("impossible");
  }

  cubecalcGeneratedGlobalFree();
  return 0;
}