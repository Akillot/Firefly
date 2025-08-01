import time
import noise
import shutil
import threading
import sys

state = {
    "scale": 0.1,
    "speed": 0.005,
    "char": "░",
    "paused": False,
    "running": True,
    "color_scheme": "purple"
}

color_schemes = {
    "purple": (90, 45),
    "blue": (27, 45),
    "red": (196, 30)
}

def noise_to_color(val):
    norm = (val + 1) / 2
    start, rng = color_schemes[state["color_scheme"]]
    return int(start + norm * rng)

def render_frame(time_step):
    width, height = shutil.get_terminal_size((80, 24))
    frame = []

    for y in range(height - 2):
        row = ""
        for x in range(width):
            val = noise.pnoise3(x * state["scale"], y * state["scale"], time_step)
            color_code = noise_to_color(val)
            row += f"\033[38;5;{color_code}m{state['char']}\033[0m"
        frame.append(row)

    frame.append("\033[0m" + "─" * width)
    frame.append(f" [P] Pause/Resume | [C] Color | [+/-] Speed | [Q] Quit | Current: {state['color_scheme'].capitalize()}, Speed: {state['speed']:.3f}, Command: \n")

    print("\033[H" + "\n".join(frame), end="")
    frame.append("\033[0m" + "─" * width)
def input_listener():
    while state["running"]:
        cmd = sys.stdin.read(1).lower()
        if cmd == "p":
            state["paused"] = not state["paused"]
        elif cmd == "c":
            schemes = list(color_schemes.keys())
            idx = schemes.index(state["color_scheme"])
            state["color_scheme"] = schemes[(idx + 1) % len(schemes)]
        elif cmd == "+":
            state["speed"] = min(state["speed"] + 0.001, 0.05)
        elif cmd == "-":
            state["speed"] = max(state["speed"] - 0.001, 0.001)
        elif cmd == "q":
            state["running"] = False
            break

print("\033[?25l", end="")
thread = threading.Thread(target=input_listener, daemon=True)
thread.start()

t = 0
try:
    while state["running"]:
        if not state["paused"]:
            render_frame(t)
            t += state["speed"]
        else:
            render_frame(t)
        time.sleep(0.05)
except KeyboardInterrupt:
    state["running"] = False
finally:
    print("\033[?25h", end="")
    print("\nFirefly terminated.")
