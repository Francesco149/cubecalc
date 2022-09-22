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
  RangeBefore(ArrayLength(allLinesHi), i) {
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

LineData const* DataFind(int categoryMask, int cubeMask, int tier) {
  LineData const* res = 0;
  Map* data = DataFindMap(cubeMask);
  int* cubes = MapKeys(data);
  BufEach(int, cubes, cube) {
    if (*cube & cubeMask) {
      Map* categoryMap = MapGet(data, *cube);
      int* categories = MapKeys(categoryMap);
      BufEach(int, categories, category) {
        if (*category & categoryMask) {
          Map* tiers = MapGet(categoryMap, *category);
          if (MapHas(tiers, tier)) {
            res = MapGet(tiers, tier);
            break;
          }
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
  intmax_t* prime;
  size_t comboSize;
} Lines;

typedef union _LineFields {
  Lines data;
  int* fields[offsetof(Lines, prime) / sizeof(void*)];
  int* allFields[offsetof(Lines, comboSize) / sizeof(void*)];
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

  // important: fill the rest of the bit mask with zeros so they dont get counted by NumPrimes
  for (; j % ArrayElementBitSize(l->prime); ++j) {
    ArrayBitClear(l->prime, j);
  }
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
  intmax_t* result = 0;
  BufIndexBit(l->prime, indices, &result);
  BufFree(&l->prime);
  l->prime = result;
}

#undef F

int LinesCatData(Lines* l, LineData const* ld, size_t group, int tier) {
  Map* hi = MapGet(valueGroups[group], tier);
  if (!hi) {
    fprintf(stderr, "no data for tier %d\n", tier);
    return 0;
  }
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

int LinesInit(Lines* l, LineData const* dataPrime, LineData const* dataNonPrime,
  size_t group, int tier)
{
  l->comboSize = 1;
  if (!LinesCatData(l, dataPrime, group, tier)) return 0;
  size_t numPrimes = BufLen(l->lineHi);
  if (!LinesCatData(l, dataNonPrime, group, tier - 1)) return 0;
  (void)BufReserve(&l->prime, ArrayBitElements(l->prime, BufLen(l->lineHi)));
  BufZero(l->prime);
  RangeBefore(numPrimes, i) {
    ArrayBitSet(l->prime, i);
  }
  return 1;
}

size_t valueGroupFind(int cubeMask, int categoryMask, int regionMask, int level) {
  int minLevel = 300;
  size_t match = valueGroupsLen;
  RangeBefore(valueGroupsLen, i) {
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

void LinesMatch(Lines* l, int lineHiMask, int lineLoMask, intmax_t** pmatch, intmax_t** pmatchLo) {
  lineHiMask |= ANY_HI;
  lineLoMask |= ANY_LO;
  BufClear(*pmatch);
  BufClear(*pmatchLo);
  BufMask(int, l->lineHi, *x & lineHiMask, pmatch);
  BufMask(int, l->lineLo, *x & lineLoMask, pmatchLo);
  BufAND(*pmatch, *pmatchLo);
}

int WantEval(int category, int cube, Lines* combos, Want const* wantBuf) {
  Want* stack = 0;
  int res = 0;

  // filter all lines that don't match these stats
  int lineHiMask = 0;
  int lineLoMask = 0;
  BufEach(Want const, wantBuf, s) {
    if (s->type == WANT_STAT) {
      lineHiMask |= s->lineHi;
      lineLoMask |= s->lineLo;
    }
  }

  intmax_t* match = 0;
  intmax_t* matchLo = 0;

  LinesMatch(combos, lineHiMask, lineLoMask, &match, &matchLo);
  LinesFilt(combos, match);

  size_t numPrimes = LinesNumPrimes(combos);

  // convert "one in" to probability (onein = 1/onein)
  BufEach(float, combos->onein, x) {
    *x = 1 / *x;
  }

  // calculate prime ANY line chance
  float otherLinesChance = 0;
  BufOpRange(+, combos->onein, 0, numPrimes - 2, &otherLinesChance);
  combos->onein[numPrimes - 1] = 1 - otherLinesChance;

  // calculate non-prime ANY line chance
  otherLinesChance = 0;
  BufOpRange(+, combos->onein, numPrimes, -2, &otherLinesChance);
  BufAt(combos->onein, -1) = 1 - otherLinesChance;

  // generate combinations (array of indices)

#define P 0, -2
#define N 0, -1
#define O -3, -1
// O is non-prime only

#define rangeIf(cond, ...) if (cond) { range(__VA_ARGS__); }
#define range(...) \
  static const BufStatic(intmax_t const, r, __VA_ARGS__); \
  ranges = BufDup((void*)r)

  intmax_t* ranges;

  rangeIf(cube & VIOLET, P, N, N, N, N, N)
  else rangeIf(cube & UNI, N)
  else rangeIf(cube & EQUALITY, P, P, P)
  else if (cube & (FAMILIAR | RED_FAM_CARD)) {
    // assuming no double primes on fam reveal (we don't know if this is accurate)
    rangeIf(category & FAMILIAR, P, O)
    else {
      range(P, N);
    }
  } else {
    range(P, N, N);
  }

#undef range
#undef rangeIf

#undef P
#undef N
#undef O

  BufEach(intmax_t, ranges, x) {
    if (*x == -2) {
      // primes end
      *x = numPrimes - 1;
    } else if (*x == -3) {
      // non-primes start
      *x = numPrimes;
    } else {
      *x = BufI(combos->lineHi, *x);
    }
  }

  // convert list of lines to flattened array of all possible line combinations
  combos->comboSize = BufLen(ranges) / 2;
  intmax_t* indices = BufCombos(ranges, combos->comboSize);
  LinesIndex(combos, indices);
  BufFree(&indices);
  BufFree(&ranges);

  BufEach(Want const, wantBuf, w) {
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
              LinesMatch(combos, s->lineHi, s->lineLo, &match, &matchLo);

              // multiply all the values by the mask (non matching values will be 0)
              int* relevantValues = BufDup(combos->value);
              BufEachi(relevantValues, i) {
                relevantValues[i] *= ArrayBitVal(match, i);
              }

              // sum every N elements (repeat sum N times in the array to match size)
              BufEachi(relevantValues, i) {
                int sum = 0;
                BufOpRange(+, relevantValues, i, i + combos->comboSize - 1, &sum);
                for (size_t j = 0; j < combos->comboSize; ++j) {
                  relevantValues[i + j] = sum;
                }
                i += combos->comboSize - 1;
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

  LinesFilt(combos, stack[0].mask);

cleanup:
  BufFree(&match);
  BufFree(&matchLo);
  WantStackFree(&stack);
  return res;
}

double CubeCalc(Want const* wantBuf, int category, int cube, int tier, int lvl, int region) {
  double res = 0;

  LineData const* dataPrime = DataFind(category, cube, tier);
  if (!dataPrime) {
    fprintf(stderr, "prime line data not found\n");
    goto cleanup;
  }

  LineData const* dataNonPrime = DataFind(category, cube, tier - 1);
  if (!dataNonPrime) {
    fprintf(stderr, "non-prime line data not found\n");
    goto cleanup;
  }

  size_t group = valueGroupFind(cube, category, region, lvl);
  if (group >= valueGroupsLen || !valueGroups[group]) {
    fprintf(stderr, "failed to find value group\n");
    return 0;
  }

  Lines combos = {0};
  if (!LinesInit(&combos, dataPrime, dataNonPrime, group, tier)) {
    goto cleanup;
  }

#ifdef CUBECALC_DEBUG
  size_t numPrimes = LinesNumPrimes(&combos);
  puts("# prime");
  DataPrint(dataPrime, tier, combos.value);
  puts("");
  puts("# nonprime");
  DataPrint(dataNonPrime, tier - 1, combos.value + numPrimes);
#endif

  if (!WantEval(category, cube, &combos, wantBuf)) {
    goto cleanup;
  }

  float const* primeChanceData;
  Container* primeChance = MapGet(primeChances, cube);
  switch (primeChance->type) {
    case CONTAINER_BUF: {
      primeChanceData = primeChance->data;
      break;
    }
    case CONTAINER_MAP: {
      primeChanceData = MapGet(primeChance->data, tier);
      break;
    }
    default:
      fprintf(stderr, "invalid prime chance container %d\n", primeChance->type);
      goto cleanup;
  }

  {
    size_t len = BufLen(primeChanceData);
    if (len != combos.comboSize) {
      fprintf(stderr, "expected %zu prime chances, got %zu\n", combos.comboSize, len);
      goto cleanup;
    }
  }

  // multiply line probabilities by prime chance
  // to make it branchless, we prepend the non-prime chances and then we mul the index by prime bit
  // example:
  //   multipliers = [1 - primeChance1, 1 - primeChance2, 1 - primeChance3,
  //                      primeChance1,     primeChance2,     primeChance3]
  //   index = (line % 3) + IsPrime * 3

  float* primeChanceBuf = 0;

  {
    float* primeMul = 0;
    BufReserve(&primeMul, combos.comboSize * 2);
    RangeBefore(combos.comboSize, i) {
      primeMul[i] = 1 - primeChanceData[i];
      primeMul[i + combos.comboSize] = primeChanceData[i];
    }

    size_t numLines = BufLen(combos.lineHi);
    BufReserve(&primeChanceBuf, numLines);
    RangeBefore(numLines, i) {
      size_t idx = (i % combos.comboSize) + ArrayBitVal(combos.prime, i) * combos.comboSize;
      primeChanceBuf[i] = primeMul[idx];
    }

    BufFree(&primeMul);
  }

  BufOp2(*, combos.onein, primeChanceBuf);
  BufFree(&primeChanceBuf);

#ifdef CUBECALC_DEBUG
  puts("");
  puts("# combos");
  LinesPrint(&combos);
  printf("%zu total combos\n", BufLen(combos.lineHi) / combos.comboSize);
#endif

  // calculate combo probabilities
  float* comboProbs = 0;
  BufEach(float, combos.onein, x) {
    float comboProb = 1;
    OpRange(*, x, 0, combos.comboSize - 1, &comboProb);
    *BufAlloc(&comboProbs) = comboProb;
    x += combos.comboSize - 1;
  }

  // calculate probability to roll any of the combos
  BufOp(+, comboProbs, &res);
  BufFree(&comboProbs);

cleanup:
  LinesFree(&combos);

  return res;
}

#define _WantStatLine(line) .lineLo = line##_LO, .lineHi = line##_HI
#define WantStat(line, val) (Want){ .type = WANT_STAT, _WantStatLine(line), .value = val }
#define Line(x) x##_LO, x##_HI
#define WantOp(opname, n) (Want){ .type = WANT_OP, .op = WANT_##opname, .opCount = (n) }

int main() {
  cubecalcGeneratedGlobalInit();

  /*
  BufStatic(Want, want,
    WantStat(MESO, 20),
    WantStat(DROP, 20),
    WantOp(OR, 2),
    WantStat(STAT, 10),
    WantOp(AND, 2),
    WantStat(STAT, 23),
    WantOp(OR, 2),
  );
  */

  // TODO: violet cube results are wrong
  // TODO: lvl 151+ doesn't find a match with bpot cubes

  const BufStatic(Want const, want,
    WantStat(ATT, 33),
    WantOp(AND, -1),
  );

  double p = CubeCalc(want, WEAPON, RED, LEGENDARY, 200, GMS);
  puts("");
  if (p > 0) {
    printf("1 in %d\n", (int)round(1/p));
  } else {
    puts("impossible");
  }

  cubecalcGeneratedGlobalFree();
  return 0;
}
