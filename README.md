<h1 align="center">Firefly</h1>

<p align="center">
  <strong>Real-time Perlin noise animation in your terminal.</strong>
</p>

<p align="center">
  <a href="https://github.com/Akillot/Firefly/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Akillot/Firefly?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.7+">
</p>

---

## What is this?

Firefly renders animated Perlin noise directly in the terminal using ANSI 256-color codes. It turns your terminal into a flowing, organic light show. No GUI, no dependencies beyond `noise`.

```
┌──────────────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░▓▓▓▓░░░░░░░░░░░▓▓░░░░░░░░░░▓▓▓░░░░░░░░░ │
│ ░░░▓▓▓▓▓▓▓▓░░░░░░░▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓░░░░░░░░ │
│ ░░░░▓▓▓▓▓░░░░░░░░░░▓▓▓░░░░░░░░▓▓▓▓▓░░░░░░░░░ │
│ ░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░░░░░▓▓░░░░░░░░░░ │
│──────────────────────────────────────────────│
│ [P] Pause  [C] Color  [+/-] Speed  [Q] Quit  │
└──────────────────────────────────────────────┘
```
*(Actual output is full-color and animated)*

## Features

- **3D Perlin noise** — smooth, organic patterns via `pnoise3` with time as Z-axis
- **3 color schemes** — purple, blue, red (cycle with `C`)
- **Interactive controls** — pause, speed adjustment, color switching, all in real-time
- **Adaptive rendering** — auto-detects terminal size, fills entire screen
- **Zero flicker** — cursor-addressed rendering via ANSI escape sequences

## Controls

| Key | Action |
|-----|--------|
| `P` | Pause / Resume |
| `C` | Cycle color scheme (purple → blue → red) |
| `+` | Increase speed (max 0.050) |
| `-` | Decrease speed (min 0.001) |
| `Q` | Quit |

## Quick Start

```bash
git clone https://github.com/Akillot/Firefly.git
cd Firefly
pip install noise
python main.py
```

## How it works

Each frame:
1. Sample `pnoise3(x * scale, y * scale, time_step)` for every terminal cell
2. Map noise value (−1..1) → ANSI 256 color index via scheme-specific offset + range
3. Render character (`░`) with `[38;5;{color}m` escape code
4. Print entire frame at cursor position `[H` — no screen clear, no flicker

The time dimension advances by `speed` each frame (default 0.005), creating smooth motion through 3D noise space.

## Configuration

Edit constants in `main.py`:

```python
state = {
    "scale": 0.1,      # noise zoom level (lower = larger patterns)
    "speed": 0.005,     # animation speed
    "char": "░",        # render character
}

color_schemes = {
    "purple": (90, 45),  # (start_color, range) in ANSI 256
    "blue": (27, 45),
    "red": (196, 30)
}
```

## Requirements

- Python 3.7+
- `noise` package
- Terminal with ANSI 256-color support

## License

[MIT](./LICENSE)

---

## AI Bootstrap Prompt

You are working on **Firefly** — a Python terminal animation that renders 3D Perlin noise as a full-screen ANSI 256-color animation.

**Stack:** Python 3.7+, `noise` package (only external dependency)
**Entry point:** `main.py` (single file)
**Run:** `pip install noise && python main.py`

**Non-obvious:**
- All config lives in two dicts at the top of `main.py`: `state` (scale, speed, char) and `color_schemes` (ANSI color offset + range per scheme) — no external config file
- Rendering works by printing to fixed cursor position `[H` every frame — no `clear()` call, which is why there is no flicker
- The Z-axis of `pnoise3` is the time dimension — incrementing it each frame creates smooth motion through 3D noise space
- Adding a new color scheme: add an entry to `color_schemes` as `(start_color, range)` in ANSI 256 space and wire it into the `C` key handler
