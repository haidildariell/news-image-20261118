"""THE WORLD TODAY - front page for Wednesday 18 November 2026.

Draws a newspaper front page summing up the day's world news as a
1024x1024 PNG, using only the Python standard library. Everything is
drawn in code: a small embedded 5x7 bitmap font, simple pictograms,
and a hand-rolled PNG encoder (zlib + struct). No network, no clock,
no randomness: two runs write byte-identical files.

Usage: MAKEFUN_OUTPUT_DIR=<dir> python3 main.py
Writes <dir>/entry.png (default /output/entry.png).
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, '#' = ink, '.' = paper. Written for this entry.
FONT = {
    "A": (".###.",
          "#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    "B": ("####.",
          "#...#",
          "#...#",
          "####.",
          "#...#",
          "#...#",
          "####."),
    "C": (".####",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          ".####"),
    "D": ("####.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "####."),
    "E": ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#####"),
    "F": ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#...."),
    "G": (".####",
          "#....",
          "#....",
          "#.###",
          "#...#",
          "#...#",
          ".###."),
    "H": ("#...#",
          "#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    "I": ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "#####"),
    "J": ("..###",
          "...#.",
          "...#.",
          "...#.",
          "...#.",
          "#..#.",
          ".##.."),
    "K": ("#...#",
          "#..#.",
          "#.#..",
          "##...",
          "#.#..",
          "#..#.",
          "#...#"),
    "L": ("#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#####"),
    "M": ("#...#",
          "##.##",
          "#.#.#",
          "#.#.#",
          "#...#",
          "#...#",
          "#...#"),
    "N": ("#...#",
          "##..#",
          "##..#",
          "#.#.#",
          "#..##",
          "#..##",
          "#...#"),
    "O": (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    "P": ("####.",
          "#...#",
          "#...#",
          "####.",
          "#....",
          "#....",
          "#...."),
    "Q": (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#..#.",
          ".##.#"),
    "R": ("####.",
          "#...#",
          "#...#",
          "####.",
          "#.#..",
          "#..#.",
          "#...#"),
    "S": (".####",
          "#....",
          "#....",
          ".###.",
          "....#",
          "....#",
          "####."),
    "T": ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    "U": ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    "V": ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".#.#.",
          "..#.."),
    "W": ("#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#.#.#",
          "##.##",
          "#...#"),
    "X": ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          ".#.#.",
          "#...#",
          "#...#"),
    "Y": ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    "Z": ("#####",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#....",
          "#####"),
}

FONT.update({
    "0": (".###.",
          "#..##",
          "#.#.#",
          "##..#",
          "#...#",
          "#...#",
          ".###."),
    "1": ("..#..",
          ".##..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".###."),
    "2": (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#####"),
    "3": ("####.",
          "....#",
          "....#",
          ".###.",
          "....#",
          "....#",
          "####."),
    "4": ("...#.",
          "..##.",
          ".#.#.",
          "#..#.",
          "#####",
          "...#.",
          "...#."),
    "5": ("#####",
          "#....",
          "####.",
          "....#",
          "....#",
          "#...#",
          ".###."),
    "6": (".###.",
          "#....",
          "#....",
          "####.",
          "#...#",
          "#...#",
          ".###."),
    "7": ("#####",
          "....#",
          "...#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    "8": (".###.",
          "#...#",
          "#...#",
          ".###.",
          "#...#",
          "#...#",
          ".###."),
    "9": (".###.",
          "#...#",
          "#...#",
          ".####",
          "....#",
          "....#",
          ".###."),
    " ": (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".....",
          "....."),
    ".": (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".##..",
          ".##.."),
    ",": (".....",
          ".....",
          ".....",
          ".....",
          ".##..",
          ".##..",
          ".#..."),
    ":": (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          "....."),
    ";": (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          ".#..."),
    "'": ("..#..",
          "..#..",
          "..#..",
          ".....",
          ".....",
          ".....",
          "....."),
    '"': (".#.#.",
          ".#.#.",
          ".#.#.",
          ".....",
          ".....",
          ".....",
          "....."),
    "-": (".....",
          ".....",
          ".....",
          ".###.",
          ".....",
          ".....",
          "....."),
    "(": ("...##",
          "..#..",
          ".#...",
          ".#...",
          ".#...",
          "..#..",
          "...##"),
    ")": ("##...",
          "..#..",
          "...#.",
          "...#.",
          "...#.",
          "..#..",
          "##..."),
    "/": ("....#",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#....",
          "#...."),
    "&": (".##..",
          "#..#.",
          "#.#..",
          ".#...",
          "#.#.#",
          "#..#.",
          ".##.#"),
    "%": ("##..#",
          "##.#.",
          "...#.",
          "..#..",
          ".#...",
          "#.##.",
          "#..##"),
    "+": (".....",
          "..#..",
          "..#..",
          "#####",
          "..#..",
          "..#..",
          "....."),
    "=": (".....",
          ".....",
          ".###.",
          ".....",
          ".###.",
          ".....",
          "....."),
    "?": (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".....",
          "..#.."),
    "!": ("..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".....",
          "..#.."),
})

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 58, 95)
GRAY = (96, 90, 78)
RULE = (196, 187, 165)


class Canvas:
    def __init__(self, w=W, h=H, bg=PAPER):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.px), 3):
            self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        for t in range(thick):
            for xx in range(x, x + w):
                self.set(xx, y + t, color)

    def vline(self, x, y, h, color, thick=1):
        for t in range(thick):
            for yy in range(y, y + h):
                self.set(x + t, yy, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        # Bresenham
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for t in range(thick):
                self.set(x0 + t, y0, color)
                self.set(x0, y0 + t, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, thick=1):
        x, y, d = 0, r, 3 - 2 * r
        while x <= y:
            for px, py in ((cx + x, cy + y), (cx - x, cy + y),
                           (cx + x, cy - y), (cx - x, cy - y),
                           (cx + y, cy + x), (cx - y, cy + x),
                           (cx + y, cy - x), (cx - y, cy - x)):
                for t in range(thick):
                    self.set(px + t, py, color)
                    self.set(px, py + t, color)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def ellipse(self, cx, cy, rx, ry, color):
        # outline by parametric sampling
        import math
        steps = max(48, int(2 * math.pi * max(rx, ry)))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.set(int(cx + rx * math.cos(a)), int(cy + ry * math.sin(a)), color)

    def arc(self, cx, cy, r, a0, a1, color):
        import math
        steps = max(8, int(abs(a1 - a0) * r))
        for i in range(steps + 1):
            a = a0 + (a1 - a0) * i / steps
            self.set(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), color)


def text_width(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def draw_text(cv, x, y, s, scale, color):
    """Draw uppercase-friendly text; unknown chars become spaces."""
    s = s.upper()  # the embedded font covers capitals, digits, punctuation
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "#":
                    cv.fill_rect(cx + gx * scale, y + gy * scale,
                                 scale, scale, color)
        cx += 6 * scale
    return cx


def draw_centered(cv, y, s, scale, color):
    draw_text(cv, (W - text_width(s, scale)) // 2, y, s, scale, color)


# ------------------------------------------------------------ pictograms
# Each draws inside a 64x64 box whose top-left is (x, y). Ink only.

def pic_globe(cv, x, y):
    cx, cy = x + 32, y + 32
    cv.circle(cx, cy, 28, INK, 2)
    cv.ellipse(cx, cy, 28, 11, INK)
    cv.ellipse(cx, cy, 11, 28, INK)
    cv.hline(cx - 27, cy, 54, INK)
    cv.line(cx - 20, cy - 20, cx + 20, cy - 20, INK)
    cv.line(cx - 20, cy + 20, cx + 20, cy + 20, INK)


def pic_bridge(cv, x, y):
    # two towers, deck, suspension cables, water
    cv.hline(x + 4, y + 34, 56, INK, 3)
    for tx in (x + 14, x + 46):
        cv.vline(tx, y + 10, 26, INK, 3)
        cv.hline(tx - 2, y + 8, 7, INK, 3)
    cv.line(x + 4, y + 34, x + 15, y + 10, INK, 2)
    cv.line(x + 60, y + 34, x + 47, y + 10, INK, 2)
    cv.line(x + 15, y + 10, x + 32, y + 30, INK, 2)
    cv.line(x + 47, y + 10, x + 32, y + 30, INK, 2)
    cv.line(x + 8, y + 46, x + 56, y + 46, BLUE, 2)
    cv.line(x + 14, y + 52, x + 50, y + 52, BLUE, 2)


def pic_tanker(cv, x, y):
    # hull, containers, waves
    cv.line(x + 8, y + 34, x + 56, y + 34, INK, 3)
    cv.line(x + 8, y + 34, x + 14, y + 46, INK, 3)
    cv.line(x + 56, y + 34, x + 50, y + 46, INK, 3)
    cv.hline(x + 14, y + 46, 36, INK, 3)
    for i, cx in enumerate((x + 12, x + 26, x + 40)):
        cv.fill_rect(cx, y + 20, 12, 12, RED if i == 1 else BLUE)
    cv.fill_rect(x + 52, y + 24, 4, 10, INK)
    cv.line(x + 4, y + 54, x + 60, y + 54, BLUE, 2)
    cv.line(x + 10, y + 59, x + 54, y + 59, BLUE, 2)


def pic_parliament(cv, x, y):
    # dome, columns, steps
    cv.line(x + 32, y + 6, x + 14, y + 20, INK, 2)
    cv.line(x + 32, y + 6, x + 50, y + 20, INK, 2)
    cv.hline(x + 12, y + 20, 40, INK, 3)
    for cx in (x + 16, x + 27, x + 38, x + 49):
        cv.vline(cx, y + 23, 20, INK, 3)
    cv.hline(x + 10, y + 44, 44, INK, 3)
    cv.hline(x + 6, y + 50, 52, INK, 3)
    cv.hline(x + 2, y + 56, 60, INK, 3)


def pic_chip(cv, x, y):
    cv.fill_rect(x + 18, y + 18, 28, 28, INK)
    cv.fill_rect(x + 26, y + 26, 12, 12, PAPER)
    cv.fill_rect(x + 29, y + 29, 6, 6, RED)
    for i in range(3):
        px = x + 22 + i * 10
        cv.vline(px, y + 8, 10, INK, 3)
        cv.vline(px, y + 46, 10, INK, 3)
        py = y + 22 + i * 10
        cv.hline(x + 8, py, 10, INK, 3)
        cv.hline(x + 46, py, 10, INK, 3)


def pic_fence(cv, x, y):
    # closed border fence with gate cross
    for bx in range(x + 6, x + 60, 9):
        cv.vline(bx, y + 10, 34, INK, 3)
    cv.hline(x + 4, y + 14, 56, INK, 3)
    cv.hline(x + 4, y + 40, 56, INK, 3)
    cv.line(x + 10, y + 48, x + 54, y + 60, RED, 3)
    cv.line(x + 54, y + 48, x + 10, y + 60, RED, 3)


def pic_cricket(cv, x, y):
    # stumps, bat, ball
    for sx in (x + 12, x + 19, x + 26):
        cv.vline(sx, y + 30, 20, INK, 3)
    cv.hline(x + 12, y + 28, 17, INK, 2)
    cv.line(x + 40, y + 12, x + 52, y + 42, INK, 5)
    cv.line(x + 52, y + 42, x + 56, y + 52, INK, 3)
    cv.circle(x + 48, y + 16, 7, RED, 2)
    cv.hline(x + 6, y + 54, 52, INK, 2)


def pic_cyclone(cv, x, y):
    import math
    cx, cy = x + 32, y + 32
    for r, a0, a1 in ((26, 0.3, 5.2), (19, 2.2, 6.0),
                      (12, 4.0, 6.9), (6, 0.0, 5.5)):
        cv.arc(cx, cy, r, a0, a1, BLUE)
    cv.circle(cx, cy, 3, RED, 2)
    cv.line(x + 4, y + 58, x + 60, y + 58, GRAY, 2)


# ------------------------------------------------------------------- png
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        raw.extend(cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3])
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


# ---------------------------------------------------------------- layout
# (headline, deck lines, pictogram) for the seven stories below the lead.
STORIES = [
    ("UKRAINE HITS CRIMEA BRIDGE AGAIN",
     ["Second day of strikes on the bridge; Russia pounds",
      "Kyiv's bridges as new talks open with Europe and the US."],
     pic_bridge),
    ("TANKER SINKS IN STRAIT OF HORMUZ",
     ["Iran says a tanker carrying 2m barrels of oil sank;",
      "US hits Qeshm Island; IRGC claims a US drone downed;",
      "US national-security comms network reported down."],
     pic_tanker),
    ("ISRAEL ELECTS NEW SPEAKER",
     ["A Gadi Eisenkot ally wins the vote - a blow for",
      "Prime Minister Benjamin Netanyahu."],
     pic_parliament),
    ("NVIDIA BOARD BLOCKS HUANG RETURN",
     ["Trump backs Jensen Huang's return as Nvidia CEO;",
      "the board refuses to consider reinstatement."],
     pic_chip),
    ("ESTONIA TO CLOSE RUSSIA BORDER",
     ["Move follows a sabotage bid on a drone maker."],
     pic_fence),
    ("DHONI RETIRES FROM THE IPL",
     ["Becomes Chennai Super Kings mentor; Jay Shah",
      "re-elected ICC chairman."],
     pic_cricket),
    ("CYCLONE AKVAN GATHERS FORCE",
     ["Severe cyclonic storm likely by 19 Nov; Baidu chief",
      "warns of an AI bubble; Pope Leo hit by a rosary in Peru."],
     pic_cyclone),
]


def draw_page(cv):
    # --- masthead
    draw_centered(cv, 30, "THE WORLD TODAY", 6, INK)
    cv.hline(36, 88, W - 72, INK, 3)
    cv.hline(36, 94, W - 72, INK, 1)
    draw_centered(cv, 106, "WEDNESDAY, 18 NOVEMBER 2026", 2, RED)
    draw_centered(cv, 128, "ONE DAY IN THE WORLD - ALL THE NEWS THAT MATTERS",
                  2, GRAY)

    # --- lead story
    draw_text(cv, 36, 164, "LEAD STORY", 2, RED)
    draw_text(cv, 36, 190, "TRUMP IN MANILA FOR QUAD TALKS", 4, INK)
    draw_text(cv, 36, 224, "XI-TRUMP-PUTIN SUMMIT THURSDAY", 4, INK)
    draw_text(cv, 36, 264,
              "APEC leaders meet in Shenzhen 18-19 Nov ahead of Trump's China visit.",
              2, INK)
    draw_text(cv, 36, 284,
              "First-ever Xi-Trump-Putin three-way meeting set for Thursday 19 Nov.",
              2, INK)
    pic_globe(cv, 876, 168)
    cv.hline(36, 306, W - 72, INK, 2)

    # --- seven stories, one row each
    y = 322
    for headline, deck, pic in STORIES:
        pic(cv, 36, y + 8)
        cv.vline(112, y + 6, 76, RULE, 1)
        draw_text(cv, 128, y + 8, headline, 3, INK)
        dy = y + 38
        for line in deck:
            draw_text(cv, 128, dy, line, 2, (58, 54, 46))
            dy += 18
        y += 88
        if pic is not STORIES[-1][2]:
            cv.hline(128, y - 6, W - 128 - 36, RULE, 1)

    # --- footer
    cv.hline(36, 946, W - 72, INK, 2)
    draw_centered(cv, 962, "ALL EVENTS FIRST REPORTED ON WEDNESDAY 18 NOVEMBER 2026",
                  2, GRAY)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas()
    draw_page(cv)
    data = encode_png(cv)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
