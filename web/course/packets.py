"""Personalized topic packets (lesson + practice + AP test prep in one PDF).

build.py compiles one base packet per topic (build/pdf/<num>/<num>-packet-classic.pdf, plus a -key twin for
teachers). A student's download is that base with their name and a packet ID stamped in the footer of every page,
and the ID is recorded as an IssuedPacket, so a copy that turns up somewhere can be traced to who printed it.
Stamping is pymupdf only: no LaTeX on the server, and a download takes well under a second.
"""
import hashlib
import hmac
import secrets
import time

import pymupdf
from django.conf import settings

from .models import IssuedPacket

PDF_DIR = settings.BASE_DIR.parent / "build" / "pdf"
FONT = PDF_DIR / "fonts" / "LibertinusSans-Regular.otf"     # copied there by build.py; Helvetica if missing
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"            # no 0/O/1/I/L: easy to read off paper

# Page geometry from pdf/calc.sty: 0.7in side margins, 0.8in bottom margin, 30pt footskip (11pt article).
# The stamp shares the page number's baseline, left and right of it.
SIDE = 0.7 * 72
FOOT_BASELINE = 0.8 * 72 - 30          # up from the bottom edge
INK = (0.35, 0.35, 0.35)               # the "soft" gray of the printed header and footer
SIZE = 8.5


def base_path(num, key=False):
    return PDF_DIR / num / f"{num}-packet{'-key' if key else ''}-classic.pdf"


def available(num):
    return not num.startswith("U") and base_path(num).is_file()


def new_code(user, num):
    """8 characters derived from user id + topic + time (keyed with SECRET_KEY, salted so two downloads
    in the same instant differ), shown as XXXX-XXXX."""
    msg = f"{user.pk}:{num}:{time.time_ns()}:{secrets.token_hex(4)}".encode()
    n = int.from_bytes(hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).digest(), "big")
    chars = []
    for _ in range(8):
        n, r = divmod(n, len(CODE_ALPHABET))
        chars.append(CODE_ALPHABET[r])
    return "".join(chars[:4]) + "-" + "".join(chars[4:])


def issue(user, num):
    """Record a new packet for this user and topic and return it."""
    for _ in range(5):
        code = new_code(user, num)
        if not IssuedPacket.objects.filter(code=code).exists():
            return IssuedPacket.objects.create(user=user, topic=num, code=code)
    raise RuntimeError("could not find a free packet code")


def holder_name(user):
    p = getattr(user, "profile", None)
    name = (p.display_name if p is not None and p.display_name else user.get_username()).strip()
    return name if len(name) <= 48 else name[:47] + "…"


def _font():
    return pymupdf.Font(fontfile=str(FONT)) if FONT.is_file() else pymupdf.Font("helv")


def stamp(path, name, code, what="Packet"):
    """The PDF at path with '<what> printed for <name>' and '<what> ID <code>' on every page -> PDF bytes.
    Student packets say "Packet ..."; a teacher's handouts (what="") just say "Printed for <name>" and "ID <code>"."""
    doc = pymupdf.open(path)
    font = _font()
    left = f"{what} printed for {name}" if what else f"Printed for {name}"
    right = f"{what} ID {code}" if what else f"ID {code}"
    for page in doc:
        r = page.rect
        y = r.height - FOOT_BASELINE
        tw = pymupdf.TextWriter(r)
        tw.append((SIDE, y), left, font=font, fontsize=SIZE)
        tw.append((r.width - SIDE - font.text_length(right, fontsize=SIZE), y), right, font=font, fontsize=SIZE)
        tw.write_text(page, color=INK)
    meta = doc.metadata or {}
    doc.set_metadata({**{k: v for k, v in meta.items() if k in ("title", "author", "creator", "producer")},
                      "subject": f"{what or 'Handout'} {code}, printed for {name}", "keywords": f"packet {code}"})
    doc.subset_fonts()
    data = doc.tobytes(garbage=3, deflate=True)
    doc.close()
    return data
