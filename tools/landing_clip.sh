#!/bin/bash
# The landing page's silent hero loop and its poster, cut from a lesson video.
#   tools/landing_clip.sh [video] [start] [end]     (defaults: 6.2's rectangles getting thinner)
# Adder 2026-10-12: start where the four rectangles are already drawn, so it moves as soon as the page opens.
# Re-run after 6.2 is re-rendered, and check the start/end against the new video (contact sheet: fps=2 tile).
set -e
cd "$(dirname "$0")/.."
SRC=${1:-web/static/video/6_2.mp4}; START=${2:-13.4}; END=${3:-19.5}
FF=$HOME/opt/mamba/envs/calc/bin/ffmpeg
OUT=web/static/img/landing
$FF -v error -y -ss "$START" -to "$END" -i "$SRC" -an -r 24 -c:v libx264 -preset slow -crf 30 -pix_fmt yuv420p -movflags +faststart $OUT/riemann-loop.mp4
$FF -v error -y -ss "$START" -i "$SRC" -frames:v 1 -c:v libwebp -quality 82 $OUT/riemann-poster.webp
ls -la $OUT/riemann-loop.mp4 $OUT/riemann-poster.webp
