#!/bin/bash

CONKY_DIR="$HOME/.config/conky"
STYLE_FILE="$CONKY_DIR/current_style.txt"

mkdir -p "$CONKY_DIR/themes" "$CONKY_DIR/scripts"

if [ ! -f "$STYLE_FILE" ]; then
    echo "scifi_hud" > "$STYLE_FILE"
fi
STYLE=$(cat "$STYLE_FILE" 2>/dev/null || echo "scifi_hud")

start_cava_daemon() {
    pkill -f "cava_daemon.py" 2>/dev/null || true
    pkill -f "cava_bin" 2>/dev/null || true
    sleep 0.1
    setsid nohup python3 "$CONKY_DIR/scripts/cava_daemon.py" >/dev/null 2>&1 &
}

stop_cava_daemon() {
    pkill -f "cava_daemon.py" 2>/dev/null || true
    pkill -f "cava_bin" 2>/dev/null || true
    rm -f /tmp/cava_conky.fifo /tmp/cava_bars.txt 2>/dev/null || true
}

start_music_daemon() {
    if ! pgrep -f "music_engine.py --daemon" > /dev/null; then
        setsid nohup python3 "$CONKY_DIR/scripts/music_engine.py" --daemon >/dev/null 2>&1 &
    fi
}

stop_music_daemon() {
    pkill -f "music_engine.py" 2>/dev/null || true
}

launch_conky() {
    local cfg="$1"
    if [ -f "$cfg" ]; then
        setsid nohup conky -c "$cfg" >/dev/null 2>&1 &
    fi
}

start_conky() {
    killall conky 2>/dev/null
    sleep 0.2
    start_cava_daemon
    start_music_daemon
    sleep 0.2
    case "$STYLE" in
        music_studio)
            launch_conky "$CONKY_DIR/themes/ultimate_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/ultimate_hud.conkyrc"
            launch_conky "$CONKY_DIR/themes/music_lyrics_card.conkyrc"
            ;;
        scifi_hud)
            launch_conky "$CONKY_DIR/themes/scifi_core.conkyrc"
            launch_conky "$CONKY_DIR/themes/scifi_telemetry.conkyrc"
            ;;
        scifi_classic)
            if [ -f "$HOME/.conky/conky_start" ]; then
                bash "$HOME/.conky/conky_start" >/dev/null 2>&1 &
            else
                launch_conky "$CONKY_DIR/themes/scifi_core.conkyrc"
                launch_conky "$CONKY_DIR/themes/scifi_telemetry.conkyrc"
            fi
            ;;
        ultimate_dual|modern_hud)
            launch_conky "$CONKY_DIR/themes/ultimate_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/ultimate_hud.conkyrc"
            ;;
        ultimate_card)
            launch_conky "$CONKY_DIR/themes/ultimate_single_card.conkyrc"
            ;;
        catppuccin)
            launch_conky "$CONKY_DIR/themes/catppuccin_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/catppuccin_hud.conkyrc"
            ;;
        nordic)
            launch_conky "$CONKY_DIR/themes/nordic_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/nordic_hud.conkyrc"
            ;;
        cyberpunk)
            launch_conky "$CONKY_DIR/themes/cyberpunk_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/cyberpunk_hud.conkyrc"
            ;;
        whitesur)
            launch_conky "$CONKY_DIR/themes/whitesur_clock.conkyrc"
            launch_conky "$CONKY_DIR/themes/whitesur_hud.conkyrc"
            ;;
        minimal)
            launch_conky "$CONKY_DIR/themes/minimal_clock.conkyrc"
            ;;
        *)
            launch_conky "$CONKY_DIR/themes/scifi_core.conkyrc"
            launch_conky "$CONKY_DIR/themes/scifi_telemetry.conkyrc"
            ;;
    esac
    echo "Conky widgets + Music Studio started ($STYLE)!"
}

stop_conky() {
    killall conky 2>/dev/null
    stop_cava_daemon
    stop_music_daemon
    echo "Conky widgets stopped!"
}

toggle_visualizer_standalone() {
    if pgrep -f "desktop_visualizer.conkyrc" > /dev/null; then
        pkill -f "desktop_visualizer.conkyrc"
        echo "Bottom Audio Visualizer stopped!"
    else
        start_cava_daemon
        launch_conky "$CONKY_DIR/themes/desktop_visualizer.conkyrc"
        echo "Bottom Audio Visualizer started!"
    fi
}

toggle_lyrics_card() {
    if pgrep -f "music_lyrics_card.conkyrc" > /dev/null; then
        pkill -f "music_lyrics_card.conkyrc"
        echo "Desktop Lyrics Card stopped!"
    else
        start_music_daemon
        start_cava_daemon
        launch_conky "$CONKY_DIR/themes/music_lyrics_card.conkyrc"
        echo "Desktop Lyrics Card started!"
    fi
}

toggle_vinyl_player() {
    if pgrep -f "vinyl_player.py" > /dev/null; then
        pkill -f "vinyl_player.py"
        echo "Desktop Vinyl Player stopped!"
    else
        start_music_daemon
        start_cava_daemon
        nohup ~/.local/bin/desktop-music-player >/dev/null 2>&1 &
        echo "Desktop Vinyl Player started!"
    fi
}

case "$1" in
    start)
        start_conky
        ;;
    stop)
        stop_conky
        ;;
    restart)
        start_conky
        ;;
    toggle)
        if pgrep -x "conky" > /dev/null; then
            stop_conky
        else
            start_conky
        fi
        ;;
    visualizer)
        toggle_visualizer_standalone
        ;;
    lyrics)
        toggle_lyrics_card
        ;;
    vinyl)
        toggle_vinyl_player
        ;;
    style)
        if [ -n "$2" ]; then
            echo "$2" > "$STYLE_FILE"
            STYLE="$2"
            start_conky
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|toggle|visualizer|lyrics|vinyl|style [music_studio|scifi_hud|ultimate_dual|catppuccin|nordic|cyberpunk|whitesur|minimal]}"
        ;;
esac
