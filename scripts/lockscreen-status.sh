#!/bin/bash
CACHE_FILE="$HOME/.cache/lockscreen_weather_cache.txt"
CACHE_TIME_FILE="$HOME/.cache/lockscreen_weather_timestamp.txt"
NOW=$(date +%s)

# Function to fetch weather in background
fetch_weather() {
    # Try fetching short format from wttr.in
    W_DATA=$(curl -s --max-time 2 "wttr.in/?format=%c+%t+%C")
    if [ -n "$W_DATA" ] && [[ ! "$W_DATA" =~ "Unknown" ]] && [[ ! "$W_DATA" =~ "html" ]]; then
        echo "$W_DATA" > "$CACHE_FILE"
        echo "$NOW" > "$CACHE_TIME_FILE"
    fi
}

# Check cache freshness (refresh if older than 900s / 15m or empty)
if [ ! -f "$CACHE_FILE" ] || [ ! -f "$CACHE_TIME_FILE" ]; then
    fetch_weather &
else
    LAST=$(cat "$CACHE_TIME_FILE" 2>/dev/null || echo 0)
    DIFF=$((NOW - LAST))
    if [ "$DIFF" -gt 900 ]; then
        fetch_weather &
    fi
fi

# Read weather if available
WEATHER=""
if [ -f "$CACHE_FILE" ]; then
    WEATHER=$(cat "$CACHE_FILE" | tr -d '\n' | sed 's/  */ /g')
fi

# Battery info
BAT_INFO=""
if [ -f /sys/class/power_supply/BAT0/capacity ]; then
    CAP=$(cat /sys/class/power_supply/BAT0/capacity)
    STATUS=$(cat /sys/class/power_supply/BAT0/status)
    if [ "$STATUS" = "Charging" ]; then
        BAT_INFO="⚡ ${CAP}%"
    else
        BAT_INFO="🔋 ${CAP}%"
    fi
fi

# Format output
OUT=""
if [ -n "$WEATHER" ]; then
    OUT="$WEATHER"
fi

if [ -n "$BAT_INFO" ]; then
    if [ -n "$OUT" ]; then
        OUT="$OUT  •  $BAT_INFO"
    else
        OUT="$BAT_INFO"
    fi
fi

if [ -z "$OUT" ]; then
    OUT="$(date '+%A, %d %B')"
fi

echo "$OUT"
