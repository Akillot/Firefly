import time
import noise

width, height = 80, 24
scale = 0.1
speed = 0.05
char = "░"

def noise_to_color(val):
    norm = (val + 1) / 2
    color = int(16 + norm * 215)
    return color

def clear():
    print("\033[H\033[J", end="")

def render_frame(time_step):
    for y in range(height):
        row = ""
        for x in range(width):
            val = noise.pnoise3(x * scale, y * scale, time_step)
            color_code = noise_to_color(val)
            row += f"\033[38;5;{color_code}m{char}\033[0m"
        print(row)

t = 0
try:
    while True:
        clear()
        render_frame(t)
        t += speed
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n🌀 Firefly terminated.")