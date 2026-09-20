#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from pathlib import Path

cache_dir = Path.home() / ".cache"
cache_dir.mkdir(exist_ok=True)
weather_file = cache_dir / "lockscreen_weather_cache.txt"
time_file = cache_dir / "lockscreen_weather_time.txt"

now = int(time.time())
need_refresh = True

if weather_file.exists() and time_file.exists():
    try:
        last_t = int(time_file.read_text().strip())
        if now - last_t < 900: # 15 min cache
            need_refresh = False
    except Exception:
        pass

if need_refresh:
    # Spawn background curl updater
    cmd = (
        f'W=$(curl -s --max-time 3 "wttr.in/?format=%c+%t+(%C)"); '
        f'if [ -n "$W" ] && [[ ! "$W" =~ "html" ]]; then '
        f'  echo "$W" | tr -d "+" | sed "s/  */ /g" > {weather_file}; '
        f'  echo {now} > {time_file}; '
        f'fi'
    )
    subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

weather_text = ""
if weather_file.exists():
    try:
        weather_text = weather_file.read_text().strip()
    except Exception:
        pass

bat_info = ""
bat_cap_path = Path("/sys/class/power_supply/BAT0/capacity")
bat_stat_path = Path("/sys/class/power_supply/BAT0/status")
if bat_cap_path.exists():
    try:
        cap = bat_cap_path.read_text().strip()
        stat = bat_stat_path.read_text().strip() if bat_stat_path.exists() else ""
        icon = "⚡" if stat == "Charging" else ("🔋" if int(cap) > 20 else "🪫")
        bat_info = f"{icon} {cap}%"
    except Exception:
        pass

parts = []
if weather_text:
    parts.append(weather_text)
if bat_info:
    parts.append(bat_info)

if parts:
    print("   •   ".join(parts))
else:
    print(time.strftime("%A, %d %B"))
