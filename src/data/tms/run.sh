#!/bin/sh

. ../common.sh

scrape() {
  tmp="$1"
  htmlq --text '#lblTopicContent1 td' < "$tmp" > cache/tier_prime_rates.txt
  htmlq --text '#divContent td' < "$tmp" > cache/line_chances.txt
}

if ! [ -f cache/line_chances.txt ]; then
  tmp=$(mktemp /tmp/XXXXXX.html)
  curl -sL 'https://tw.beanfun.com/beanfuncommon/EventAD_Mobile/EventAD.aspx?EventADID=8421' \
    > "$tmp"
  scrape "$tmp"
  rm "$tmp"
fi

(
  header
  echo "import sys"
  echo "from datautils import percent"
  echo "from common import *"
  echo
  echo "event = {"
  ./process.py | sed 's/^/  /g'
  echo "}"
) | tee ../../tms.py
