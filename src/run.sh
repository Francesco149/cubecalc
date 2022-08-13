#!/bin/sh

d=$(dirname $(realpath "$0"))
"${d}/textfile.py" | tee "${d}/../cubechances.txt"
