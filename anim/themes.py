"""Video themes: a palette plus a painted background (paper, border, logo) for each look.

Pick one with the env var CALC_THEME (default "dark", the original look). For a paper theme, style.py swaps in the
palette and LessonScene paints `background(theme, w, h)` into the camera's background, so the paper, border and logo
sit behind every frame: scene code can't fade, move or zoom them away.

    CALC_THEME=parchment ./publish.sh 2.1
"""
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
LOGO = HERE.parent / "logo.png"
FONT = os.path.expanduser("~/opt/texlive/texmf-dist/fonts/opentype/public/tex-gyre/texgyrepagella-bold.otf")

# The color roles never change meaning between themes (blue = the function, gold = secant, red = tangent, ...);
# on paper they get darker, more saturated inks so they read on a light ground.
PALETTES = {
    "dark": dict(BG="#0E1216", INK="#ECE7DC", DIM="#7D8791", PANEL="#1A2128", FUNC="#58C4DD", SECANT="#FFD166",
                 TANGENT="#FF6B5A", AREA="#2EC4B6", ACCUM="#B39DDB", DERIV="#9CD96B"),
    # warm aged paper, sepia ink, a double rule border, logo bottom right
    # (inks darkened 2026-10-02 so every role is at least 5.5:1 against the paper)
    "parchment": dict(BG="#F1E6CC", INK="#1F150C", DIM="#5E4D37", PANEL="#E6D7B3", FUNC="#154A79", SECANT="#7E4F00",
                      TANGENT="#962419", AREA="#0F5E55", ACCUM="#4F347E", DERIV="#2C5F17"),
    # clean off-white graph paper, navy ink, a rounded slate frame, logo top right
    "graphpaper": dict(BG="#F8F6F0", INK="#1C2733", DIM="#7C8794", PANEL="#ECE8DE", FUNC="#1F6FB2", SECANT="#B9820A",
                       TANGENT="#CF4430", AREA="#178A80", ACCUM="#7A5BC2", DERIV="#2E8B45"),
    # a cream notebook page with faint rules and a red margin, charcoal ink, corner brackets, logo bottom left
    "notebook": dict(BG="#FBF7EC", INK="#262626", DIM="#7F7A70", PANEL="#F0EADB", FUNC="#22609E", SECANT="#B07A00",
                     TANGENT="#C23B2C", AREA="#1A857A", ACCUM="#74559F", DERIV="#3A7F2E"),
    # dark papers (2026-10-02): textured, never flat black; light inks warm or cool to suit the ground
    "darkparchment": dict(BG="#221C16", INK="#F2E8D5", DIM="#A8987F", PANEL="#2E261E", FUNC="#7FC8E8", SECANT="#F2C14E",
                          TANGENT="#F07F6A", AREA="#5CC9B6", ACCUM="#C3A9E6", DERIV="#A9D67C"),
    "slate": dict(BG="#1E2528", INK="#EEF0EC", DIM="#97A3A8", PANEL="#28323A", FUNC="#79C6E3", SECANT="#F5CF63",
                  TANGENT="#F48A72", AREA="#5ACBBE", ACCUM="#BDA7E8", DERIV="#A6DB82"),
    "navy": dict(BG="#141C2B", INK="#EDEAE2", DIM="#8C97AB", PANEL="#1D2738", FUNC="#7CC4F0", SECANT="#F3CB5A",
                 TANGENT="#F2846F", AREA="#57C7BA", ACCUM="#B9A4EC", DERIV="#A3D97E"),
}


def current():
    return os.environ.get("CALC_THEME", "dark")


def border():
    """Border style, env CALC_BORDER: none (Adder's pick, 2026-10-02), double (the first draft), rule (one thin line),
    deckle (darkened edges)."""
    return os.environ.get("CALC_BORDER", "none")


def palette(theme=None):
    return PALETTES[theme or current()]


def _rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def _noise(w, h, scale, seed):
    """Smooth value noise in [-1, 1]: random field at 1/scale resolution, upsampled and blurred."""
    rng = np.random.default_rng(seed)
    small = rng.random((max(2, h // scale), max(2, w // scale)))
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 3))
    return np.asarray(img, dtype=float) / 127.5 - 1


def _logo(height, ink, bg=None):
    """The Mr Oaks logo from logo.png, cropped to its ink. With `bg` (dark themes) it is inverted: the dark outline
    becomes `ink` and the cream fill becomes `bg`, so it reads as the same mark on dark paper. Until logo.png has
    content, a placeholder wordmark."""
    if LOGO.exists() and LOGO.stat().st_size > 0:
        im = Image.open(LOGO).convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())
        if bg is not None:
            a = np.asarray(im, dtype=float)
            lum = (a[..., :3] @ [0.299, 0.587, 0.114]) / 255                  # 0 = outline, 1 = fill
            rgb = _rgb(ink)[None, None, :] * (1 - lum[..., None]) + _rgb(bg)[None, None, :] * lum[..., None]
            im = Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), "RGBA")
        return im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
    font = ImageFont.truetype(FONT, int(height * 0.62))
    text = "Mr Oaks"
    box = font.getbbox(text)
    im = Image.new("RGBA", (box[2] - box[0] + 8, height), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - box[0], (height - (box[3] - box[1])) // 2 - box[1]), text, font=font, fill=tuple(int(c) for c in _rgb(ink)) + (200,))
    return im


def _paper(w, h, base, grain, blotch, vignette, seed=7):
    b = _rgb(base)
    tone = 1 + blotch * _noise(w, h, max(8, w // 6), seed) + grain * _noise(w, h, 2, seed + 1) + 0.5 * grain * _noise(w, h, 6, seed + 2)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    tone *= 1 - vignette * np.clip(r - 0.55, 0, None) ** 2
    img = np.clip(b[None, None, :] * tone[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(img, "RGB").convert("RGBA")


def background(theme, w, h):
    """The painted background for a paper theme at w x h pixels (cached in assets/)."""
    out = HERE / "assets" / f"bg_{theme}{'_' + border() if theme in ('parchment', 'darkparchment', 'slate', 'navy') else ''}_{w}x{h}.png"
    if out.exists() and out.stat().st_mtime > max(Path(__file__).stat().st_mtime, LOGO.stat().st_mtime if LOGO.exists() else 0):
        return str(out)
    p = PALETTES[theme]
    s = w / 1920                       # every size below is in 1080p pixels, scaled to the render
    if theme == "parchment":
        style = border()
        img = _paper(w, h, p["BG"], 0.025, 0.05, 0.45)
        d = ImageDraw.Draw(img)
        rule = tuple(int(c) for c in _rgb("#6B4E2E"))
        m = int(26 * s)
        m2 = m + int(12 * s)
        if style == "double":
            d.rectangle([m, m, w - m, h - m], outline=rule, width=max(2, int(5 * s)))
            d.rectangle([m2, m2, w - m2, h - m2], outline=rule, width=max(1, int(2 * s)))
            for cx, cy in ((m2, m2), (w - m2, m2), (m2, h - m2), (w - m2, h - m2)):      # small diamonds at the corners
                r = int(9 * s)
                d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=rule)
        elif style == "rule":
            d.rectangle([m2, m2, w - m2, h - m2], outline=rule, width=max(1, int(2 * s)))
        elif style == "deckle":
            # a burnt, uneven edge: darken a noisy band around the sides instead of drawing a line
            arr = np.asarray(img, dtype=float)
            yy, xx = np.mgrid[0:h, 0:w]
            edge = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)) / (26 * s)
            edge = edge + 0.35 * _noise(w, h, max(4, int(18 * s)), 11)
            burn = np.clip(1 - edge, 0, 1) ** 2
            arr[..., :3] *= (1 - 0.3 * burn)[..., None]
            img = Image.fromarray(arr.astype(np.uint8), "RGBA")
        logo = _logo(int(70 * s), p["INK"])
        img.alpha_composite(logo, (w - m2 - int(24 * s) - logo.width, h - m2 - int(18 * s) - logo.height))
    elif theme in ("darkparchment", "slate", "navy"):
        if theme == "darkparchment":
            img = _paper(w, h, p["BG"], 0.06, 0.12, 0.5)
            rule = tuple(int(c) for c in _rgb("#8A7354"))
        elif theme == "slate":
            img = _paper(w, h, p["BG"], 0.05, 0.10, 0.4)
            # faint chalk dust: soft light smudges here and there
            dust = np.clip(_noise(w, h, max(8, w // 5), 21), 0, None) ** 2 * 18 + np.clip(_noise(w, h, 3, 22), 0.7, None) * 8
            arr = np.asarray(img, dtype=float)
            arr[..., :3] += dust[..., None]
            img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
            rule = tuple(int(c) for c in _rgb("#56636B"))
        else:
            img = _paper(w, h, p["BG"], 0.07, 0.10, 0.5)
            rule = tuple(int(c) for c in _rgb("#4A5873"))
        d = ImageDraw.Draw(img)
        m = int(38 * s)
        if border() != "none":
            d.rectangle([m, m, w - m, h - m], outline=rule, width=max(1, int(2 * s)))
        logo = _logo(int(70 * s), p["INK"], bg=p["BG"])
        img.alpha_composite(logo, (w - m - int(24 * s) - logo.width, h - m - int(18 * s) - logo.height))
    elif theme == "graphpaper":
        img = _paper(w, h, p["BG"], 0.008, 0.012, 0.25)
        d = ImageDraw.Draw(img)
        grid, minor = tuple(int(c) for c in _rgb("#D9E3EE")), tuple(int(c) for c in _rgb("#E9EEF4"))
        step = int(48 * s)
        for x in range(0, w, step // 4):
            d.line([(x, 0), (x, h)], fill=grid if x % step == 0 else minor, width=1)
        for y in range(0, h, step // 4):
            d.line([(0, y), (w, y)], fill=grid if y % step == 0 else minor, width=1)
        m = int(28 * s)
        d.rounded_rectangle([m, m, w - m, h - m], radius=int(28 * s), outline=tuple(int(c) for c in _rgb("#4C5B6B")), width=max(2, int(4 * s)))
        logo = _logo(int(64 * s), p["INK"])
        plate = Image.new("RGBA", (logo.width + int(28 * s), logo.height + int(16 * s)), tuple(int(c) for c in _rgb(p["BG"])) + (255,))
        x0, y0 = w - m - int(30 * s) - plate.width, m + int(22 * s)
        img.alpha_composite(plate, (x0, y0))
        img.alpha_composite(logo, (x0 + int(14 * s), y0 + int(8 * s)))
    elif theme == "notebook":
        img = _paper(w, h, p["BG"], 0.012, 0.02, 0.35)
        d = ImageDraw.Draw(img)
        rule = tuple(int(c) for c in _rgb("#DDE6EF"))
        for y in range(int(150 * s), h - int(40 * s), int(54 * s)):
            d.line([(0, y), (w, y)], fill=rule, width=max(1, int(2 * s)))
        d.line([(int(150 * s), 0), (int(150 * s), h)], fill=tuple(int(c) for c in _rgb("#E7A8A0")), width=max(1, int(3 * s)))
        ink = tuple(int(c) for c in _rgb("#3A3A3A"))
        m, arm, wd = int(30 * s), int(80 * s), max(2, int(5 * s))
        for cx, cy, dx, dy in ((m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)):
            d.line([(cx, cy), (cx + dx * arm, cy)], fill=ink, width=wd)
            d.line([(cx, cy), (cx, cy + dy * arm)], fill=ink, width=wd)
        logo = _logo(int(64 * s), p["INK"])
        img.alpha_composite(logo, (int(150 * s) + int(24 * s), h - m - int(26 * s) - logo.height))
    else:
        raise ValueError(f"no painted background for theme {theme!r}")
    img.convert("RGB").save(out)
    return str(out)
