#!/bin/bash
# Teacher slide stills for one lesson, both looks: every beat's fullest frame and each worked example's posed problem
# and figure, as 1080p PNGs (kit.py, CALC_STILLS). Nothing is animated (-s), so it takes a minute or two, not a render.
#   ./stills.sh 2.1        -> ../build/stills/2_1/{light,dark}/*.png + stills.json
# Uses the published render's media dir, so its LaTeX and narration caches are reused and the timing matches.
set -e
NUM=$1; SLUG=${NUM/./_}
cd "$(dirname "$0")"
REC=$(printf "%02d-%02d" "${NUM%%.*}" "${NUM##*.}")
if [ -z "$CALC_VOICE" ] && [ -f "../voice/aligned/$REC.beats.json" ]; then export CALC_VOICE=adder; fi
for LOOK in ${LOOKS:-light dark}; do
  case $LOOK in
    light) export CALC_THEME=parchment ;;
    dark)  export CALC_THEME=navy ;;
    *) echo "unknown look $LOOK"; exit 1 ;;
  esac
  export CALC_BORDER=none MEDIA=media/pub_${SLUG}_$LOOK
  export CALC_STILLS=$(cd .. && pwd)/build/stills/$SLUG/$LOOK
  rm -rf "$CALC_STILLS"; mkdir -p "$CALC_STILLS"
  ./render.sh "s$SLUG.py" Lesson -qh -s > "$MEDIA.stills.log" 2>&1 || { grep -E "Error|❱" "$MEDIA.stills.log" | tail -5; exit 1; }
  echo "stills $NUM $LOOK: $(ls "$CALC_STILLS"/*.png | wc -l) images"
done
