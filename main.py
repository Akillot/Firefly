import time
import noise
import shutil

scale = 0.1
speed = 0.005
char = "░"

def noise_to_color(val):
    norm = (val + 1) / 2
    purple_start = 90
    purple_range = 45
    color = int(purple_start + norm * purple_range)
    return color

def render_frame(time_step):
    width, height = shutil.get_terminal_size((80, 24))
    frame = []
    for y in range(height):
        row = ""
        for x in range(width):
            val = noise.pnoise3(x * scale, y * scale, time_step)
            color_code = noise_to_color(val)
            row += f"\033[38;5;{color_code}m{char}\033[0m"
        frame.append(row)
    print("\033[H" + "\n".join(frame), end="")

print("\033[?25l", end="")
t = 0
try:
    while True:
        render_frame(t)
        t += speed
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\033[?25h", end="")
    print("\n🌀 Firefly terminated.")