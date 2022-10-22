#!/bin/sh

flags="-std=c11 -Wall -lm"
commonbuildflags="-fno-strict-aliasing"
buildflags="-O0 -D_FORTIFY_SOURCE=0"
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
      buildflags="-Og -g -fsanitize=address,undefined,leak -Werror"
      ;;
    gen*)
      gen=true
      ;;
    dbg*)
      flags="$flags -DCUBECALC_DEBUG"
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
flags="$flags $buildflags $commonbuildflags"
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
./cubecalc | tee cubechances.txt

# compare without percentages
(
  echo "" &&
  echo "### these are the differences from the reference python implementation ###" &&
  echo "### as long as the difference is tiny, it's probably just rounding     ###" &&
  echo "" &&
  echo "" &&
    diff \
      <(sed 's/, [0-9.%]\+$//g' < cubechances.txt) \
      <(sed 's/, [0-9.%]\+$//g' < ../../../cubechances.txt)
) | less
