#ifndef UTILS_H
#define UTILS_H

#include <stddef.h> // size_t
#include <limits.h>

#ifndef UTILS_NO_STDINT
#include <stdint.h> // intmax_t
#elif defined(LLONG_MAX)
typedef long long intmax_t;
#ifndef SIZE_MAX
#define SIZE_MAX LLONG_MAX
#endif
#else
typedef long intmax_t;
#ifndef SIZE_MAX
#define SIZE_MAX LONG_MAX
#endif
#endif

#ifndef UTILS_NO_STDINT
typedef intptr_t intmax_t; // TODO: more robust fallback
#endif

//
// Misc Macros
//

#define ArrayElementSize(array) sizeof((array)[0])
#define ArrayLength(array) (sizeof(array) / ArrayElementSize(array))
#define ArgsLength(type, ...) (sizeof((type[]){__VA_ARGS__}) / sizeof(type))
#define MemZero(p) memset(p, 0, sizeof(*p))
#define Min(a, b) ((a) < (b) ? (a) : (b))
#define Max(a, b) ((a) > (b) ? (a) : (b))
#define Clamp(x, lo, hi) Max(lo, Min(hi, x))

// this treats the int array as a bitmask (32bit per element for int) and checks if bit i is set
#define ArrayElementBitSize(array) (ArrayElementSize(array) << 3)
#define ArrayBitSlot(array, bit) (array)[bit / ArrayElementBitSize(array)]
#define ArrayBitMask(array, bit) (1 << (bit % ArrayElementBitSize(array)))
#define ArrayBit(array, bit)     (ArrayBitSlot(array, bit) & ArrayBitMask(array, bit))
#define ArrayBitSet(array, bit)   ArrayBitSlot(array, bit) |= ArrayBitMask(array, bit)
#define ArrayBitClear(array, bit) ArrayBitSlot(array, bit) &= ~ArrayBitMask(array, bit)

// these are for macros that define a list of things that will be passed to another macro
#define PREFIX
#define SUFFIX
#define StringifyComma(x) PREFIX #x SUFFIX,
#define AppendComma(x) PREFIX##x##SUFFIX,

//
// Allocator: can be passed to some utilities to use a custom allocator
//

typedef struct _Allocator {
  void* param;
  void* (* alloc)(void* param, size_t n);
  void* (* realloc)(void* param, void* p, size_t n);
  void (* free)(void* param, void* p);
} Allocator;

void* allocatorAlloc(Allocator const* allocator, size_t n);
void* allocatorRealloc(Allocator const* allocator, void* p, size_t n);
void allocatorFree(Allocator const* allocator, void* p);

// these versions do nothing without erroring if realloc/free are unavailable
void* allocatorTryRealloc(Allocator const* allocator, void* p, size_t n);
void allocatorTryFree(Allocator const* allocator, void* p);

extern Allocator const allocatorDefault_;
extern Allocator const allocatorNull_; // this allocator errors on any attempt to (re)alloc/free

// redefine this to change the default allocator for a block of code without passing it manually
#ifndef allocatorDefault
#define allocatorDefault allocatorDefault_
#endif

// use these when you don't want the allocator to allow realloc or free. if they are called
// an error is thrown and the program exits
void* noalloc(void* para, size_t n);
void* norealloc(void* para, void* p, size_t n);
void nofree(void* param, void* p);

//
// Buf: resizable array
//
// NOTE: when a function parameter is named pp, that means a _pointer to a buf_
//
//   int* buf = 0;
//   // BufAlloc and BufFree take a "pp" parameter because they can change the pointer
//   *BufAlloc(&buf) = 10;
//   *BufAlloc(&buf) = 20;
//   printf("%d\n", BufLen(buf)); // BufLen doesn't take a pp parameter so it's just the buf
//   BufFree(&buf);
//

// number of elements
#define BufLen(b) \
  ((b) ? BufHdr(b)->len : 0)

// fancy indexing. if i is negative, it will start from the end of the array (BufLen(b) - i)
// this is used by other functions that take indices
#define BufI(b, i) \
  ((i) < 0 ? (BufLen(b) + (i)) : (i))

// macro to fancy index
//
//   BufAt(x, -1) = 10;
//
#define BufAt(b, i) \
  ((b)[ BufI(b, i) ])

// remove element at fancy index i
void BufDel(void* b, intmax_t i);

// index of value (-1 if it can't be found)
int BufFindInt(int* b, int value);

// delete value if it can be found and return its index (-1 if it can't be found)
int BufDelFindInt(int* b, int value);

// empty without freeing memory
void BufClear(void* b);

// call free on every element of a buf of pointers, then empty it without freeing memory
void BufFreeClear(void** b);

// release memory. the buf pointer is also zeroed by this
void BufFree(void* pp);

// grows by count, reallocating as needed. length += count. pp can point to a null buf
// returns a pointer to the start of the new elements (fancy index -count)
#define BufReserve(pp, count) \
  (_BufAlloc((pp), (count), ArrayElementSize(*(pp)), &allocatorDefault), \
   &BufAt(*(pp), -(count)))

#define BufAlloc(pp) BufReserve(pp, 1)

// if you want to use a custom allocator, call this on the desired buf before anything else.
// count can be 0
#define BufReserveWithAllocator(pp, count, allocator) \
  (_BufAlloc((pp), (count), ArrayElementSize(*(pp)), allocator), \
   &BufAt(*(pp), -(count)))

// it's recommended to call this through macros like BufReserve and BufAlloc.
// see the description of BufReserve
void _BufAlloc(void* pp, size_t count, size_t elementSize, Allocator const* allocator);

#define BufZero(p) memset((p), 0, ArrayElementSize(p) * BufLen(p))
#define BufAllocZero(b) MemZero(BufAlloc(b))
#define BufReserveZero(pp, count) \
  (_BufAllocZero((pp), (count), ArrayElementSize(*(pp)), &allocatorDefault), \
   &BufAt(*(pp), -(count)))
void _BufAllocZero(void* pp, size_t count, size_t elementSize, Allocator const* allocator);

//
// shortcut to loop over every element
//
//   int* x = 0;
//   *BufAlloc(&x) = 10;
//   *BufAlloc(&x) = 20;
//   BufEach(int, x, pval) {
//     printf("%d\n", *pval);
//   }
//
#define BufEach(type, b, x) \
  if (b) for (type* x = b; x < b + BufLen(b); ++x)

//
// shortcut to loop over every index
//
//   int* x = 0;
//   *BufAlloc(&x) = 10;
//   *BufAlloc(&x) = 20;
//   BufEachi(x, i) {
//     printf("x[%zu] = %d\n", i, x[i]);
//   }
//
#define BufEachi(b, i) \
  for (size_t i = 0; i < BufLen(b); ++i)

// pp points to a buf of char pointers.
// malloc and format a string and append it to the buf.
// returns the formatted string (same pointer that will be appended to the buf).
char* BufAllocStrf(char*** pp, char* fmt, ...);

// append formatted string to a char buf. the buf is kept zero terminated
char* BufAllocCharsf(char** pp, char* fmt, ...);

// shallow copy
#define BufDup(p) _BufDup(p, &allocatorDefault)
void* _BufDup(void* p, Allocator const* allocator);

// returns a zero-terminated char buf containing a copy of len bytes at p
#define BufStrDupn(p, len) _BufStrDupn(p, len, &allocatorDefault)
char* _BufStrDupn(char* p, size_t len, Allocator const* allocator);

//returns a zero-terminated char buf containing a copy of null-terminated string p
#define BufStrDup(p) _BufStrDup(p, &allocatorDefault)
char* _BufStrDup(char* p, Allocator const* allocator);

// convert a Buf of structs to a Buf of pointers to the structs (no copying)
// this is useless normally, it's mainly for protobuf

#define BufToProto(protoStruc, member, b) \
  (protoStruc)->member = _BufToProto(b, &(protoStruc)->n_##member, &allocatorDefault)

void* _BufToProto(void* b, size_t *pn, Allocator const* allocator);

// declares a statically initialized buf with the given name.
#define BufStatic(type, name, ...) \
  BufStatic_(type, name, ArgsLength(type, __VA_ARGS__), __VA_ARGS__)

#define BufStatic_(type, name, n, ...) \
struct { \
  struct BufHdr hdr; \
  type data[n]; \
} name##Hdr = { \
  .hdr = (struct BufHdr){ \
    .allocator = &allocatorNull_, \
    .len = n, \
    .cap = n, \
    .elementSize = sizeof(type), \
  }, \
  .data = { __VA_ARGS__ }, \
}; type* const name = &name##Hdr.data[0]

// header internally used by Bufs. this is only exposed so that we can declare const/static Buf's
// must be aligned so that the data is also aligned (which is right after the header)
struct BufHdr {
  Allocator const* allocator;
  size_t len, cap, elementSize;
} __attribute__ ((aligned (8)));

#define BufHdr(b) ((struct BufHdr*)(b) - 1)

//
// Statistics
//

//
// convert a probability between 0.0 and 1.0 to a rounded integer representing the "one in" chance.
//
// example:
//   0.5 -> 2
//   0.45 -> 2
//   0.25 -> 4
//   0.3 -> 3
//   0.33 -> 3
//
intmax_t ProbToOneIn(double p);

//
// return the geometric quantile for p, in rounded "one in" form
//
// examples:
//   percent=75: the num of attempts to have 75% chance for an event of probability p to occur
//   percent=50: the median
//
intmax_t ProbToGeoDistrQuantileDingle(double p, double percent);

//
// Memory arena
//
// this allocator is inteded for cases when you will free all allocations at once and no resizing
// is needed. it does not support realloc or free (except for freeing the entire arena)
//

typedef struct _Arena Arena;

#define ArenaInit() _ArenaInit(&allocatorDefault)
Arena* _ArenaInit(Allocator const* allocator);
void* ArenaAlloc(Arena* a, size_t n);
void ArenaFree(Arena* a);
Allocator ArenaAllocator(Arena* a);

//
// Map
//
// map with integer keys. allocator only requires alloc until the map needs to be
// re-allocated, in which case free is also needed. if you use an allocator with no free, you can
// pre-allocate a larger map with MapInitCap. free+alloc happens when the number of values is half
// of cap
//

typedef struct _Map Map;

#define MapInit() _MapInit(&allocatorDefault)
#define MapInitCap(cap) _MapInitCap(&allocatorDefault, cap)
Map* _MapInit(Allocator const* allocator);
void MapFree(Map* m);

// returns 0 if key is missing. use MapHas to test for presence
void* MapGet(Map* m, int key);
int MapHas(Map* m, int key);

// delete a key and return the value it had
void MapDel(Map* m, int key);

// set a key, return non-zero when it succeeds. should only fail if out of memory or can't realloc
int MapSet(Map* m, int key, void* value);

// returns a Buf with all the keys
#define MapKeys(m) _MapKeys(m, &allocatorDefault)
int* _MapKeys(Map* m, Allocator const* allocator);

//
// Math
//

// fast log base 2 of a 32-bit integer
int Log2i(int n);

// round to the next higher power of 2
size_t RoundUp2(size_t v);

// hash functions
int HashInt(int x);

#endif

#if defined(UTILS_IMPLEMENTATION) && !defined(UTILS_UNIT)
#define UTILS_UNIT

#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>

//
// Allocator
//

void* allocatorAlloc(Allocator const* allocator, size_t n) {
  return allocator->alloc(allocator->param, n);
}

void* allocatorRealloc(Allocator const* allocator, void* p, size_t n) {
  return allocator->realloc(allocator->param, p, n);
}

void* allocatorTryRealloc(Allocator const* allocator, void* p, size_t n) {
  if (allocator->realloc == norealloc) {
    return 0;
  }
  return allocatorRealloc(allocator, p, n);
}

void allocatorTryFree(Allocator const* allocator, void* p) {
  if (allocator->free != nofree) {
    allocatorFree(allocator, p);
  }
}

void allocatorFree(Allocator const* allocator, void* p) {
  return allocator->free(allocator->param, p);
}

static void* xmalloc(void* param, size_t n) {
  void* res = malloc(n);
  if (!res) {
    perror("malloc");
  }
  return res;
}

static void* xrealloc(void* param, void* p, size_t n) {
  void* res = realloc(p, n);
  if (!res) {
    perror("realloc");
  }
  return res;
}

static void xfree(void* param, void* p) {
  free(p);
}

Allocator const allocatorDefault_ = {
  .param = 0,
  .alloc = xmalloc,
  .realloc = xrealloc,
  .free = xfree,
};

void* noalloc(void* para, size_t n) {
  fprintf(stderr, "noalloc(%p, %zu): this allocator does not support alloc\n", para, n);
  exit(1);
  return 0;
}

void* norealloc(void* para, void* p, size_t n) {
  fprintf(stderr, "norealloc(%p, %p, %zu): this allocator does not support realloc\n", para, p, n);
  exit(1);
  return 0;
}

void nofree(void* param, void* p) {
  fprintf(stderr, "nofree(%p, %p): this allocator does not support free\n", param, p);
  exit(1);
}

Allocator const allocatorNull_ = {
  .param = 0,
  .alloc = noalloc,
  .realloc = norealloc,
  .free = nofree,
};

#ifndef allocatorDefault
#define allocatorDefault allocatorDefault_
#endif

//
// Buf
//

void BufDel(void* b, intmax_t i) {
  if (b) {
    i = BufI(b, i);
    struct BufHdr* hdr = BufHdr(b);
    char* data = (char*)(hdr + 1);
    --hdr->len;
    memmove(&data[i * hdr->elementSize],
            &data[(i + 1) * hdr->elementSize],
            hdr->elementSize * (hdr->len - i));
  }
}

int BufFindInt(int* b, int value) {
  for (int i = 0; i < BufLen(b); ++i) {
    if (b[i] == value) {
      return i;
    }
  }
  return -1;
}

int BufDelFindInt(int* b, int value) {
  int i = BufFindInt(b, value);
  if (i >= 0) {
    BufDel(b, i);
  }
  return i;
}

void BufClear(void* b) {
  if (b) {
    BufHdr(b)->len = 0;
  }
}

void BufFreeClear(void** b) {
  if (b) {
    BufEach(void*, b, pp) {
      free(*pp);
    }
    BufClear(b);
  }
}

void BufFree(void *p) {
  void** b = p;
  if (*b) {
    free(BufHdr(*b));
    *b = 0;
  }
}

size_t RoundUp2(size_t v);

void _BufAlloc(void* p, size_t count, size_t elementSize, Allocator const* allocator) {
  size_t cap, len = 0;
  struct BufHdr* hdr = 0;
  void **b = p;
  if (*b) {
    hdr = BufHdr(*b);
    cap = hdr->cap;
    len = hdr->len;
  } else {
    size_t r = RoundUp2(count);
    // if count is small, we just default to 4, otherwise we do count / 2 because it get multiplied
    // by 2 later
    cap = r < 8 ? 4 : (r >> 1);
  }
  while (!hdr || len + count > cap) {
    cap <<= 1;
    size_t allocSize = sizeof(struct BufHdr) + elementSize * cap;
    if (hdr) {
      hdr = allocatorRealloc(hdr->allocator, hdr, allocSize);
    } else {
      hdr = allocatorAlloc(allocator, allocSize);
      hdr->allocator = allocator;
    }
    hdr->cap = cap;
    hdr->elementSize = elementSize;
    *b = hdr + 1;
  }
  hdr->len = len + count;
}

void _BufAllocZero(void* pp, size_t count, size_t elementSize, Allocator const* allocator) {
  char** b = pp;
  _BufAlloc(pp, count, elementSize, allocator);
  memset(*b + (BufLen(*b) - count) * elementSize, 0, count * elementSize);
}

void* _MemZero(void* p, size_t size) {
  memset(p, 0, size);
  return p;
}

char* BufAllocStrf(char*** b, char* fmt, ...) {
  va_list va;
  va_start(va, fmt);
  int n = vsnprintf(0, 0, fmt, va);
  va_end(va);
  int sz = n + 1;
  char* p = *BufAlloc(b) = malloc(sz);
  va_start(va, fmt);
  vsnprintf(p, sz, fmt, va);
  va_end(va);
  return p;
}

char* BufAllocCharsf(char** pp, char* fmt, ...) {
  va_list va;
  // remove null terminator if buf is not empty
  if (BufLen(*pp)) {
    --BufHdr(*pp)->len;
  }
  va_start(va, fmt);
  int n = vsnprintf(0, 0, fmt, va);
  va_end(va);
  int sz = n + 1;
  char* p = BufReserve(pp, sz);
  va_start(va, fmt);
  vsnprintf(p, sz, fmt, va);
  va_end(va);
  return p;
}

void* _BufDup(void* p, Allocator const* allocator) {
  if (!p) {
    return 0;
  }
  struct BufHdr* hdr = BufHdr(p);
  size_t cap = RoundUp2(hdr->len);
  size_t allocSize = sizeof(struct BufHdr) + hdr->elementSize * cap;
  struct BufHdr* copy = allocatorAlloc(allocator, allocSize);
  copy->allocator = allocator;
  copy->len = hdr->len;
  copy->cap = cap;
  copy->elementSize = hdr->elementSize;
  void* res = copy + 1;
  memcpy(res, p, hdr->len * hdr->elementSize);
  return res;
}

char* _BufStrDupn(char* p, size_t len, Allocator const* allocator) {
  char* res = 0;
  (void)BufReserveWithAllocator(&res, len + 1, allocator);
  memcpy(res, p, len);
  res[len] = 0;
  return res;
}

char* _BufStrDup(char* s, Allocator const* allocator) {
  return _BufStrDupn(s, strlen(s), allocator);
}

void* _BufToProto(void* b, size_t *pn, Allocator const* allocator) {
  if (!BufLen(b)) return 0;
  char* p = b;
  void** res = 0;
  struct BufHdr* hdr = BufHdr(b);
  *pn = hdr->len;
  (void)BufReserveWithAllocator(&res, hdr->len, allocator);
  BufEachi(b, i) {
    res[i] = p + i * hdr->elementSize;
  }
  return res;
}

//
// Statistics
//

intmax_t ProbToOneIn(double p) {
  if (p <= 0) return 0;
  return round(1 / p);
}

intmax_t ProbToGeoDistrQuantileDingle(double p, double percent) {
  if (p <= 0) return 0;
  return round(log(1 - percent / 100) / log(1 - p));
}

//
// Memory arena
//

struct _Arena {
  Allocator const* allocator;
  char** chunks;
  size_t align;
};

Arena* _ArenaInit(Allocator const* allocator) {
  Arena* a = allocatorAlloc(allocator, sizeof(Arena));
  a->allocator = allocator;
  a->chunks = 0;
  a->align = 4096;
  return a;
}

void* ArenaAlloc(Arena* a, size_t x) {
  // look for empty space in existing chunks
  BufEach(char*, a->chunks, chunk) {
    struct BufHdr* hdr = BufHdr(*chunk);
    if (hdr->cap - hdr->len >= x) {
      void* res = chunk + hdr->len;
      hdr->len += x;
      return res;
    }
  }
  // no space found, alloc a new chunk
  size_t n = a->align;
  x = (x + (n - 1)) & ~(n - 1); // round up to alignment
  char** pchunk = BufAllocZero(&a->chunks);
  (void)BufReserveWithAllocator(pchunk, x, a->allocator);
  return *pchunk;
}

void ArenaFree(Arena* a) {
  if (a) {
    BufEach(char*, a->chunks, chunk) {
      BufFree(chunk);
    }
    BufFree(&a->chunks);
  }
  allocatorTryFree(a->allocator, a);
}

static void* _ArenaAlloc(void* param, size_t x) {
  return ArenaAlloc(param, x);
}

Allocator ArenaAllocator(Arena* a) {
  return (Allocator){
    .param = a,
    .alloc = _ArenaAlloc,
    .realloc = norealloc,
    .free = nofree,
  };
}

//
// Map
//

struct _Map {
  Arena* arena;
  size_t cap, len;
  int* present; // bitmask. so that we can have zero keys/values that count as present
  int* keys;
  void** values;
};

static Map* MapRealloc(Allocator const* allocator, Map* m, size_t newCap) {
  Map* newMap = allocatorAlloc(allocator, sizeof(Map));
  Arena* arena = _ArenaInit(allocator);
  memset(newMap, 0, sizeof(*newMap));
  newMap->arena = arena;
  newMap->cap = newCap;
  newMap->keys = ArenaAlloc(arena, ArrayElementSize(newMap->keys) * newCap);
  newMap->values = ArenaAlloc(arena, ArrayElementSize(newMap->values) * newCap);
  size_t alignBits = ArrayElementBitSize(newMap->present) - 1;
  size_t bitCnt = (newCap + alignBits) & ~(alignBits);
  size_t elements = bitCnt / ArrayElementBitSize(newMap->present);
  size_t allocSize = elements * ArrayElementSize(newMap->present);
  newMap->present = ArenaAlloc(arena, allocSize);
  memset(newMap->present, 0, allocSize);
  if (m) {
    for (size_t i = 0; i < m->cap; ++i) {
      if (ArrayBit(m->present, i)) {
        MapSet(newMap, m->keys[i], m->values[i]);
      }
    }
  }
  return newMap;
}

#define MAP_BASE_CAP 16

Map* _MapInitCap(Allocator const* allocator, size_t cap) {
  cap = RoundUp2(cap);
  cap = Max(MAP_BASE_CAP, cap);
  return MapRealloc(allocator, 0, cap);
}

Map* _MapInit(Allocator const* allocator) {
  return _MapInitCap(allocator, MAP_BASE_CAP);
}

void MapFree(Map* m) {
  Allocator const* allocator = m->arena->allocator;
  ArenaFree(m->arena);
  allocatorFree(allocator, m);
}

static size_t MapNextIndex(size_t cap, size_t i) {
  return (i + 1) & (cap - 1); // cap should always be a power of two so we AND instead of %
}

#define MapScanEx(hash) \
  for (size_t i = MapNextIndex(m->cap, hash), j = 0; j < m->cap; ++j, i = MapNextIndex(m->cap, i))

#define MapScan MapScanEx(HashInt(key))

int* _MapKeys(Map* m, Allocator const* allocator) {
  int* res = 0;
  _BufAlloc(&res, 0, ArrayElementSize(res), allocator);
  for (size_t i = 0; i < m->cap; ++i) {
    if (ArrayBit(m->present, i)) {
      *BufAlloc(&res) = m->keys[i];
    }
  }
  return res;
}

static void** MapGetRef(Map* m, int key) {
  MapScan {
    if (ArrayBit(m->present, i) && m->keys[i] == key) {
      return &m->values[i];
    }
  }
  return 0;
}

int MapSet(Map* m, int key, void* value) {
  if (m->len * 2 >= m->cap) {
    // if the map is getting too full, reallocate it with twice the capacity
    Map* newMap = MapRealloc(m->arena->allocator, m, m->cap * 2);
    ArenaFree(m->arena);
    *m = *newMap;
    allocatorFree(newMap->arena->allocator, newMap);
  }

  // first, just see if the key is already there
  // we have to do this in case we remove a key that used to collide with this key
  void** ref = MapGetRef(m, key);
  if (ref) {
    *ref = value;
    return 1;
  }

  // key is missing
  // start scanning from MapNextIndex(hash), keep scanning forward (with wrap) until no more
  // collisions
  MapScan {
    if (!ArrayBit(m->present, i)) {
      m->keys[i] = key;
      m->values[i] = value;
      ArrayBitSet(m->present, i);
      ++m->len;
      return 1;
    }
  }

  return 0;
}

int MapHas(Map* m, int key) {
  return MapGetRef(m, key) != 0;
}

void* MapGet(Map* m, int key) {
  void** ref = MapGetRef(m, key);
  if (ref) {
    return *ref;
  }
  return 0;
}

void MapDel(Map* m, int key) {
  void** ref = MapGetRef(m, key);
  if (ref) {
    size_t i = ref - m->values;
    ArrayBitClear(m->present, i);
    --m->len;
  }
}


//
// Math
//

// https://stackoverflow.com/questions/11376288/fast-computing-of-log2-for-64-bit-integers
// https://graphics.stanford.edu/~seander/bithacks.html

int Log2i(int n) {
  const int tab32[32] = {
     0,  9,  1, 10, 13, 21,  2, 29,
    11, 14, 16, 18, 22, 25,  3, 30,
     8, 12, 20, 28, 15, 17, 24,  7,
    19, 27, 23,  6, 26,  5,  4, 31
  };
  n |= n >> 1;
  n |= n >> 2;
  n |= n >> 4;
  n |= n >> 8;
  n |= n >> 16;
  return tab32[(n * 0x07C4ACDD) >> 27];
}

size_t RoundUp2(size_t v) {
  --v;
  v |= v >> 1;
  v |= v >> 2;
  v |= v >> 4;
  v |= v >> 8;
#if SIZE_MAX > USHORT_MAX
  v |= v >> 16;
#endif
#if SIZE_MAX > UINT_MAX
  v |= v >> 32;
#endif
  return ++v;
}

int HashInt(int x) {
  x *= 0x85ebca6b;
  x ^= x >> 16;
  return x;
}
#endif
