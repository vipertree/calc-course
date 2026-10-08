#!/bin/bash
# Get one of Adder's lesson recordings ready for the videos:  tools/prepare_recording.sh 01-03
#   1. clean   voice/adder-lesson-recordings/01-03 -> cleaned/01-03.wav (denoise, loudness; nothing cut)
#   2. hear    word timings with Whisper -> voice/aligned/01-03.words.json
#   3. edit    bad takes out by reading the words ("Claude, scrap that ...") -> 01-03.edited.wav + 01-03.cuts.md
#   4. align   his words to the transcript's beats and lines -> 01-03.beats.json + 01-03.review.md
#              (beats he skipped are flagged as pickups; loud sounds muted between words are listed)
# Then ./anim/publish.sh 1.3 renders the lesson in his voice. Read cuts.md and review.md first.
set -e
REC=$1
cd "$(dirname "$0")/.."
export PATH=$HOME/opt/mamba/envs/calc/bin:$PATH
python tools/clean_lesson_audio.py --only "$REC"
python tools/transcribe_recording.py "$REC"
python tools/cut_retakes.py "$REC"
python tools/align_recording.py "$REC"
