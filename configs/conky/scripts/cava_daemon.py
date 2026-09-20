#!/usr/bin/env python3
"""
cava_daemon.py - Real-time Audio Spectrum Processor for Conky Desktop Widgets
Reads raw audio data from CAVA and writes Conky-formatted gradient bars to /tmp/cava_bars.txt
"""

import sys
import os
import time
import subprocess
import signal
import atexit

FIFO_PATH = "/tmp/cava_conky.fifo"
BARS_PATH = "/tmp/cava_bars.txt"
CONFIG_PATH = os.path.expanduser("~/.config/cava/config_conky")

BLOCKS = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

# Gradient Colors for Tokyo/Catppuccin/SciFi
COLORS = [
    "${color1}", "${color1}", "${color1}", "${color1}", "${color1}",
    "${color3}", "${color3}", "${color3}", "${color3}", "${color3}",
    "${color2}", "${color2}", "${color2}", "${color2}", "${color2}", "${color2}",
    "${color4}", "${color4}", "${color4}", "${color4}", "${color4}", "${color4}",
    "${color5}", "${color5}", "${color5}", "${color5}", "${color5}",
    "${color7}", "${color7}", "${color7}", "${color7}", "${color7}"
]

cava_proc = None

def cleanup():
    global cava_proc
    if cava_proc and cava_proc.poll() is None:
        try:
            cava_proc.terminate()
            cava_proc.wait(timeout=1)
        except Exception:
            pass
    if os.path.exists(FIFO_PATH):
        try:
            os.remove(FIFO_PATH)
        except Exception:
            pass
    if os.path.exists(BARS_PATH):
        try:
            with open(BARS_PATH, "w") as f:
                f.write("")
        except Exception:
            pass

atexit.register(cleanup)

def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def init_cava_config():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        f.write(f"""
[general]
framerate = 30
bars = 32
bar_width = 1
bar_spacing = 0

[input]
method = pulse
source = auto

[output]
method = raw
raw_target = {FIFO_PATH}
data_format = ascii
ascii_max_range = 8
bar_delimiter = 59
""")

def run_daemon():
    global cava_proc
    init_cava_config()

    if os.path.exists(FIFO_PATH):
        try:
            os.remove(FIFO_PATH)
        except Exception:
            pass
    
    os.mkfifo(FIFO_PATH)
    
    cava_bin = os.path.expanduser("~/.local/bin/cava")
    cava_proc = subprocess.Popen([cava_bin, "-p", CONFIG_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Open FIFO for reading
    with open(FIFO_PATH, "r") as fifo:
        while True:
            line = fifo.readline()
            if not line:
                time.sleep(0.05)
                continue
            
            raw_vals = line.strip().split(";")
            values = []
            for v in raw_vals:
                if v.isdigit():
                    values.append(int(v))
            
            if not values:
                continue
            
            # Format conky string with gradient colors
            out_parts = []
            cur_color = ""
            is_silent = all(v <= 0 for v in values)
            
            if is_silent:
                # Idle subtle wave
                formatted = "${color6}· · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·${font}"
            else:
                for idx, v in enumerate(values[:32]):
                    c = COLORS[idx] if idx < len(COLORS) else "${color1}"
                    if c != cur_color:
                        out_parts.append(c)
                        cur_color = c
                    clamped = min(max(v, 0), 8)
                    out_parts.append(BLOCKS[clamped])
                formatted = "".join(out_parts) + "${font}"
            
            # Write atomically to BARS_PATH
            tmp_target = BARS_PATH + ".tmp"
            with open(tmp_target, "w", encoding="utf-8") as f:
                f.write(formatted + "\n")
            os.replace(tmp_target, BARS_PATH)

if __name__ == "__main__":
    try:
        run_daemon()
    except KeyboardInterrupt:
        cleanup()
