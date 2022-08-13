#!/bin/sh

red=5062009
meister=2711004
bonus=5062500

tier_names() {
  printf "RARE EPIC UNIQUE LEGENDARY"
}

tiers() {
  seq 1 4
}

get() {
  cfile="./cache/${1}_${2}_${3}_${4}.txt"
  if ! [ -f "$cfile" ]; then
    curl -sL 'https://maplestory.nexon.com/Guide/OtherProbability/cube/GetSearchProbList' \
      -X POST \
      -H 'X-Requested-With: XMLHttpRequest' \
      -F "nCubeItemID=${1}" \
      -F "nGrade=${2}" \
      -F "nPartsType=${3}" \
      -F "nReqLev=${4}" | htmlq --text .cube_data._1 td > "$cfile"
  fi
  cat "$cfile"
}

indent() {
  sed 's/^/  '/g
}

i() {
  item=$1
  name=$2
  equip_type=${3:-$name}
  level=${4:-150}
  cube=${CUBE:-$red}
  cube_name=${CUBENAME:-RED}
  if [ "$equip_type" = "FORCE_SHIELD_SOUL_RING" ] ||
     [ "$equip_type" = "EMBLEM" ]
  then
    level=100
  fi
  echo "$name: percent({"
  echo "  COMMON: [],"
  for x in $(tiers); do
    tier=$(tier_names | cut -d' ' -f$x)
    printf "$tier: "
    get $cube $x $item $level | ./process.py $cube_name $equip_type || exit
  done | indent
  echo "}),"
  echo
}

generate() {
  i 1  WEAPON
  i 2  EMBLEM
  i 3  SECONDARY
  i 4  FORCE_SHIELD_SOUL_RING
  i 6  HAT
  i 7  TOP_OVERALL
  i 9  BOTTOM
  i 10 SHOE
  i 11 GLOVE
  i 12 CAPE_BELT_SHOULDER
  i 15 FACE_EYE_RING_EARRING_PENDANT
  i 20 HEART_BADGE
}

(
  echo "import sys"
  echo "sys.path.append(\"../../\")"
  echo "from data.utils import percent"
  echo "from common import *"
  echo
  echo "# cash cubes (red, black)"
  echo "cash = {"
  generate | indent
  echo "}"
  echo
  echo "# non-cash cubes (occult/suspicious, master/yellow, meister/artisan/purple)"
  echo "noncash = {"
  CUBENAME=MEISTER CUBE=$meister generate | indent
  echo "}"
  echo
  echo "# bonus/additional potential"
  echo "bonus = {"
  CUBENAME=BONUS CUBE=$bonus generate | indent
  echo "}"
) | tee __init__.py
