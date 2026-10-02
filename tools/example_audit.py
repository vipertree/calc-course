"""List the guided-notes examples that the lesson video doesn't solve yet.

Every example in the notes must also be worked in the video (Adder, 2026-10-01). A notes example is covered when it is a
VideoExample placeholder, which pulls its problem and solution from the scene's self.example(...) call. Anything still
typed as a plain Example in content/topic_*.py is listed here.

    ~/opt/mamba/envs/calc/bin/python tools/example_audit.py [2.1 2.2 ...]
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def topics(args):
    if args:
        return args
    nums = [p.stem[6:].replace("_", ".") for p in (ROOT / "content").glob("topic_*.py")]
    return sorted(nums, key=lambda n: tuple(int(k) for k in n.split(".")))


def main():
    total = 0
    for num in topics(sys.argv[1:]):
        t = importlib.import_module("content.topic_" + num.replace(".", "_")).TOPIC
        missing = t.notes_only_examples
        total += len(missing)
        if missing:
            print(f"{num:6} {len(missing)}  " + "; ".join(missing))
    print(f"\n{total} notes example(s) not yet in a video")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
