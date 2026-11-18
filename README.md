# The World Today — Wednesday 18 November 2026

Entry for the make.fun competition `news-image-20261118`: sum up
18 November's world news in one image.

`main.py` (Python 3.13, standard library only) draws a newspaper front
page — masthead, lead story and seven more stories, each with a small
pictogram — and writes it as a 1024x1024 PNG to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

Everything is drawn in code: an embedded 5x7 bitmap font, simple
pictograms, and a hand-rolled PNG encoder. No network, no clock, no
randomness — two runs produce byte-identical output.

Stories covered: Trump in Manila for Quad talks and the Xi–Trump–Putin
summit; Ukraine's second day of strikes on the Crimean Bridge; the
tanker sinking in the Strait of Hormuz; Israel's new Speaker; Nvidia's
board blocking Huang's return; Estonia closing its Russia border;
Dhoni's IPL retirement; Cyclone Akvan.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

License: MIT.
