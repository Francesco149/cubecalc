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
    intmax_t* mask;
  };
} Want;

// some of the hi/lo masks are actually zero and replaced by NULLBIT
#define LineMask(x) ((x) & ~NULLBIT)

char* LineToStr(int hi, int lo, int full) {
  char* res = 0;
  size_t nflags = 0;
  if (!full) {
    hi &= ~LineMask(LINE_A_HI | LINE_B_HI | LINE_C_HI);
    lo &= ~LineMask(LINE_A_LO | LINE_B_LO | LINE_C_LO);
  }
  for (size_t i = 0; i < ArrayLength(allLinesHi); ++i) {
    if ((hi & allLinesHi[i]) && (lo & allLinesLo[i])) {
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
  if (cubeMask & (FAMILIAR | RED_FAM_CARD)) {
    return fams;
  }
  if (cubeMask & (VIOLET | EQUALITY | UNI)) {
    return tms;
  }
  return kms;
}

Map* DataFind(int categoryMask, int cubeMask) {
  Map* res = 0;
  Map* data = DataFindMap(cubeMask);
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

typedef struct _Lines {
  int* lineHi;
  int* lineLo;
  float* onein;
  int* value;
  uintmax_t* prime;
} Lines;

typedef union _LineFields {
  Lines data;
  int* fields[offsetof(Lines, prime) / sizeof(void*)];
  int* allFields[sizeof(Lines) / sizeof(void*)];
} LineFields;

#define F(x) ((LineFields*)(x))

void LinesFree(Lines* l) {
  ArrayEach(int*, F(l)->allFields, x) {
    BufFree(x);
  }
}

void LinesDup(Lines* dst, Lines const* src) {
  ArrayEachi(F(dst)->allFields, i) {
    F(dst)->allFields[i] = BufDup(F(src)->allFields[i]);
  }
}

size_t LinesNumPrimes(Lines* l) {
  return BitCount(l->prime, ArrayElementSize(l->prime) * BufLen(l->prime));
}

void LinesFilt(Lines* l, intmax_t* mask) {
  size_t j = 0;
  BufEachi(l->lineHi, i) {
    if (ArrayBit(mask, i)) {
      ArrayEachi(F(l)->fields, k) {
        // NOTE: this will not work on platforms where float is not representable as a 32-bit int
        // because we are casting onein to an int array
        F(l)->fields[k][j] = F(l)->fields[k][i];
      }
      if (ArrayBit(l->prime, i)) {
        ArrayBitSet(l->prime, j);
      } else {
        ArrayBitClear(l->prime, j);
      }
      ++j;
    }
  }
  ArrayEach(int*, F(l)->fields, x) {
    BufHdr(*x)->len = j;
  }
  BufHdr(l->prime)->len = ArrayBitElements(l->prime, j);
}

void BufIndexFreeInt(int** buf, intmax_t* indices) {
  int* result = 0;
  BufIndex(*buf, indices, &result);
  BufFree(buf);
  *buf = result;
}

void LinesIndex(Lines* l, intmax_t* indices) {
  ArrayEach(int*, F(l)->fields, x) {
    BufIndexFreeInt(x, indices);
  }
  uintmax_t* result = 0;
  BufIndexBit(l->prime, indices, &result);
  BufFree(&l->prime);
  l->prime = result;
}

#undef F

int LinesCatData(Lines* l, Map* data, size_t group, int tier) {
  Map* hi = MapGet(valueGroups[group], tier);
  if (!hi) {
    fprintf(stderr, "no data for tier %d\n", tier);
    return 0;
  }
  LineData* ld = MapGet(data, tier);
  if (ld) {
    size_t start = BufLen(l->lineHi);
    BufCat(&l->lineHi, ld->lineHi);
    BufCat(&l->lineLo, ld->lineLo);
    BufCat(&l->onein, ld->onein);

    // ANY line
    *BufAlloc(&l->lineHi) = ANY_HI;
    *BufAlloc(&l->lineLo) = ANY_LO;
    *BufAlloc(&l->onein) = 1;

    BufEachiRange(l->lineHi, start, -1, i) {
      int lineHi = l->lineHi[i];
      int lineLo = l->lineLo[i];
      Map* lo = MapGet(hi, lineHi);
      if (!lo || !MapHas(lo, lineLo)) {
        char* s = LineToStr(lineHi, lineLo, 1);
        fprintf(stderr, "no value for %s\n", s);
        BufFree(&s);
        return 0;
      }
      // int value = valueGroups[group][tier][lineHi][lineLo]
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
  WantStackPop(*pstack, BufLen(*pstack));
  BufFree(pstack);
}

#include "debug.c"

void LinesMatch(Lines* l, int lineHiMask, int lineLoMask,
    intmax_t** pmatch, intmax_t** pmatchLo)
{
  BufClear(*pmatch);
  BufClear(*pmatchLo);
  BufMask(int, l->lineHi, *x & lineHiMask, pmatch);
  BufMask(int, l->lineLo, *x & lineLoMask, pmatchLo);
  BufAND(*pmatch, *pmatchLo);
}

int WantEval(Lines const* l, Want* wantBuf) {
  Want* stack = 0;
  int res = 0;

  // make a copy of the line data
  Lines combos = {0};
  LinesDup(&combos, l);

  // filter all lines that don't match these stats
  int lineHiMask = ANY_HI;
  int lineLoMask = ANY_LO;
  BufEach(Want, wantBuf, s) {
    if (s->type == WANT_STAT) {
      lineHiMask |= s->lineHi;
      lineLoMask |= s->lineLo;
    }
  }

  intmax_t* match = 0;
  intmax_t* matchLo = 0;

  LinesMatch(&combos, lineHiMask, lineLoMask, &match, &matchLo);
  LinesFilt(&combos, match);

  // generate combinations (array of indices)

#define P 0, -2
#define N 0, -1
#define NN -3, -1

  // TODO: handle different cubes
  BufStatic(intmax_t, ranges, P, N, N);

#undef P
#undef N

  size_t numPrimes = LinesNumPrimes(&combos);
  BufEach(intmax_t, ranges, x) {
    if (*x == -2) {
      // primes end
      *x = numPrimes - 1;
    } else if (*x == -3) {
      // non-primes start
      *x = numPrimes;
    } else {
      *x = BufI(combos.lineHi, *x);
    }
  }

  intmax_t* indices = BufCombos(ranges, BufLen(ranges) / 2);
  LinesIndex(&combos, indices);
  BufFree(&indices);

  // TODO: generate ANY line probability


  BufEach(Want, wantBuf, w) {
    switch (w->type) {
      case WANT_STAT:
        *BufAlloc(&stack) = *w;
        break;
      case WANT_OP: {
        intmax_t* result = 0;
        int opCount = w->opCount >= 0 ? w->opCount : BufLen(stack);

        BufEachRange(Want, stack, -opCount, -1, s) {
          switch (s->type) {
            case WANT_STAT: {
              // make a mask of lines that match the stat
              LinesMatch(&combos, s->lineHi, s->lineLo, &match, &matchLo);

              // multiply all the values by the mask (non matching values will be 0)
              int* relevantValues = BufDup(combos.value);
              BufEachi(relevantValues, i) {
                relevantValues[i] *= ArrayBitVal(match, i);
              }

              // sum every 3 elements (repeat sum 3 times in the array to match size)
              BufEach(int, relevantValues, x) {
                x[0] = x[1] = x[2] = x[0] + x[1] + x[2];
                x += 2;
              }

              // make mask of elements in this sum array that are >= desired value
              BufClear(match);
              BufMask(int, relevantValues, *x >= s->value, &match);
              BufFree(&relevantValues);

              // remember to copy match as it gets reused
              s->type = WANT_MASK;
              s->mask = BufDup(match);

              // fall through to the MASK case
            }
            case WANT_MASK:
              if (!result) {
                result = s->mask;
                s->mask = 0; // prevent result from being freed
                break;
              }
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
        WantStackPop(stack, opCount);
        *BufAlloc(&stack) = (Want){
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

  if (BufLen(stack) > 1) {
    fprintf(stderr, "%zu values on the stack, expected 1\n", BufLen(stack));
#ifdef CUBECALC_DEBUG
    puts("");
    puts("# final stack");
    WantPrint(stack);
    puts("");
#endif
    goto cleanup;
  }

  int typ = stack[0].type;
  if (typ != WANT_MASK) {
    fprintf(stderr, "expected WANT_MASK result, got %s\n", WantTypeNames[typ]);
    goto cleanup;
  }

  if (!stack[0].mask) {
    fprintf(stderr, "NULL line filter mask\n");
    goto cleanup;
  }

  res = 1;

  LinesFilt(&combos, stack[0].mask);
#ifdef CUBECALC_DEBUG
  puts("");
  puts("# combos");
  LinesPrint(&combos, 3);
  printf("%zu total combos\n", BufLen(combos.lineHi) / 3);
#endif

cleanup:
  BufFree(&match);
  BufFree(&matchLo);
  LinesFree(&combos);
  WantStackFree(&stack);
  return res;
}

double CubeCalc(Want* wantBuf, int category, int cube, int tier, int lvl, int region, Map* data) {
  double res = 0;

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
  size_t numPrimes = LinesNumPrimes(&l);
  puts("# prime");
  DataPrint(data, tier, l.value);
  puts("");
  puts("# nonprime");
  DataPrint(data, tier - 1, l.value + numPrimes);
#endif

  if (!WantEval(&l, wantBuf)) {
    goto cleanup;
  }

cleanup:
  LinesFree(&l);

  return res;
}

#define _WantStatLine(line) .lineLo = line##_LO, .lineHi = line##_HI
#define WantStat(line, val) (Want){ .type = WANT_STAT, _WantStatLine(line), .value = val }
#define Line(x) x##_LO, x##_HI
#define WantOp(opname, n) (Want){ .type = WANT_OP, .op = WANT_##opname, .opCount = (n) }

int main() {
  cubecalcGeneratedGlobalInit();

  Map* data = DataFind(FACE_EYE_RING_EARRING_PENDANT, RED);
  if (!data) {
    fprintf(stderr, "line data not found\n");
    goto cleanup;
  }

  BufStatic(Want, want,
    WantStat(MESO, 20),
    WantStat(DROP, 20),
    WantOp(OR, 2),
    WantStat(STAT, 10),
    WantOp(AND, 2),
    WantStat(STAT, 23),
    WantOp(OR, 2),
  );

  double p = CubeCalc(want, FACE_EYE_RING_EARRING_PENDANT, RED, LEGENDARY, 160, GMS, data);
  puts("");
  if (p > 0) {
    printf("1 in %d\n", (int)round(1/p));
  } else {
    puts("impossible");
  }

cleanup:
  cubecalcGeneratedGlobalFree();
  return 0;
}
