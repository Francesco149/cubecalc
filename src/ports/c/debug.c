#include <stdio.h>

static
void WantPrint(Want const* wantBuf) {
  BufEach(Want const, wantBuf, w) {
    switch (w->type) {
      case WANT_STAT: {
        char* line = LineToStr(w->lineHi, w->lineLo, 0);
        printf("%d %s\n", w->value, line);
        BufFree(&line);
        break;
      }
      case WANT_OP:
        printf("<%s %d>\n", WantOpNames[w->op], w->opCount);
        break;
      case WANT_MASK:
      case WANT_NULLTYPE:
        puts(WantTypeNames[w->type]);
        break;
    }
  }
}

typedef struct _Align {
  size_t maxlen;
  size_t* lens;
  char** ss;
} Align;

#define AlignFeed(al, alignFmt, restFmt, ...) \
  _AlignFeed(al, alignFmt, alignFmt restFmt, __VA_ARGS__)
static
void _AlignFeed(Align* al, char* alignFmt, char* fmt, ...) {
  va_list va;
  va_start(va, fmt);
  size_t len = vsnprintf(0, 0, alignFmt, va);
  va_end(va);
  al->maxlen = Max(len, al->maxlen);
  *BufAlloc(&al->lens) = len;
  va_start(va, fmt);
  BufAllocVStrf(&al->ss, fmt, va);
  va_end(va);
}

static
void AlignPrint(Align* al, FILE* f) {
  BufEachi(al->ss, i) {
    Repeat(al->maxlen + 1 - al->lens[i]) putc(' ', f);
    fputs(al->ss[i], f);
    putc('\n', f);
  }
}

static
void AlignFree(Align* al) {
  BufFreeClear((void**)al->ss);
  BufFree(&al->ss);
  BufFree(&al->lens);
}

static
void DataPrint(LineData const* ld, int tier, int* values) {
  if (!ld) {
    puts("(null)");
    return;
  }
  Align al = {0};
  BufEachi(ld->lineHi, i) {
    char* s = LineToStr(ld->lineHi[i], ld->lineLo[i], 0);
    AlignFeed(&al, "%d %s 1", " in %g", values[i], s, ld->onein[i]);
    BufFree(&s);
  }
  AlignPrint(&al, stdout);
  AlignFree(&al);
}

static
void LinesPrint(Lines* l) {
  Align al = {0};
  BufEachi(l->lineHi, i) {
    char* s = LineToStr(l->lineHi[i], l->lineLo[i], 0);
    if (!(i % l->comboSize)) {
      AlignFeed(&al, "%s", "", "");
    }
    float p = l->onein[i];
    if (p < 1) {
      p = 1/p;
    }
    AlignFeed(&al, "%d %s %s 1", " in %g",
      l->value[i], s, ArrayBit(l->prime, i) ? "P" : " ", p);
    BufFree(&s);
  }
  AlignPrint(&al, stdout);
  AlignFree(&al);
}
