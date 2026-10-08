#!/bin/bash
# Render a lesson at draft quality (480p30) in both looks and copy the videos + captions into the site:
# parchment for light mode (<slug>.mp4) and navy for dark mode (<slug>-dark.mp4), no border (Adder, 2026-10-02).
#   ./publish.sh 1.1 [-qh]            both looks
#   LOOKS=light ./publish.sh 1.1      just one (light or dark)
# Narration: Adder's own recording when it has been aligned (voice/aligned/UU-TT.beats.json, made by
# tools/transcribe_recording.py + tools/align_recording.py), otherwise the Kokoro placeholder voice.
# Force one with CALC_VOICE=adder or CALC_VOICE=am_michael.
set -e
NUM=$1; Q=${2:--ql --frame_rate 30}; SLUG=${NUM/./_}   # 480p30 drafts for now; final pass at 1080p+ later
cd "$(dirname "$0")"
REC=$(printf "%02d-%02d" "${NUM%%.*}" "${NUM##*.}")
if [ -z "$CALC_VOICE" ] && [ -f "../voice/aligned/$REC.beats.json" ]; then export CALC_VOICE=adder; fi
OUT=../web/static/video
mkdir -p $OUT
for LOOK in ${LOOKS:-light dark}; do
  case $LOOK in
    light) export CALC_THEME=parchment SUFFIX="" ;;
    dark)  export CALC_THEME=navy SUFFIX="-dark" ;;
    *) echo "unknown look $LOOK"; exit 1 ;;
  esac
  export CALC_BORDER=none
  export MEDIA=media/pub_${SLUG}_$LOOK      # one media dir per topic and look, so parallel renders don't share a LaTeX cache
  ./render.sh "s$SLUG.py" Lesson $Q > "$MEDIA.log" 2>&1 || { grep -E "Error|❱" "$MEDIA.log" | tail -5; exit 1; }
  DIR=$(ls -td $MEDIA/videos/s$SLUG/*/ | head -1)
  cp "$DIR/Lesson.mp4" "$OUT/$SLUG$SUFFIX.mp4"
  if [ "$CALC_VOICE" = adder ]; then
    # Adder's narration: captions are his actual words, placed on the video's clock (same timings in both looks)
    python3 ../tools/voice_captions.py "$MEDIA/voicemap_$SLUG.json" "$REC" "$OUT/$SLUG.vtt"
  else
    # manim writes SRT subtitles from the narration; browsers want WebVTT (same timings in both looks)
    { echo "WEBVTT"; echo; sed -E 's/([0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]{3})/\1.\2/g' "$DIR/Lesson.srt"; } > "$OUT/$SLUG.vtt"
    python3 ../tools/subtitle_math.py "$OUT/$SLUG.vtt"
  fi
  echo "published $OUT/$SLUG$SUFFIX.mp4 ($(du -h "$OUT/$SLUG$SUFFIX.mp4" | cut -f1))"
done
