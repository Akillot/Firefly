import time
import noise
import shutil

state = {
    "scale": 0.1,
    "speed": 0.005,
    "char": "░",
    "paused": False
}

def noise_to_color(val):
    norm = (val + 1) / 2
    purple_start = 90
    purple_range = 45
    color = int(purple_start + norm * purple_range)
    return color

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
    frame.append(" [P] Pause/Resume | [Q] Quit ")

    print("\033[H" + "\n".join(frame), end="")

print("\033[?25l", end="")
t = 0
try:
    while True:
        if not state["paused"]:
            render_frame(t)
            t += state["speed"]
        else:
            render_frame(t)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\033[?25h", end="")
    print("\n🌀 Firefly terminated.")
