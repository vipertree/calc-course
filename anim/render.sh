#!/bin/bash
# Usage: ./render.sh <file.py> <Scene> [manim flags...]   e.g. ./render.sh s2_1.py Lesson -ql
ENV=$HOME/opt/mamba/envs/calc
cd "$(dirname "$0")"
export PATH=$HOME/opt/texlive/bin/x86_64-linux:$ENV/bin:$PATH
exec "$ENV/bin/python" -m manim --media_dir "${MEDIA:-media}" "${@:3}" "$1" "$2"
