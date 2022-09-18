#include "utils.c"
#include "generated.c"

#include <stdio.h>
#include <math.h>
#include <string.h>

#define WantOps(f) \
  f(NULLOP) \
  f(AND) \
  f(OR) \

#define WantTypes(f) \
  f(NULLTYPE) \
  f(STAT) \
  f(OP) \
  f(MASK) \

#undef PREFIX
#define PREFIX(x) WANT_##x
DefEnum(WantOp);
DefEnum(WantType);
#undef PREFIX
#define PREFIX(x) DEF_PREFIX(x)

typedef struct _Want {
  WantType type;
  union {
    struct {
      int lineLo;
      int lineHi;
      int value;
    };
    struct {
      WantOp op;
      int opCount;
    };
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

// a |= b
void WantOr(Want* a, Want* b) {
  a->lineLo |= b->lineLo;
  a->lineHi |= b->lineHi;
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

#define LinesFields(f) \
  f(int*, lineHi) \
  f(int*, lineLo) \
  f(float*, onein) \
  f(int*, value) \

#define LinesAllFields(f) \
  LinesFields(f) \
  f(int*, prime) \

#define DeclField(type, name) type name;
typedef struct _Lines { LinesAllFields(DeclField) } Lines;

#define FreeField(type, name) BufFree(&l->name);
void LinesFree(Lines* l) {
  LinesAllFields(FreeField)
}

void LinesFilt(Lines* l, int* mask) {
  size_t j = 0;
  BufEachi(l->lineHi, i) {
    if (ArrayBit(mask, i)) {
#define a(t, x) l->x[j] = l->x[i];
      LinesFields(a)
#undef a
      if (ArrayBit(l->prime, i)) {
        ArrayBitSet(l->prime, j);
      } else {
        ArrayBitClear(l->prime, j);
      }
      ++j;
    }
  }
#define a(t, x) BufHdr(l->x)->len = j;
  LinesFields(a)
  BufHdr(l->prime)->len = ArrayBitElements(l->prime, j);
#undef a
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
  (void)BufReserve(&l->prime, ArrayBitElements(l->prime, BufLen(l->lineHi)));
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

void WantFree(Want* w) {
  if (w->type == WANT_MASK) BufFree(&w->mask);
}

void WantStackPop(Want* stack, intmax_t n) {
  BufEachRange(Want, stack, -n, -1, w) {
    WantFree(w);
  }
  BufHdr(stack)->len -= n;
}

void WantStackFree(Want** pstack) {
  BufEach(Want, *pstack, w) {
    WantFree(w);
  }
  BufFree(pstack);
}

#include "debug.c"

int WantEval(Lines* l, Want** pstack, Want* wantBuf) {
  int res = 0;
  wantBuf = BufDup(wantBuf);

  size_t numOps = 0;
  BufCount(Want, wantBuf, x->type == WANT_OP, numOps);
  if (!numOps) {
    *BufAlloc(&wantBuf) = (Want){
      .type = WANT_OP,
      .op = WANT_AND,
      .opCount = -1,
    };
  }

  BufEach(Want, wantBuf, w) {
    switch (w->type) {
      case WANT_STAT:
        *BufAlloc(pstack) = *w;
        break;
      case WANT_OP: {
        int* result = 0;
        int opCount = w->opCount >= 0 ? w->opCount : BufLen(*pstack);
        BufEachRange(Want, *pstack, -opCount, -1, s) {
          int* match = 0;
          switch (s->type) {
            case WANT_STAT: {
              int* matchLo;
              BufMask(int, l->lineHi, *x & s->lineHi, match);
              BufMask(int, l->lineLo, *x & s->lineLo, matchLo);
              BufAND(match, matchLo);
              BufFree(&matchLo);

              s->type = WANT_MASK;
              s->mask = match;

              if (!result) {
                result = match;
                s->mask = 0; // prevent result from being freed
                break;
              }

              // fall through to the MASK case
            }
            case WANT_MASK:
#define c(x) case WANT_##x: Buf##x(result, s->mask); break
              switch (w->op) {
                c(AND);
                c(OR);
                default:
                  fprintf(stderr, "unsupported operator %s\n", WantOpNames[w->op]);
                  goto cleanup;
              }
#undef c
              break;
            default:
              fprintf(stderr, "unsupported operand %s\n", WantTypeNames[s->type]);
              goto cleanup;
          }
        }
        WantStackPop(*pstack, opCount);
        *BufAlloc(pstack) = (Want){
          .type = WANT_MASK,
          .mask = result,
        };
        break;
      }
      default:
        fprintf(stderr, "%s is only for internal use\n", WantTypeNames[w->type]);
        goto cleanup;
    }
  }

  if (BufLen(*pstack) > 1) {
    fprintf(stderr, "%zu values on the stack, expected 1\n", BufLen(*pstack));
#ifdef CUBECALC_DEBUG
    puts("");
    puts("# final stack");
    WantPrint(*pstack);
    puts("");
#endif
    goto cleanup;
  }

  int typ =(*pstack)[0].type;
  if (typ != WANT_MASK) {
    fprintf(stderr, "expected WANT_MASK result, got %s\n", WantTypeNames[typ]);
    goto cleanup;
  }

  res = 1;

cleanup:
  BufFree(&wantBuf);
  return res;
}

double CubeCalc(Want* wantBuf, int category, int cube, int tier, int lvl, int region, Map* data) {
  double res = 0;

  size_t group = valueGroupFind(cube, category, region, lvl);
  if (group >= valueGroupsLen || !valueGroups[group]) {
    fprintf(stderr, "failed to find value group\n");
    return 0;
  }

  Want* stack = 0;
  Lines l = {0};
  if (!LinesInit(&l, data, group, tier)) {
    goto cleanup;
  }

#ifdef CUBECALC_DEBUG
  size_t numPrimes = BitCount(l.prime, ArrayElementSize(l.prime) * BufLen(l.prime));
  puts("# prime");
  DataPrint(data, tier, l.value);
  puts("");
  puts("# nonprime");
  DataPrint(data, tier - 1, l.value + numPrimes);
#endif

  if (!WantEval(&l, &stack, wantBuf)) {
    goto cleanup;
  }

  if (!stack[0].mask) {
    fprintf(stderr, "NULL line filter mask\n");
    goto cleanup;
  }

  LinesFilt(&l, stack[0].mask);
#ifdef CUBECALC_DEBUG
  LinesPrint(&l);
#endif

cleanup:
  LinesFree(&l);
  WantStackFree(&stack);

  return res;
}

#define _WantStatLine(line) .lineLo = line##_LO, .lineHi = line##_HI
#define WantStat(line, val) (Want){ .type = WANT_STAT, _WantStatLine(line), .value = val }
#define Line(x) x##_LO, x##_HI

int main() {
  cubecalcGeneratedGlobalInit();

  Map* weaponCash = DataFind(RED, WEAPON);

  BufStatic(Want, want,
    WantStat(MESO, 20),
    WantStat(DROP, 20),
    WantStat(STAT, 6),
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
