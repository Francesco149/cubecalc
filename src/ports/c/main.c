#include "cubecalc.c"
#include "generated.c"

#include <stdio.h>
#include <math.h>

int main() {
  CubeGlobalInit();

  printf("%s", disclaimer);

  const BufStatic(Want const, want,
    WantStat(ATT, 33),
    WantOp(AND, -1),
  );

  float p = CubeCalc(want, WEAPON, BONUS, LEGENDARY, 200, GMS);
  puts("");
  if (p > 0) {
    printf("1 in %d\n", (int)round(1/p));
  } else {
    puts("impossible");
  }

  CubeGlobalFree();
  return 0;
}
