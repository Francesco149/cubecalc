#!/bin/sh

flags="-std=c99 -Wall -lm"
buildflags="-O0 -DCUBECALC_DEBUG -D_FORTIFY_SOURCE=0"
units=compilation-units/monolith.c
cc=tcc
gen=false

for x in $@; do
  case "$x" in
    clang*)
      cc=clang
      ;;
    gcc*)
      cc=gcc
      ;;
    rel*)
      cc=clang
      buildflags="-O3 -flto -Werror"
      ;;
    san*)
      cc=clang
      buildflags="-Og -g -fsanitize=address,undefined,leak -DCUBECALC_DEBUG -Werror"
      ;;
    gen*)
      gen=true
      ;;

    # optionally build as separate compilation units to test that
    # they are not referencing each other in unintended ways.
    # monolith build is usually faster and lets the compiler optimize harder
    # on my machine, monolith build is ~12% faster
    unit*)
      units=compilation-units/*_impl.c
      units="$units main.c"
      ;;
  esac
done

if $gen; then
  echo
  echo "=== generating code"
  time ./gen.py > generated.c || exit
fi

echo
echo "=== compiling"
flags="$flags $buildflags"
echo "compiler: $cc"
echo "flags: $flags"

time mold -run $cc \
  -o cubecalc $units \
  $flags \
  || exit

echo
echo binary size: $(wc -c ./cubecalc)

echo
echo "=== running"
time env ASAN_OPTIONS=use_sigaltstack=false,symbolize=1 \
ASAN_SYMBOLIZER_PATH=$(which addr2line) \
./cubecalc
