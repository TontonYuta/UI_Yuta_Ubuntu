#!/usr/bin/env python3
"""
helper.py - Dynamic greeting, media detector, and battery helpers for Conky
Using clean, universally supported text formatting (no broken emojis)
"""

import sys
import os
import time
import subprocess
import random
from datetime import datetime

QUOTES = [
    "Simplicity is the soul of efficiency.",
    "First, solve the problem. Then, write the code.",
    "Make it work, make it right, make it fast.",
    "Talk is cheap. Show me the code.",
    "Stay curious, stay hungry.",
    "Simplicity is prerequisite for reliability.",
    "Continuous improvement is better than delayed perfection.",
    "The best error message is the one that never shows up.",
    "Hành trình vạn dặm bắt đầu từ một bước chân.",
    "Kỷ luật là cầu nối giữa mục tiêu và thành tựu.",
    "Học tập không ngừng, sáng tạo không giới hạn.",
]

def get_greeting(lang="en", name="Yuta"):
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return f"Chào buổi sáng, {name}" if lang == "vi" else f"Good Morning, {name}"
    elif 12 <= hour < 18:
        return f"Chào buổi chiều, {name}" if lang == "vi" else f"Good Afternoon, {name}"
    elif 18 <= hour < 22:
        return f"Chào buổi tối, {name}" if lang == "vi" else f"Good Evening, {name}"
    else:
        return f"Chúc ngủ ngon, {name}" if lang == "vi" else f"Good Night, {name}"

def get_media_status():
    try:
        out = subprocess.check_output(['busctl', '--user', 'list'], stderr=subprocess.DEVNULL).decode()
        players = [line.split()[0] for line in out.splitlines() if 'org.mpris.MediaPlayer2' in line]
        if not players:
            return ""
        for target in players:
            status_raw = subprocess.check_output(['busctl', '--user', 'get-property', target, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'PlaybackStatus'], stderr=subprocess.DEVNULL).decode().strip()
            if 'Playing' in status_raw:
                meta_raw = subprocess.check_output(['busctl', '--user', 'get-property', target, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'Metadata'], stderr=subprocess.DEVNULL).decode()
                title = ''
                artist = ''
                for line in meta_raw.splitlines():
                    if 'xesam:title' in line:
                        parts = line.split('\"')
                        if len(parts) >= 2: title = parts[1]
                    elif 'xesam:artist' in line:
                        parts = line.split('\"')
                        if len(parts) >= 2: artist = parts[1]
                if title:
                    track = f"{title} - {artist}" if artist else title
                    if len(track) > 35:
                        track = track[:32] + "..."
                    return f">> {track}"
    except Exception:
        pass
    return ""

def get_battery_info():
    bat_path = "/sys/class/power_supply/BAT0"
    if not os.path.exists(bat_path):
        return "N/A"
    try:
        with open(os.path.join(bat_path, "capacity")) as f:
            cap = f.read().strip()
        with open(os.path.join(bat_path, "status")) as f:
            status = f.read().strip()
        tag = "[AC]" if status == "Charging" else ("[Full]" if status == "Full" else "[Bat]")
        return f"{tag} {cap}%"
    except Exception:
        return "N/A"

def get_quote():
    return f'"{random.choice(QUOTES)}"'

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "--greeting"
    name = sys.argv[2] if len(sys.argv) > 2 else "Yuta"
    
    if arg == "--greeting":
        print(get_greeting("vi", name))
    elif arg == "--greeting-en":
        print(get_greeting("en", name))
    elif arg == "--quote":
        print(get_quote())
    elif arg == "--media":
        media = get_media_status()
        print(media if media else get_quote())
    elif arg == "--battery":
        print(get_battery_info())
    else:
        print(get_greeting("en", name))

if __name__ == "__main__":
    main()
