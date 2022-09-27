#define CUBECALC_MONOLITH
#include "../cubecalc.c"

#include <stdio.h>
#include <math.h>

int main() {
  CubeGlobalInit();

  static const BufH(Want, want,
    WantStat(ATT, 33),
    WantOp(AND, -1),
  );

  float p = CubeCalc(want.data, WEAPON, BONUS, LEGENDARY, 200, GMS, 0);
  if (p > 0) {
    printf("1 in %.0f\n", round(1 / p));
  } else {
    puts("impossible");
  }

  CubeGlobalFree();
  return 0;
}
