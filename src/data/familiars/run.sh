#!/bin/sh

. ../common.sh

scrape() {
  tmp="$1"
  htmlq --text 'blockquote > .spoiler' < "$tmp" > cache/familiars.txt
}

if ! [ -f cache/familiars.txt ]; then
  tmp=$(mktemp /tmp/XXXXXX.html)
  curl -sL 'http://www.southperry.net/showthread.php?t=82643&p=1322876&viewfull=1#post1322876' \
    > "$tmp"
  scrape "$tmp"
  rm "$tmp"
fi

(
  header
  ./process.py
) | tee ../../familiars.py
