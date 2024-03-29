#!/bin/sh

. ../common.sh

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
  cfile="./cache/${1}_${2}_${3}_${4}${SELECTOR}.txt"
  if ! [ -f "$cfile" ]; then
    curl -sL 'https://maplestory.nexon.com/Guide/OtherProbability/cube/GetSearchProbList' \
      -X POST \
      -H 'X-Requested-With: XMLHttpRequest' \
      -F "nCubeItemID=${1}" \
      -F "nGrade=${2}" \
      -F "nPartsType=${3}" \
      -F "nReqLev=${4}" | htmlq --text ${SELECTOR:-.cube_data._1} td > "$cfile"
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
  for x in $(tiers); do
    tier=$(tier_names | cut -d' ' -f$x)
    if [ $tier = "RARE" ]; then
      printf "COMMON: "
      # janky way to remove the rare lines since the site doesn't have an option to only
      # show common. this relies on the fact that the non-common lines are grouped together and
      # in the same order as in the rare column
      firstrare=$(get $cube $x $item $level | head -n 1)
      SELECTOR=.cube_data._2 get $cube $x $item $level |
        sed "/$firstrare/q" | head -n -1 |
        ./process.py $cube_name $equip_type || exit
    fi
    printf "$tier: "
    get $cube $x $item $level | ./process.py $cube_name $equip_type || exit
  done | indent
  echo "}),"
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
  header
  echo "cubes = {"
  (
    echo "CASH_MAIN: {"
    generate | indent
    echo "},"
    echo "NONCASH_MAIN: {"
    CUBENAME=MEISTER CUBE=$meister generate | indent
    echo "},"
    echo "BONUS: {"
    CUBENAME=BONUS CUBE=$bonus generate | indent
    echo "},"
  ) | indent
  echo "}"
) | tee ../../kms.py
