#!/bin/sh

d=$(dirname $(realpath "$0"))

if [ "$1" = "scrape" ]; then
  echo "scraping probabilities data..."
  for x in "${d}/data/"*/; do
    pushd "$x"
    ./run.sh
    popd
  done
  echo "scraping complete"
fi

"${d}/textfile.py" | tee "${d}/../cubechances.txt"
