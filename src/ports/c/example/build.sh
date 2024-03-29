#!/bin/sh

flags=""

for x in $@; do
  case "$x" in
    dbg*)
      flags="$flags -DCUBECALC_DEBUG -DCUBECALC_PRINTCOMBOS"
      ;;
  esac
done

tcc -std=c11 -Wall -lm -flto -Werror $flags main.c -o example &&
./example
