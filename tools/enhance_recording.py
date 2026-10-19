"""Studio-clean one of Adder's edited lesson recordings with Resemble Enhance (removes room echo and noise).

    ~/opt/mamba/envs/enhance/bin/python tools/enhance_recording.py 01-01 [01-02 ...]

Reads voice/aligned/<UU-TT>.edited.wav and writes voice/aligned/<UU-TT>.edited.enhanced.wav, the same length, so
every beat timing in <UU-TT>.beats.json still holds. anim/style.py RecordedService plays the enhanced file when it
exists (and its narration cache keys on the file, so a re-publish picks it up).

Adder 2026-10-19 compared VoiceFixer and Resemble on a 30 s clip and picked Resemble Enhance at lambd 0.5 ("strong";
0.9 sounded overdone). Runs on CPU in the separate `enhance` env (torch CPU, resemble-enhance installed without its
pinned deps, a stand-in deepspeed module for its training-only imports, the model fetched from Hugging Face into the
package's model_repo since there is no git-lfs here). About 6 minutes of processing per minute of audio.
"""
import sys
from pathlib import Path

import soundfile as sf
import torch

import resemble_enhance.enhancer.inference as inf
from resemble_enhance.enhancer import download as dl

inf.download = lambda: dl.REPO_DIR / "enhancer_stage2"      # the model is already in model_repo (no git-lfs)

ROOT = Path(__file__).resolve().parent.parent
LAMBD, TAU, NFE = 0.5, 0.5, 64

for slug in sys.argv[1:]:
    src = ROOT / "voice" / "aligned" / f"{slug}.edited.wav"
    dest = src.with_name(f"{slug}.edited.enhanced.wav")
    wav, sr = sf.read(src, dtype="float32")
    dwav = torch.from_numpy(wav if wav.ndim == 1 else wav.mean(1))
    out, osr = inf.enhance(dwav, sr, "cpu", nfe=NFE, solver="midpoint", lambd=LAMBD, tau=TAU)
    sf.write(dest, out.numpy(), osr)
    print(f"{slug}: {len(wav) / sr:.1f} s in, {len(out) / osr:.1f} s out -> {dest.relative_to(ROOT)}", flush=True)
