#!/bin/bash
# Render a lesson at draft quality (480p30) and copy video + captions into the site.
#   ./publish.sh 1.1 [-qh]
set -e
NUM=$1; Q=${2:--ql --frame_rate 30}; SLUG=${NUM/./_}   # 480p30 drafts for now; final pass at 1080p+ later
cd "$(dirname "$0")"
export MEDIA=media/pub_$SLUG          # one media dir per topic, so parallel renders don't share a LaTeX cache
./render.sh "s$SLUG.py" Lesson $Q > "$MEDIA.log" 2>&1 || { grep -E "Error|❱" "$MEDIA.log" | tail -5; exit 1; }
DIR=$(ls -td $MEDIA/videos/s$SLUG/*/ | head -1)
OUT=../web/static/video
mkdir -p $OUT
cp "$DIR/Lesson.mp4" "$OUT/$SLUG.mp4"
# manim writes SRT subtitles from the narration; browsers want WebVTT
{ echo "WEBVTT"; echo; sed -E 's/([0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]{3})/\1.\2/g' "$DIR/Lesson.srt"; } > "$OUT/$SLUG.vtt"
echo "published $OUT/$SLUG.mp4 ($(du -h "$OUT/$SLUG.mp4" | cut -f1))"
