#ifdef CUBECALC_DEBUG
void WantPrint(Want* wantBuf) {
  BufEach(Want, wantBuf, w) {
    switch (w->type) {
      case WANT_STAT: {
        char* line = LineToStr(w->lineHi, w->lineLo);
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

void LinesPrint(Lines* l) {
  BufEachi(l->lineHi, i) {

  }
}

typedef struct _Align {
  size_t maxlen;
  size_t* lens;
  char** ss;
} Align;

void AlignFeed(Align* al, char* alignFmt, char* fmt, ...) {
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

void AlignPrint(Align* al, FILE* f) {
  BufEachi(al->ss, i) {
    for (size_t x = 0; x < al->maxlen + 1 - al->lens[i]; ++x) putc(' ', f);
    fputs(al->ss[i], f);
    putc('\n', f);
  }
}

void AlignFree(Align* al) {
  BufFreeClear((void**)al->ss);
  BufFree(&al->ss);
  BufFree(&al->lens);
}

void DataPrint(Map* data, int tier, int* values) {
  LineData* ld = MapGet(data, tier);
  if (!ld) {
    puts("(null)");
    return;
  }
  Align al = {0};
  BufEachi(ld->lineHi, i) {
    char* s = LineToStr(ld->lineHi[i], ld->lineLo[i]);
#define FMT "%d %s 1"
    AlignFeed(&al, FMT, FMT " in %g", values[i], s, ld->onein[i]);
#undef FMT
    BufFree(&s);
  }
  AlignPrint(&al, stdout);
  AlignFree(&al);
}
#endif
