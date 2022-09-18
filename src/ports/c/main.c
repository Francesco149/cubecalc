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
  BufFree(&cubes);
  return res;
}

#ifdef CUBECALC_DEBUG
void DataPrint(Map* data, int tier, int* values) {
  LineData* ld = MapGet(data, tier);
  if (!ld) {
    puts("(null)");
    return;
  }
  size_t maxlen = 0;
  size_t* lens = 0;
  char** ss = 0;
#define FMT "%d %s 1"
  BufEachi(ld->lineHi, i) {
    char* s = LineToStr(ld->lineHi[i], ld->lineLo[i]);
    size_t len = snprintf(0, 0, FMT, values[i], s, ld->onein[i]);
    maxlen = Max(len, maxlen);
    *BufAlloc(&lens) = len;
    *BufAlloc(&ss) = s;
  }
  BufEachi(ld->lineHi, i) {
    for (size_t x = 0; x < maxlen + 1 - lens[i]; ++x) putchar(' ');
    printf(FMT " in %g\n", values[i], ss[i], ld->onein[i]);
    BufFree(&ss[i]);
  }
#undef FMT
  BufFree(&lens);
  BufFree(&ss);
}
#endif

typedef struct _Lines {
  int* lineHi;
  int* lineLo;
  float* onein;
  int* value;
  int* prime;
} Lines;

void LinesFree(Lines* l) {
  BufFree(&l->lineHi);
  BufFree(&l->lineLo);
  BufFree(&l->onein);
  BufFree(&l->value);
  BufFree(&l->prime);
}

int LinesCatData(Lines* l, Map* data, size_t group, int tier) {
  Map* hi = MapGet(valueGroups[group], tier);
  if (!hi) {
    fprintf(stderr, "no data for tier %d\n", tier);
    return 0;
  }
  LineData* ld = MapGet(data, tier);
  if (ld) {
    BufCat(&l->lineHi, ld->lineHi);
    BufCat(&l->lineLo, ld->lineLo);
    BufCat(&l->onein, ld->onein);
    BufEachi(ld->lineHi, i) {
      int lineHi = ld->lineHi[i];
      int lineLo = ld->lineLo[i];
      Map* lo = MapGet(hi, lineHi);
      if (!lo || !MapHas(lo, lineLo)) {
        char* s = LineToStr(lineHi, lineLo);
        fprintf(stderr, "no value for %s\n", s);
        BufFree(&s);
        return 0;
      }
      *BufAlloc(&l->value) = (int)(intptr_t)MapGet(lo, lineLo);
    }
  }
  return 1;
}

int LinesInit(Lines* l, Map* data, size_t group, int tier) {
  if (!LinesCatData(l, data, group, tier)) return 0;
  size_t numPrimes = BufLen(l->lineHi);
  if (!LinesCatData(l, data, group, tier - 1)) return 0;
  size_t bitSize = ArrayBitSize(l->prime, BufLen(l->lineHi));
  (void)BufReserve(&l->prime, bitSize / ArrayElementSize(l->prime));
  BufZero(l->prime);
  for (size_t i = 0; i < numPrimes; ++i) {
    ArrayBitSet(l->prime, i);
  }
  return 1;
}

size_t valueGroupFind(int cubeMask, int categoryMask, int regionMask, int level) {
  int minLevel = 300;
  size_t match = valueGroupsLen;
  for (size_t i = 0; i < valueGroupsLen; ++i) {
    if ((valueGroupsCubeMask[i] & cubeMask) &&
        (valueGroupsCategoryMask[i] & categoryMask) &&
        (valueGroupsRegionMask[i] & regionMask) &&
        (valueGroupsMaxLevel[i] >= level))
    {
      if (valueGroupsMaxLevel[i] < minLevel) {
        minLevel = valueGroupsMaxLevel[i];
        match = i;
      }
    }
  }
  if (match >= valueGroupsLen) {
    fprintf(stderr, "couldn't match cube 0x%x category 0x%x region 0x%x level %d\n",
      cubeMask, categoryMask, regionMask, level);
  }
  return match;
}

double CubeCalc(Want* wantBuf, int category, int cube, int tier, int lvl, int region, Map* data) {
  size_t group = valueGroupFind(cube, category, region, lvl);
  if (group >= valueGroupsLen || !valueGroups[group]) {
    fprintf(stderr, "failed to find value group\n");
    return 0;
  }

  Lines l = {0};
  if (!LinesInit(&l, data, group, tier)) {
    goto cleanup;
  }

#ifdef CUBECALC_DEBUG
  size_t numPrimes = BitCount(l.prime, ArrayElementSize(l.prime) * BufLen(l.prime));
  WantPrint(wantBuf);
  puts("# prime");
  DataPrint(data, tier, l.value);
  puts("");
  puts("# nonprime");
  DataPrint(data, tier - 1, l.value + numPrimes);
  puts("");
#endif



cleanup:
  LinesFree(&l);
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

  double p = CubeCalc(want, WEAPON, RED, LEGENDARY, 150, GMS, weaponCash);
  puts("");
  if (p > 0) {
    printf("1 in %d\n", (int)round(1/p));
  } else {
    puts("impossible");
  }

  cubecalcGeneratedGlobalFree();
  return 0;
}
